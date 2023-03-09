'''
Created on 2022. 12. 28.

@author: joonj
'''
from django.urls.conf import path
from kakao import views

app_name="kakao"
urlpatterns = [
        path("main", views.MainView.as_view(), name="main"),
        path("login", views.MainLoginView.as_view(), name="login"),
        path("logout", views.LogoutView.as_view(), name="logout"),
        path("register", views.RegisterView.as_view(), name="register"),
        
        #아이디/비밀번호찾기
        path( "findid", views.FindIdView.as_view(), name="findid" ),
        path( "findpw", views.FindPWView.as_view(), name="findpw" ),
        
        #아이디/이름/이메일 중복확인 (ajax)
        path("idchk", views.IdChkView.as_view(), name="idchk"),
        path("namechk", views.NameChkView.as_view(), name="namechk"),
        path("emailchk", views.EmailChkView.as_view(), name="emailchk"),
        
        #게시판
        path("music", views.MusicView.as_view(), name="music"),
        path("muscipro", views.MusicproView.as_view(), name="musicpro"),
        path("paint", views.PaintView.as_view(), name="paint"),
        path("free", views.FreeView.as_view(), name="free"),
        path("advertise", views.AdvertiseView.as_view(), name="advertise"),
        path("portfolio", views.PortfolioView.as_view(), name="portfolio"),
        path("game", views.GameView.as_view(), name="game"),
        path("general_search", views.GeneralSearchView.as_view(), name="general_search"),
        
        #회원정보 관리
        path( "modify", views.ModifyView.as_view(), name="modify" ),
        path( "modifyPro", views.ModifyProView.as_view(), name="modifypro" ),
        path('delete', views.DeleteView.as_view(), name="delete"),
        path('registerpro', views.RegisterProView.as_view(), name="registerpro"),
        
        #kakao callback
        path("kakaologin", views.KakaoLoginView.as_view(), name="kakaologin"),
        path("login/callback", views.KakaoLoginCallbackView.as_view(), name="login/callback"),
        
    ]