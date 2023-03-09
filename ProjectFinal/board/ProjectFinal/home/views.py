from django.shortcuts import render
from kakao.models import Member
from board.models import Board

def hello(request):
    context = {}
    
    login_session = request.session.get('userid', '')
    
    if login_session == '':
        context['login_session'] = False
    else:
        context['login_session'] = True
    
    return render(request, 'home/index.html', context)
