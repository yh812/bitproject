from django.shortcuts import render, redirect
from django.views.generic.base import View
import json
from ProjectSummary.settings import get_secret
from django.template import loader
from django.http.response import HttpResponse, JsonResponse
import requests
from django.core.exceptions import ObjectDoesNotExist
from kakao.models import Member
import urllib.request
import logging
from django.contrib.auth.models import User
from django.core.paginator import Paginator
#email 전송용
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from kakao.tokens import account_activation_token
import random
#board
from board.models import Board, Adboard, Comment, Comment_count, Notice
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
logger= logging.getLogger(__name__)
    
########################## 메인화면 localhost:8000/kakako/main########################    
class MainView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        template=loader.get_template("main.html")
        session_id = request.session.get('nickname')
        userid = request.session.get('userid')
        
        #실시간/music/paint/free  ->출력부분
        alls = Board.objects.all().order_by("-write_dttm")[0:8]
        #음악
        musics =Board.objects.all().filter(board_name="Music").order_by("-like_count")[0:8]
        #그림
        paints = Board.objects.all().filter(board_name='Picture').order_by("-like_count")[0:8]
        #자유게시판
        frees = Board.objects.all().filter(board_name='Free').order_by("-like_count")[0:8]
        #광고
        ads = Adboard.objects.all().filter(accept=True)
        adlist = []
        for i in ads:
            adlist.append(i)
        ad_random = random.choice(adlist)
        
        if session_id == None:
            session_id = "None"
            context={
                "session_id" : session_id,
                "alls":alls,
                "musics":musics,
                "paints":paints,
                "frees":frees,
                "ad_random":ad_random,
                }
        else :
            dto = Member.objects.get(userid = userid)
            context={
                "session_id" : session_id,
                "alls":alls,
                "musics":musics,
                "paints":paints,
                "frees":frees,
                "ad_random":ad_random,
                "dto":dto
                }
        logger.info(str(session_id)+"*이,메인페이지이동")
        
        return HttpResponse(template.render(context, request))
    
    def post(self, request):
        session_id = request.session.get('nickname')
        print(session_id)
        template = loader.get_template("main.html")
        context = {
            "session_id" : session_id
            }
        return HttpResponse(template.render(context, request))
########################################################################################
################## 로그인 화면 localhost:8000/kakao/login#############################    
class MainLoginView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        template = loader.get_template('login.html')
        context={}
        return HttpResponse(template.render(context, request))
        
    def post(self, request):
        userid = request.POST["id"]
        passwd = request.POST["passwd"]
        message = ""
        try : 
            dto = Member.objects.get(userid=userid)
            if passwd == dto.passwd :
                request.session["nickname"] = dto.nickname
                request.session["userid"]=dto.userid
                session_id = request.session.get('nickname')
                dto.user_total_point += 30
                dto.user_current_point += 30
                logger.info(str(session_id) + "*이,로그인")
                dto.save()
                context = {
                        "session_id" : session_id
                    }
                return redirect("kakao:main")
            else:
                message = "입력하신 비밀번호가 다릅니다."
        except ObjectDoesNotExist:
            message = "입력하신 아이디가 없습니다."
        template = loader.get_template("login.html")
        context = {
            "message" : message,
            }
        return HttpResponse(template.render(context, request))
#################################################################################3

###########################로그아웃 ###############################
class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        session_id = request.session.get('nickname')
        logger.info(str(session_id)+"*이,로그아웃")
        request.session.flush()
        return redirect("kakao:main")
    
    def post(self, request):
        session_id = request.session.get('nickname')
        logger.info(str(session_id)+"*로그아웃post")
        request.session.flush()
        return redirect("kakao:main")
####################################################################

#######################회원정보수정##############################
class ModifyView( View ) :
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request ) :
        template = loader.get_template( "modify.html" )
        context = {}
        return HttpResponse( template.render( context, request ) )   
         
    def post(self, request ) :
        session_id = request.session.get( "nickname" )
        id = request.session.get("userid")
        logger.info(str(session_id)+"*이,회원정보수정")
        passwd = request.POST["passwd"]
        dto = Member.objects.get( userid=id )
        if passwd == dto.passwd :
            template = loader.get_template( "modifypro.html" )
            context = {
                "dto" : dto
                }
            return HttpResponse( template.render( context, request ) )
        else :
            template = loader.get_template( "modify.html" )
            context = {
                "message" : "비밀번호가 다릅니다",
                }
            return HttpResponse( template.render( context, request ) )

