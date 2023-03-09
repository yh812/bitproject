'''
Created on 2022. 12. 28.

@author: joonj
'''
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "로그인 후 사용해 주십시오")
            return redirect("kakao:login")
        return function(request, *args, **kwargs)
    return wrap

def login_required(func):
    def wrapper(request, *args, **kwargs):
        session_id = request.session.get('nickname', "")
        if session_id == "":
            return redirect('kakao:login')
        
        return func(request, *args, **kwargs)
    return wrapper

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.kakao.level =='1' or request.user.level=='0':
            return function(request, *args, **kwargs)
        messages.info(request, "접근 권한이 없습니다.")
        return redirect('/kakao/main/')
    return wrap

def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "접속중인 사용자입니다.")
            return redirect('/kakao/main')
        return function(request, *args, **kwargs)
    return wrap