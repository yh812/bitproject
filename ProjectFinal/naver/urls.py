'''
Created on 2023. 1. 2.

@author: joonj
'''
from django.urls.conf import path
from naver import views
urlpatterns = [
    path("login", views.NaverLoginView.as_view(), name="naver/login"),
    path("callback", views.NaverLoginCallbackView.as_view(), name="naver/callback"),
    ]