class ModifyProView ( View ) :
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def post(self, request ) :
        id = request.session.get( "userid" )
        passwd = request.POST["passwd"]
        repasswd = request.POST["repasswd"]
        birth = request.POST["birth"]
        tel = request.POST["tel"]
        address = request.POST["address"]
        address2 = request.POST["address2"]
        userimg= request.FILES.get('userimg')
        
        dto = Member.objects.get( userid=id )
        dto.passwd = passwd
        dto.repasswd = repasswd
        dto.tel = tel
        dto.address = address
        dto.address2 = address2
        dto.birth = birth
        dto.userimg = userimg
        dto.save()
        return redirect( "kakao:main" )
#####################################################################
  
###########################회원탈퇴###################################
class DeleteView( View ) :
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request ) :
        template = loader.get_template( "delete.html" )
        id = request.session.get( "userid" )
        dto = Member.objects.get( userid=id )
        context = {"dto" : dto}
        return HttpResponse( template.render( context, request ) )    
    
    def post(self, request ) : 
        id = request.session.get( "userid" )
        passwd = request.POST["passwd"]
        dto = Member.objects.get( userid=id )
        if passwd == dto.passwd :
            dto.delete()
            request.session.flush()
            return redirect( "kakao:main" )   
        elif dto.social !="-":
            dto.delete()
            request.session.flush()
            return redirect("kakao:main")
        else :
            template = loader.get_template( "delete.html" )
            context = {
                "message" : "비밀번호가 다릅니다",
                "dto" : dto,
                }
            return HttpResponse( template.render( context, request ) )
############################################################################

#######################카카오 로그인#################################
class KakaoLoginView(View):
    def get(self, request):
        with open('secrets.json') as f:
            secrets = json.loads(f.read())
        app_key = get_secret("KAKAO_REST_API")
        redirect_uri = 'http://localhost:8000/kakao/login/callback'
        kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
        return redirect(
            f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}'
        )
        
    def post(self, request):
        with open('secrets.json') as f:
            secrets = json.loads(f.read())
        app_key = get_secret("KAKAO_REST_API")
        redirect_uri = 'http://localhost:8000/kakao/login/callback'
        kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
        return redirect(
            f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}'
        )
    
class KakaoLoginCallbackView(View):
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type" : "authorization_code",
            "client_id" : get_secret("KAKAO_REST_API"),
            "client_secret" : get_secret("KAKAO_SECURITY"),
            "redirect_uri" : "http://localhost:8000/kakao/login/callback",
            "code" : auth_code
            }
        
        token_response =  requests.post(url=kakao_token_api,data=data)
        print(token_response)
        access_token =token_response.json().get('access_token')
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization":f'Bearer ${access_token}', "Content-type": "application/x-www-form-urlencoded;charset=utf-8"})

        user = user_info_response.json()

        userid = user['id']
        nickname = user['properties']['nickname']
        passwd = user['id']
        if "email" in user['kakao_account'] : 
            email = user['kakao_account']['email']
        else:
            email = ""
        if "phone_number" in user['kakao_account']:
            phone = user["kakao_account"]['phone_number']
        else:
            phone = ""
        gender = user['kakao_account']['gender']
        generation = user['kakao_account']['age_range']
        birth = user['kakao_account']['birthday']            
        userimage = user['kakao_account']['profile']['profile_image_url']
        regdate = user['connected_at']
        
        if Member.objects.filter(userid=userid).exists():
            request.session["userid"]=userid
            request.session["nickname"]=nickname
            dto = Member.objects.get(userid=userid)
            dto.user_current_point +=30
            dto.user_total_point +=30
            dto.save()
            return redirect("kakao:main")
        else:
            dto = Member(
                userid = userid,
                nickname = nickname,
                passwd = passwd,
                email = email,
                gender = gender,
                generation = generation,
                birth = birth,
                userimg = userimage,
                regdate = regdate,
                social = "k",
                tel = phone,
                user_total_point =50,
                user_current_point =50,
            )
            dto.save()
            
        user = User.objects.create_user(username = userid, email = email, password = str(passwd), first_name=nickname, last_name="-")
            
        request.session["userid"]=userid
        request.session["nickname"]=nickname
        return redirect("kakao:main")
    
    def post(self, request):
        pass
#############################################################

