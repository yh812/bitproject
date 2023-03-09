from django.shortcuts import render, redirect
from django.views.generic.base import View
import json
from ProjectSummary.settings import get_secret
import requests
import urllib.request
from django.http.response import JsonResponse, HttpResponse
import logging
from kakao.models import Member
from django.template import loader

logger= logging.getLogger(__name__)

# Create your views here.
class NaverLoginView(View):
    def get(self, request):
        with open('secrets.json') as f:
            secrets = json.loads(f.read())
        app_key = get_secret("NAVER_ID")
        redirect_uri = 'http://localhost:8000/naver/callback'
        naver_auth_api = 'https://nid.naver.com/oauth2.0/authorize?response_type=code'
        state = "login"
        return redirect(
            f'{naver_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}&state={state}'
        )
        #네이버 로그인 인증 요청 : https://nid.naver.com/oauth2.0/authorize
        #접근 토큰의 발급, 갱신, 삭제 요청 : https://nid.naver.com/oauth2.0/token
    def post(self):
        pass
    
class NaverLoginCallbackView(View):
    def get(self, request):
        with open('secrets.json') as f:
            secrets= json.loads(f.read())
        client_id = get_secret("NAVER_ID")
        client_secret = get_secret("NAVER_SECRET")
        code = request.GET.get('code')
        state = request.GET.get('state')
        authorization_code = "authorization_code"
        token_api = "https://nid.naver.com/oauth2.0/token"
        token_response = requests.get(token_api, params={'grant_type':authorization_code,'client_id':client_id, 'client_secret':client_secret, 'code':code,'state':state})
        
        access_token = token_response.json().get('access_token')
        refresh_token = token_response.json().get('refresh_token')
        token_type=token_response.json().get('token_type')
        expires_in=token_response.json().get('expires_in')
        
        header = "Bearer "+access_token
        url = "https://openapi.naver.com/v1/nid/me"
        requested = urllib.request.Request(url)
        requested.add_header("Authorization", header)
        response = urllib.request.urlopen(requested)
        rescode = response.getcode()
        if(rescode ==200):
            response_body = response.read()
            response_content = response_body.decode('utf-8')
            response_content = json.loads(response_content)
        else:
            print("Error Code : "+rescode)
        
            
        id = response_content["response"]["id"]
        passwd = response_content["response"]["id"]
        nickname = response_content["response"]["nickname"]
        profile_image=response_content["response"]["profile_image"]
        age = response_content["response"]["age"]
        email = response_content["response"]["email"]
        mobile = response_content["response"]["mobile"]
        birthday = response_content["response"]["birthyear"]+"-"+response_content["response"]["birthday"]
        
        if Member.objects.filter(userid=id).exists():
            request.session["userid"]=id
            request.session["nickname"]=nickname
            dto = Member.objects.get(userid=id)
            dto.user_current_point+=30
            dto.user_total_point+=30
            return redirect("kakao:main")
        else:
            dto = Member(                
                userid = id,
                passwd = passwd,
                nickname = nickname,
                generation = age,
                birth = birthday,
                userimage = profile_image,
                social="n",
                tel = mobile,
                user_current_point = 50,
                user_total_point = 50,)
            
            dto.save()
            
        request.session["userid"]=id
        request.session["nickname"]=nickname
        return redirect("kakao:main")

