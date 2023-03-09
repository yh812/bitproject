from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice, Table, Survey_Status
from django.urls import reverse
from django.views import generic
from kakao.models import Member
from django.views.decorators.csrf import csrf_exempt
from kakao.decorators import login_message_required, login_required
from django.utils.decorators import method_decorator
import logging
from django.template import loader

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def index(request):
    template = loader.get_template('index.html')
    #login_session = request.session.get('login_session', '')
    session_id = request.session.get('nickname', "")
    bs_id = Member.objects.get(nickname=session_id) 
    survey_status = Survey_Status.objects.filter(bs_id=bs_id)
    context = {
                   'session_id' : session_id,
                   'survey_status' : survey_status,
                   }
    return HttpResponse(template.render(context, request)) 
    
  
class DetailView(generic.DetailView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return generic.DetailView.dispatch(self, request, *args, **kwargs )
    model = Question
    template_name = 'detail.html'
    def get_queryset(self):
        """
        아직 게시되지 않은 질문은 제외합니다.
        """
        return Question.objects.all()
    
    
        
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 질문 투표 양식을 다시 표시하십시오. detail.html
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "선택지를 선택하세요.",
            })
    
    else:
        #login_session = request.session.get('login_session', '')
        session_id = request.session.get('nickname')
        bs_id = Member.objects.get(nickname=session_id)
        #bs_id = Member.objects.get(userid=login_session)
        table = Table(
            bs_id = bs_id,
            question_name = question,
            choice_text_name = selected_choice,
            )
        table.save()
        selected_choice.votes += 1
        selected_choice.save()
        # 성공적으로 처리 한 후 항상 HttpResponseRedirect
        # POST 데이터 포함 이렇게하면 데이터 두 번 게시x
        # 사용자가 뒤로 버튼 누르십시오
        if question_id == len(Question.objects.all()) :
            survey_status = Survey_Status(
                bs_id = bs_id,
                status = "n"
                )
            survey_status.save()
            dtos = Member.objects.get(nickname=session_id)
            dtos.user_total_point += 200
            dtos.user_current_point += 200
            dtos.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else :
            question_id += 1
            return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
        


    