####################### 회원가입 ############################
class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        template = loader.get_template('register.html')
        context = {}
        return HttpResponse(template.render(context, request))
    
    def post(self, request):
        userid = request.POST.get("id")
        passwd = request.POST.get("passwd")
        nickname = request.POST.get("user_name")
        birth = request.POST.get("birth")
        userimg = request.FILES.get('userimg')
        generation = "."
        email = request.POST.get("email")
        if request.POST.get("address"): 
            address = request.POST.get("address")
            if request.POST.get("address2"):
                address2 = request.POST.get("address2")
            else:
                address2 = ""
        else : 
            address = request.POST["address"]
            
        if request.POST["tel"]:
            tel = request.POST["tel"]
        else : 
            tel = ""
            
        dto = Member(
            userid = userid,
            nickname = nickname,
            passwd = passwd,
            email = email,
            gender = "Null",
            generation = generation,
            birth = birth,
            userimage = "Null",
            social = "-",
            address = address,
            address2 = address2,
            tel = tel,
            userimg =userimg,
            user_total_point =50,
            user_current_point =50,
            )
        dto.save()
        
        #이메일 전송
        '''
        if request.POST['passwd'] ==request.POST['repasswd']:
            user = User.objects.create_user(username=request.POST['user_name'], password=request.POST['repasswd'])
            user.is_active = False # 유저 비활성화
            user.save()
            username=request.POST['user_name']
            userid=request.POST['id']
            userpw=request.POST['passwd']
            current_site = get_current_site(request) 
            message = render_to_string('activation_email.html', {
                'username': username,
                'userid': userid,
                'userpw': userpw,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send() 
        '''
        template = loader.get_template("main.html")
        context = {}
        if Member.objects.filter(userid=id).exists():
            request.session["userid"]=userid
            request.session["nickname"]=nickname
            return redirect("kakao:main")
        
            
        return redirect("kakao:login")
##################### 회원가입 end #############################

#################3개인정보 수집 및 이용##############################
class RegisterProView(View):
    def get(self, request):
        return render(request, 'registerpro.html') 
###############################################################

######################## 아이디 중복확인 ajax ####################
class IdChkView(View):
    def get(self, request):
        template = loader.get_template("idchk.html")
        context = {}
        return HttpResponse(template.render(context, request))
    
    def post(self, request):
        template = loader.get_template("register.html")
        id = request.POST["id"]
        dto = Member.objects.get(userid=id)
        result = 0
        try:
            # 아이디가 있을때
            Member.objects.get(userid=id)
            result = 1
        except ObjectDoesNotExist:
            # 아이디가 없을때
            result = 0
        context = {
            "id" : id,
            "result" : result,
            }
        return HttpResponse(template.render(context, request))

    
#################### 이름 중복확인 ajax ##########################
class NameChkView(View):    
    def post(self, request):
        template = loader.get_template("register.html")
        user_name = request.POST["user_name"]
        dto = Member.objects.get(nickname=user_name)
        result = 0
        try:
            # 이름 있을때
            Member.objects.get(nickname=user_name)
            result = 1
        except ObjectDoesNotExist:
            # 이름 없을때
            result = 0
        context = {
            "user_name" : user_name,
            "result" : result,
            }
        return HttpResponse(template.render(context, request))

# 이메일 중복확인 ajax
class EmailChkView(View):    
    def post(self, request):
        template = loader.get_template("register.html")
        email = request.POST["email"]
        dto = Member.objects.get(email=email)
        result = 0
        try:
            # 이메일 있을때
            Member.objects.get(email=email)
            result = 1
        except ObjectDoesNotExist:
            # 이메일 없을때
            result = 0
        context = {
            "email" : email,
            "result" : result,
            }
        return HttpResponse(template.render(context, request))
####################################################################

