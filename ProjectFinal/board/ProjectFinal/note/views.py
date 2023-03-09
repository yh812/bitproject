from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from kakao.decorators import login_required
from kakao.models import Member
from note.models import Notelist
from django.template import loader
from django.http.response import HttpResponse
from django.core.paginator import Paginator
import logging
logger = logging.getLogger(__name__)

# Create your views here.
class NoteListView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs )
    def get(self, request):
        login_session = request.session.get('nickname', '')
        user = Member.objects.get(nickname=login_session)
        receive_user = Member.objects.get(nickname=user)
        receivenote = Notelist.objects.filter(receive_user=receive_user).order_by('-send_date')
        send_user = Member.objects.get(nickname=login_session)
        
        page= request.GET.get('page', '1')
        note_paginator = Paginator(receivenote, 10)
        note_page_obj = note_paginator.get_page(page)
        
        context = {"receivenote" : receivenote,
                   "send_user" : send_user,
                   "login_session" : login_session,
                   "note_page_obj" : note_page_obj,
                   }
        return render(request, 'notelist.html', context)
    
class NoteWriteView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs )
    def get(self, request) :
        template = loader.get_template("notewrite.html")
        receive_user = request.GET["receive_user"]
        receive_user = Member.objects.get(nickname=receive_user)
        login_session = request.session.get('nickname', '')
        send_user = Member.objects.get(nickname=login_session)
        context = {"receive_user" : receive_user,
                   "send_user" : send_user
                   }
        return HttpResponse(template.render(context, request))
    def post(self, request):
        receive_user = request.POST["receive_user"]
        receive_user = Member.objects.get(nickname=receive_user)
        send_user = request.POST["send_user"]
        send_user = Member.objects.get(nickname=send_user)
        logger.info(str(send_user)+"*이,"+str(receive_user)+",쪽지받는사람,쪽지보냄")
        dto = Notelist(
            receive_user = receive_user,
            send_user = send_user,
            note_title = request.POST["note_title"],
            note_content = request.POST["note_content"],
            )
        dto.save()
        return redirect("/note/notewrite?receive_user="+str(receive_user))
    
class NoteDetailView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs )
    def get(self, request):
        num = request.GET["num"]
        detaillist = Notelist.objects.get(id=num)
        context = {
            "num" : num,
            "detaillist" : detaillist,
            }
        return render(request, "notedetail.html", context)
        
class NoteDeleteView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs )
    def get(self, request):
        login_session = request.session.get('nickname', '')
        num = request.GET["num"] 
        notelist = Notelist.objects.get(id=num)
        if notelist.receive_user.nickname == login_session:
            notelist.delete()
        return redirect('/note/notelist?receive_user={note}')
    
        