########################## 아이디 찾기#######################
class FindIdView(View):
    def get(self, request):
        template = loader.get_template("findid.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        template = loader.get_template("findid.html")
        email = request.POST["email"]  
        result = 0
        try:
            dto = Member.objects.get(email=email)
            result = 1
            context = {
                "userid": dto.userid,
                "result": result
                }
        except ObjectDoesNotExist:     
            msg = ""
            result = 0
            context = {
                "result": result,
                "msg": "해당하는 이메일이 없습니다"     
            }
        return HttpResponse(template.render(context, request))
####################################################################

########################## 비밀번호 찾기 #############################3
class FindPWView(View):
    def get(self, request):
        template = loader.get_template("findpw.html")
        context = {}
        return HttpResponse(template.render(context, request))
    
    def post(self, request) :
        template = loader.get_template("findpw.html")
        email = request.POST["email"]
        id = request.POST["id"]
        tel = request.POST["tel"]  
        result = 0
        try:
            dto = Member.objects.get(email=email, userid=id, tel=tel)
            result = 1
            context = {
                "passwd": dto.passwd,
                "result": result
                }
        except ObjectDoesNotExist:     
            msg = ""
            result = 0
            context = {
                "result": result,
                "msg": "정보가 일치하지 않습니다"     
            }
        return HttpResponse(template.render(context, request)) 
########################################################

################ 게시판 #########################    
class MusicView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        template = loader.get_template('musicboard.html')
        session_id = request.session.get('nickname')
        
        dtos = Board.objects.filter(board_name='Music').order_by('-write_dttm')
        
        ads = Adboard.objects.all().filter(accept=True)
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)
        # category용    
        try : 
            cate = request.GET.get("cate")
            
        except:
            cate = ""
        
        if cate :
            logger.info(str(session_id)+"*이,"+'Music'+",게시판종류,"+str(cate)+",카테고리정렬")
            dtos=Board.objects.filter(category__contains=cate).order_by('-write_dttm')
        if cate == None:
            cate = ""
        # 정렬용
        try :
            sort = request.GET.get("sort")
        except:
            sort=""
        if sort == "like" :
            dtos = Board.objects.filter(board_name='Music').order_by("-like_count")
            logger.info(str(session_id)+"*이,"+'Music'+",게시판종류,"+str(sort)+",정렬기준")
            if cate :
                logger.info(str(session_id)+"*이,"+'Music'+",게시판종류,"+str(cate)+",카테고리정렬")
                dtos=Board.objects.filter(category__contains=cate).order_by('-like_count')
        elif sort == "write_dttm" :
            dtos = Board.objects.filter(board_name='Music').order_by("-write_dttm")
            logger.info(str(session_id)+"*이,"+'Music'+",게시판종류,"+str(sort)+",정렬기준")
            if cate :
                logger.info(str(session_id)+"*이,"+'Music'+",게시판종류,"+str(cate)+",카테고리정렬")
                dtos=Board.objects.filter(category__contains=cate).order_by('-write_dttm')
        elif sort == "follow" :
            dtos = Board.objects.filter(board_name='Music').order_by("-follow_count")
            logger.info(str(session_id)+"*이,"+'Music'+",게시판종류,"+str(sort)+",정렬기준")
            if cate :
                logger.info(str(session_id)+"*이,"+'Music'+",게시판종류,"+str(cate)+",카테고리정렬")
                dtos=Board.objects.filter(category__contains=cate).order_by('-follow_count')
        
        
        
        page = request.GET.get('page', '1')
        paginator = Paginator(dtos, 10)
        page_obj = paginator.get_page(page)
        
        if session_id:
            logger.info(session_id+"*이,"+'Music'+",게시판종류,접근")
            user = Member.objects.get(nickname=session_id)
            context={
            "sort" : sort,
            "session_id" : session_id,
            "user" : user,
            "dtos":dtos,
            "ad_random":ad_random,
            "cate":cate,
            "pageobject" : page_obj
            }
            return HttpResponse(template.render(context,request))
        else:
            context={
            "session_id" : session_id,
            "dtos":dtos,
            "ad_random":ad_random,
            "cate":cate,
            "pageobject" : page_obj
            }
            return HttpResponse(template.render(context, request))
    def post(self, request):
        session_id = request.session.get('nickname')
        if not session_id : 
            session_id = "None"
            
        dtos = Board.objects.filter(board_name='Music').order_by('-write_dttm')
        try : 
            searchkey = request.POST["searchkey"]
        except:
            searchkey = "name"   
        try : 
            search = request.POST["search"]
        except:
            search = ""
        
            
        if searchkey == "name_content":
            logger.info(str(session_id)+"*이,"+"Music"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos = Board.objects.filter(Q(board_name='Music', title__contains=search) | Q(board_name='Music', substance__contains=search)).order_by("-write_dttm")
        elif searchkey=="writer":
            logger.info(str(session_id)+"*이,"+"Music"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name='Music', writer__nickname__icontains=search)               
        elif searchkey=="name":
            logger.info(str(session_id)+"*이,"+"Music"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name='Music', title__contains=search)
        elif searchkey=="writer":
            logger.info(str(session_id)+"*이,"+"Music"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name='Music', title__contains=search)
        else:
            logger.info(str(session_id)+"*이,"+"Music"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name='Music', substance__contains=search)
        
        # 카테고리 검색    
        try : 
            categorykey= request.POST.get("categorykey")
        except:
            categorykey = ""
        if categorykey :
            logger.info(str(session_id)+"*이,"+"Music"+",게시판종류,"+categorykey+",사이드카테고리검색")
            dtos=Board.objects.filter(category__contains=categorykey).order_by('-write_dttm')
        print(categorykey)
        print(dtos)
        page = request.GET.get('page', '1')
        paginator = Paginator(dtos, 5)
        page_obj = paginator.get_page(page)
        ads = Adboard.objects.all().filter(accept=True)
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist) 
        context = {
            "session_id" : session_id,
            "dtos" : dtos,
            "searchkey" : searchkey,
            "search" : search,
            "categorykey" : categorykey,
            'pageobject' : page_obj,
            "ad_random" : ad_random
            }
        return render(request, "musicboard.html", context)
    
######## 그냥 써보는 거 <audio tag> ########

class MusicproView(View):
    def get(self):
        pass
    def post(self):
        pass
        
class PaintView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        template = loader.get_template('paintboard.html')
        session_id = request.session.get('nickname')
        dtos = Board.objects.filter(board_name='Picture').order_by('-write_dttm')
        accept = Adboard.objects.filter(accept = True).order_by('-write_dttm')
        
        ads = Adboard.objects.all().filter(accept=True)
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)
        # category용    
        try : 
            cate = request.GET.get("cate")
            
        except:
            cate = ""
        
        if cate :
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+str(cate)+",카테고리정렬")
            dtos=Board.objects.filter(category__contains=cate).order_by('-write_dttm')   
        # 정렬용
        try :
            sort = request.GET.get("sort")
        except:
            sort=""
        if cate == None:
            cate = ""
        if sort == "like" :
            dtos = Board.objects.filter(board_name='Picture').order_by("-like_count")
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+str(sort) +",정렬기준")
            if cate :
                logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+str(cate)+",카테고리정렬")
                dtos=Board.objects.filter(category__contains=cate).order_by('-like_count')   
        elif sort == "write_dttm" :
            dtos = Board.objects.filter(board_name='Picture').order_by("-write_dttm")
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+str(sort) +",정렬기준")
            if cate :
                logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+str(cate)+",카테고리정렬")
                dtos=Board.objects.filter(category__contains=cate).order_by('-write_dttm')   
        elif sort == "follow" :
            dtos = Board.objects.filter(board_name='Picture').order_by("-follow_count")
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+str(sort) +",정렬기준")
            if cate :
                logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+str(cate)+",카테고리정렬")
                dtos=Board.objects.filter(category__contains=cate).order_by('-follow_count')   
            
        
        
        page = request.GET.get('page', '1')
        paginator = Paginator(dtos, 12)  #원래 10개였음.
        page_obj = paginator.get_page(page)
        
        if session_id:
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,접근")
            user = Member.objects.get(nickname=session_id)
            context={
            "session_id" : session_id,
            "user":user,
            "dtos":dtos,
            "ad_random":ad_random,
            "cate" : cate,
            "pageobject":page_obj,
            "sort":sort
            }
            return HttpResponse(template.render(context,request))
        else:
            context={
            "session_id" : session_id,
            "dtos":dtos,
            "ad_random":ad_random,
            "cate" : cate,
            "pageobject":page_obj,
            "sort":sort
            }
            return HttpResponse(template.render(context,request))
        
    def post(self, request):
        session_id = request.session.get('nickname')
        dtos = Board.objects.filter(board_name='Picture').order_by('-write_dttm')
        if not session_id : 
            session_id = "None"
            
        try : 
            searchkey = request.POST["searchkey"]
        except:
            searchkey = "name"
            
        try : 
            search = request.POST["search"]
        except:
            search = ""
        
        if searchkey == "name_content":
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos = Board.objects.filter(Q(board_name='Picture',title__contains=search) | Q(substance__contains=search)).order_by("-write_dttm")
        elif searchkey=="name":
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name='Picture',title__contains=search)
        elif searchkey=="writer":
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name='Picture',writer__nickname__icontains=search)     
        else:
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name='Picture',substance__contains=search)
        
        # 카테고리 검색    
        try : 
            catekey = request.POST.get("catekey")
        except:
            catekey = ""
        if catekey :
            logger.info(str(session_id)+"*이,"+"Picture"+",게시판종류,"+catekey+",사이드카테고리검색")
            dtos=Board.objects.filter(category__contains=catekey).order_by('-write_dttm')
        page = request.GET.get('page', '1')
        paginator = Paginator(dtos, 12)  #원래 10개였음.
        page_obj = paginator.get_page(page)
        
        ads = Adboard.objects.all().filter(accept=True)
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)
        
        context = {
            "session_id" : session_id,
            "dtos" : dtos,
            "searchkey" : searchkey,
            "search" : search,
            "catekey" : catekey,
            'pageobject' : page_obj,
            "ad_random" : ad_random
            }
        return render(request, "paintboard.html", context)
    
class FreeView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        template = loader.get_template('freeboard.html')
        session_id = request.session.get('nickname')
        dtos = Board.objects.all().filter(board_name="Free").order_by('-write_dttm')
        ads = Adboard.objects.all().filter(accept=True)
        notice = Notice.objects.all().order_by('-write_dttm')
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)
        
        page = request.GET.get('page', '1')
        paginator = Paginator(dtos, 10)
        notice_page = Paginator(notice,7)
        page_obj = paginator.get_page(page)
        notice_page_obj= notice_page.get_page(page)
        
        if session_id:
            logger.info(str(session_id)+"*이,"+"Free"+ ",게시판종류,로접근.")
            user = Member.objects.get(nickname=session_id)
            context={
            "session_id" : session_id,
            "user" : user,
            "dtos":dtos,
            "ad_random":ad_random,
            "pageobject":page_obj,
            "notice":notice,
            "notice_page_obj" : notice_page_obj,
            }
            return HttpResponse(template.render(context, request))
        else:
            context={
            "session_id" : session_id,
            "dtos":dtos,
            "ad_random":ad_random,
            "pageobject":page_obj,
            "notice":notice,
            "notice_page_obj" : notice_page_obj,
            }
            return HttpResponse(template.render(context, request))
        
    def post(self, request):
        session_id = request.session.get('nickname')
        dtos = Board.objects.filter(board_name='Free').order_by('-write_dttm')
        if not session_id : 
            session_id = "None"
            
        try : 
            searchkey = request.POST["searchkey"]
        except:
            searchkey = "name"
            
        try : 
            search = request.POST["search"]
        except:
            search = ""
            
        if searchkey == "name_content":
            logger.info(str(session_id)+"*이,"+"Free"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos = Board.objects.filter(Q(board_name="Free", title__contains=search) | Q(substance__contains=search)).order_by("-write_dttm")   
        elif searchkey=="name":
            logger.info(str(session_id)+"*이,"+"Free"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name="Free", title__contains=search)
        elif searchkey=="writer":
            logger.info(str(session_id)+"*이,"+"Free"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name="Free", writer__nickname__icontains=search)
        else:
            logger.info(str(session_id)+"*이,"+"Free"+",게시판종류,"+searchkey+",검색조건,"+search+",검색")
            dtos=Board.objects.filter(board_name="Free", substance__contains=search)
        page = request.GET.get('page', '1')
        paginator = Paginator(dtos, 10)
        page_obj = paginator.get_page(page) 
        ads = Adboard.objects.all().filter(accept=True)
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)
        context = {
            "session_id" : session_id,
            "dtos" : dtos,
            "searchkey" : searchkey,
            "search" : search,
            "pageobject":page_obj,
            "ad_random":ad_random,
            }
        return render(request, "freeboard.html", context)

class AdvertiseView(View):
    def get(self, request):
        template = loader.get_template('advertise.html')
        session_id = request.session.get('nickname')
        
        dtos = Adboard.objects.all().order_by('-write_dttm')
        accept = Adboard.objects.filter(accept = True).order_by('-write_dttm')
        ads = Adboard.objects.all().filter(accept=True)
        notice = Notice.objects.all().order_by('-write_dttm')

        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)

        page = request.GET.get('page', '1')
        ad_paginator = Paginator(accept, 10)
        ad_page_obj = ad_paginator.get_page(page)
        notice_page = Paginator(notice,7)
        notice_page_obj = notice_page.get_page(page)
        
        if session_id:
            logger.info(str(session_id)+"*이,"+"Ad"+",게시판종류,접근")
            dto = Member.objects.get(nickname=session_id)
            if dto.user_current_point < 1000:
                goorani = True
            else:
                goorani = False
            context={
            "session_id" : session_id,
            "dtos" : dtos,
            "dto":dto,
            "accept" : accept,
            "ad_random" : ad_random,
            "goorani" : goorani,
            "ad_pageobject":ad_page_obj,
            "notice_page_obj" : notice_page_obj
            }
            return HttpResponse(template.render(context, request))
        else:
            context={
            "session_id" : session_id,
            "dtos" : dtos,
            "accept" : accept,
            "ad_random" : ad_random,
            "goorani" : True,
            "ad_pageobject":ad_page_obj,
            "notice_page_obj" : notice_page_obj
            }
            return HttpResponse(template.render(context, request))
        
class PortfolioView(View):
    def get(self, request):
        template = loader.get_template('portfolio.html')
        session_id = request.session.get('userid')
        if session_id:
            logger.info(str(session_id)+"*이,portfolio,로접근.")
        context={
            "session_id":session_id}
        return HttpResponse(template.render(context, request))

class GameView(View):
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        template = loader.get_template('game.html')
        ads = Adboard.objects.all().filter(accept=True)
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)
        session_id = request.session.get('nickname')
        if session_id :
            logger.info(str(session_id)+"*이,game,로접근.")
            dto = Member.objects.get(nickname=session_id)
            context ={
                "session_id" : session_id,
                "user_total_point" : dto.user_total_point,
                "user_current_point" : dto.user_current_point,
                "ad_random":ad_random,
                "dto":dto
                }
            return HttpResponse(template.render(context, request))
        else:
            return redirect('kakao:login')
    
    def post(self, request):
        computer = ["가위","바위","보"]
        session_id = request.session.get('userid')
        nickname= request.session.get('nickname')
        dto = Member.objects.get(userid=session_id)
        wincounter = request.POST.get('wincounter') 
        game_start=request.POST.get('game_start')
        gorani = request.POST.get('wincounter')
        member = Member.objects.get(userid=session_id)
        if game_start== "chan" : # ajax에서 넘겨받는 데이터 게임 패배와 관련있음
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,패배함')            
            member.user_current_point -=20
            member.save()            
        # ajax에서 넘겨받는 데이터 게임 승리와 관련있음
        if gorani == "1":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함') 
            member.user_current_point += 20
            member.user_total_point +=   20
            member.save()
        elif gorani == "2":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 30
            member.user_total_point +=   30            
            member.save()
        elif gorani == "3":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 50
            member.user_total_point +=   50            
            member.save()
        elif gorani == "4":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 90
            member.user_total_point +=   90            
            member.save()
        elif gorani == "5":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 130
            member.user_total_point +=   130            
            member.save()                  
        elif gorani == "6":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 260
            member.user_total_point +=   260            
            member.save()  
        elif gorani == "7":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 700
            member.user_total_point +=   700            
            member.save()
        elif gorani == "8":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 1000
            member.user_total_point +=   1000            
            member.save()
        elif gorani == "9":
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 1500
            member.user_total_point +=   1500            
            member.save()                  
        elif gorani == "10" :
            logger.info(str(nickname)+"*이," +str(member.user_current_point)+',점에서시작해,'+gorani+',연승함')
            member.user_current_point += 3000
            member.user_total_point +=   3000            
            member.save()                                       
        context = {
            "session_id" : session_id,
            "user_total_point" : dto.user_total_point,
            "user_current_point" : dto.user_current_point,
            "computer":computer,
            "wincounter":wincounter
            }
        return HttpResponse(json.dumps(context), content_type='application/json')

class GeneralSearchView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request):
        template = loader.get_template("general_search.html")
        session_id = request.session.get("nickname")
        
    
        ads = Adboard.objects.all().filter(accept=True)
        
        adlist = []
        for i in ads:
            adlist.append(i)

        ad_random=random.choice(adlist)
        
        searchkey = request.GET.get("general_search")
        
        
        if searchkey:
            logger.info(str(session_id)+"*이,"+str(searchkey)+",전체검색")
            musics = Board.objects.filter(Q(board_name='Music', title__icontains=searchkey) | Q(board_name='Music', substance__icontains=searchkey)| Q(board_name='Music', writer__nickname__icontains=searchkey)).order_by("-write_dttm")
            pictures = Board.objects.filter(Q(board_name='Picture', title__icontains=searchkey) | Q(board_name='Picture', substance__icontains=searchkey)| Q(board_name='Picture', writer__nickname__icontains=searchkey)).order_by("-write_dttm")
            frees = Board.objects.filter(Q(board_name='Free', title__icontains=searchkey) | Q(board_name='Free', substance__icontains=searchkey)| Q(board_name='Free', writer__nickname__icontains=searchkey)).order_by("-write_dttm")
            
            musicpage = request.GET.get('musicpage', '1')
            musicpaginator = Paginator(musics, 5)
            musicpage_obj = musicpaginator.get_page(musicpage)
            
            picturepage = request.GET.get('picturepage', '1')
            picturepaginator = Paginator(pictures, 8)
            picturepage_obj = picturepaginator.get_page(picturepage)
            
            freepage = request.GET.get('freepage', '1')
            freepaginator = Paginator(frees, 5)
            freepage_obj = freepaginator.get_page(freepage)
            
            musicpage = request.GET.get("musicpage")
            picturepage = request.GET.get("picturepage")
            freepage = request.GET.get("freepage")
            #dto = Member.objects.get(nickname = session_id)
            
            context={
                "general_search" : searchkey,
                "ad_random" : ad_random,
                "musicpage_obj" : musicpage_obj,
                "picturepage_obj" : picturepage_obj,
                "freepage_obj" : freepage_obj,
                "session_id" : session_id,
                "musicpage" : musicpage,
                "picturepage" : picturepage,
                "freepage" : freepage,
                }
            if session_id : 
                dto = Member.objects.get(nickname = session_id)
                context["user"] = dto
            else:
                session_id = "None"
                
            
            return HttpResponse(template.render(context, request))
        
        else:
            return redirect("kakao:main")
    # def post(self, request):
    #     template = loader.get_template("general_search.html")
    #     session_id = request.session.get("nickname")
    #
    #
    #     ads = Adboard.objects.all().filter(accept=True)
    #
    #     adlist = []
    #     for i in ads:
    #         adlist.append(i)
    #
    #     ad_random=random.choice(adlist)
    #
    #     searchkey = request.POST.get("general_search")
    #
    #
    #     if searchkey:
    #         logger.info(str(session_id)+"*이,"+str(searchkey)+",전체검색")
    #         musics = Board.objects.filter(Q(board_name='Music', title__icontains=searchkey) | Q(board_name='Music', substance__icontains=searchkey)| Q(board_name='Music', writer__nickname__icontains=searchkey)).order_by("-write_dttm")
    #         pictures = Board.objects.filter(Q(board_name='Picture', title__icontains=searchkey) | Q(board_name='Picture', substance__icontains=searchkey)| Q(board_name='Picture', writer__nickname__icontains=searchkey)).order_by("-write_dttm")
    #         frees = Board.objects.filter(Q(board_name='Free', title__icontains=searchkey) | Q(board_name='Free', substance__icontains=searchkey)| Q(board_name='Free', writer__nickname__icontains=searchkey)).order_by("-write_dttm")
    #
    #         musicpage = request.GET.get('musicpage', '1')
    #         musicpaginator = Paginator(musics, 5)
    #         musicpage_obj = musicpaginator.get_page(musicpage)
    #
    #         picturepage = request.GET.get('picturepage', '1')
    #         picturepaginator = Paginator(pictures, 8)
    #         picturepage_obj = picturepaginator.get_page(picturepage)
    #
    #         freepage = request.GET.get('freepage', '1')
    #         freepaginator = Paginator(frees, 5)
    #         freepage_obj = freepaginator.get_page(freepage)
    #
    #         #dto = Member.objects.get(nickname = session_id)
    #
    #         context={
    #             "ad_random" : ad_random,
    #             "musicpage_obj" : musicpage_obj,
    #             "picturepage_obj" : picturepage_obj,
    #             "freepage_obj" : freepage_obj,
    #             "session_id" : session_id,
    #             }
    #         if session_id : 
    #             dto = Member.objects.get(nickname = session_id)
    #             context["user"] = dto
    #         else:
    #             session_id = "None"
    #
    #
    #         return HttpResponse(template.render(context, request))
    #
    #     else:
    #         return redirect("kakao:main")
#로그아웃    
#POST /v1/user/logout HTTP/1.1
#Host: kapi.kakao.com
#Authorization: Bearer ${ACCESS_TOKEN}/KakaoAK ${APP_ADMIN_KEY}
'''
사용자 액세스 토큰과 리프레시 토큰을 모두 만료시킵니다. 
사용자가 서비스에서 로그아웃할 때 이 API를 호출하여 더 이상 해당 사용자의 정보로 카카오 API를 호출할 수 없도록 합니다. 
로그아웃은 요청 방법에 따라 다음과 같이 동작합니다.

액세스 토큰으로 요청
해당 액세스 토큰만 만료 처리
만료된 액세스 토큰을 사용하는 모든 기기에서 로그아웃됨
어드민 키로 요청
해당 사용자의 모든 토큰 만료 처리
모든 기기에서 로그아웃됨
로그아웃 요청 성공 시, 응답 코드와 로그아웃된 사용자의 회원번호를 받습니다. 
로그아웃 시에도 웹 브라우저의 카카오계정 세션은 만료되지 않고, 로그아웃을 호출한 앱의 토큰만 만료됩니다. 
따라서 웹 브라우저의 카카오계정 로그인 상태는 로그아웃을 호출해도 유지됩니다. 로그아웃 후에는 서비스 초기 화면으로 리다이렉트하는 등 후속 조치를 취하도록 합니다.
'''
#카카오 계정과 함께 로그아웃
#GET /oauth/logout?client_id=${REST_API_KEY}&logout_redirect_uri=${LOGOUT_REDIRECT_URI} HTTP/1.1
#Host: kauth.kakao.com