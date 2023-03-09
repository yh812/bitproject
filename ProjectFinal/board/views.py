from django.shortcuts import render, redirect, get_object_or_404
from board.forms import CommentForm, ReCommentForm
from board.models import Board, Adboard, Comment, ReComment, Report_board,\
    Report_ReComment, Report_Comment, Notice
from kakao.models import Member
from kakao.decorators import login_required
from django.core.paginator import Paginator
import board
import os
from django.conf import settings
from django.http.response import HttpResponse
from django.views.generic.base import View
import logging
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from django.utils.dateformat import DateFormat
from django.template.defaulttags import comment

#added import
from django.views.generic.edit import FormView
import json
import random

logger = logging.getLogger( __name__ )

#############################자유게시판 새글 작성################################
class board_write(View):
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request) :
        template = loader.get_template( "bwrite.html" )
        session_id = request.session.get('nickname', '')
        
        if session_id : 
            dto = Member.objects.get(nickname=session_id)
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            context = {
                "session_id" : session_id,
                "ad_random" : ad_random,
                "dto" : dto
                }
            return HttpResponse(template.render(context, request))
        else:
            return redirect("/kakao/login")
    
    def post(self, request ) :
        session_id=request.session.get('nickname','')
        writer= Member.objects.get(nickname=session_id)
        contents = request.POST.get("contents")
        files = request.FILES.get('files')
        hits = request.POST.get("update_counter")
        write_dttm = request.POST.get("created_string")
        dtos = Member.objects.get(nickname=session_id)
        dtos.user_total_point +=10
        dtos.user_current_point +=10
        title = request.POST.get('title')
        
        if not title:
            return redirect("board:bwrite")
        else:
            dto = Board(
                    writer = writer,
                    contents = contents,
                    title = request.POST["title"],
                    files=files,
                    board_name = 'Free',
                    write_dttm = write_dttm
                    );
            dto.save()
            logger.info(session_id+"*이," + dto.board_name+",게시판종류,글작성")
            return redirect( "kakao:free" )

class board_detail(View):
    def get(self, request, pk ) :
        template = loader.get_template( "board_detail.html" )
        login_session = request.session.get('nickname') #현재 로그인한 아이디의 닉네임
        
        if login_session :
            user= Member.objects.get(nickname=login_session)
            dto = Board.objects.get( id=pk ) # 게시글 번호 맞춰 데이터 들고오기
            writeuser = Member.objects.get(nickname=dto.writer.nickname)
            comment_form=CommentForm() # 댓글 폼 가져오기
            recom_form=ReCommentForm() # 대댓글 폼 가져오기
            comment_dto = Comment.objects.filter(post=pk)
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random=random.choice(adlist)
            
            if str(login_session) == str(dto.writer): 
                Gorani= True
            else:
                Gorani= False
            
            logger.info(login_session+"*이,"+str(dto.board_name)+",게시판종류,"+str(dto.id)+",게시글번호," +str(dto.category)+",카테고리")
            context = {
                "dto" : dto, 
                'Gorani':Gorani, # 로그인한 사람이랑 로그인 세션값 비교할때 쓰는 boolean값임
                'user':user,    
                'comment_form':comment_form ,
                'recom_form':recom_form, 
                'comment_dto':comment_dto,
                "session_id" : login_session,
                "ad_random":ad_random,
                "writeuser" : writeuser,
                }
            return HttpResponse( template.render( context, request ) )
        else:
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            
            comment_form = CommentForm()
            recom_form=ReCommentForm()
            dto = Board.objects.get( id=pk )
            writeuser = Member.objects.get(nickname=dto.writer.nickname)
            context = { 
                "ad_random" : ad_random,
                "comment_form" : comment_form, 
                "recom_form" : recom_form,
                "user" : login_session,
                "dto":dto,
                "writeuser" : writeuser,
                }
            if dto.writer.nickname == login_session:
                context['writer'] = True
                
            else:
                context['writer'] = False
                  
            context['dto'] = dto
            response =  render(request, 'board_detail.html', context)
            return response
        
    def post(self, request,pk ) :           
        dto = Board.objects.get( id=pk )
        
        template = loader.get_template( "bmodify.html" )
        context = {
            "dto" : dto,
            }
        return HttpResponse( template.render( context, request ) )
    
class board_delete(View):
    def get(self,request,pk):
        login_session = request.session.get('nickname')
        board = get_object_or_404(Board, id=pk)
        if board.writer.nickname == login_session:
            logger.info(str(login_session)+"*이," + str(board.board_name)+",게시판종류,"+ str(board.id)+",게시글번호,삭제")
            board.delete()
            if board.board_name == 'Free':
                return redirect('/kakao/free')
            elif board.board_name == 'Picture':
                return redirect('/kakao/paint')
            elif board.board_name == 'Music':
                return redirect('/kakao/music')
            
        else:
            return redirect('/board/detail/'+str(pk))

class board_modify(View):
    ######### css 적용하기 ##########
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request,pk ) :
        template = loader.get_template( "bmodify.html" )
        dto = Board.objects.get(id=pk)
        session_id = request.session.get("nickname")
        user = Member.objects.get(nickname = session_id)
        ads = Adboard.objects.all().filter(accept=True)
        adlist=[]
        for i in ads:
            adlist.append(i)
        ad_random = random.choice(adlist)
        context={
            "dto" : dto,
            "session_id" : session_id,
            "user" : user,
            "ad_random" : ad_random
            }
        return HttpResponse( template.render( context, request ) )

    def post(self, request,pk ) :
        login_session = request.session.get("nickname")
        dto = Board.objects.get( id=pk )
        dto.title=request.POST['title']
        dto.contents=request.POST['contents']
        dto.files=request.POST['files']
        logger.info(login_session+"*이," + dto.board_name+",게시판종류,"+ str(dto.id)+",게시글번호,수정")   
        dto.save()
        return redirect( "kakao:free" )
##############################################################################    


############### 그림 게시판 새글 작성 & 세부사항 & 수정 ###########################
class BoardWriteView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request) :
        ###글쓰기 페이지###
        template = loader.get_template("board/pc_board_write.html")
        session_id = request.session.get('nickname', '')
        if session_id : 
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            dto = Member.objects.get(nickname=session_id)
            context = {
                "session_id" : session_id,
                "ad_random" : ad_random,
                "login_session" : session_id,
                "dto":dto
                }
            return HttpResponse(template.render(context, request))
        else:
            return redirect("/kakao/login")
        
    def post(self, request):
        login_session = request.session.get('nickname', '')
        writer = Member.objects.get(nickname=login_session)
        contents = request.POST.get("contents")
        files = request.FILES.get('files')
        filename = files.name
        title = request.POST.get("title")
        category = request.POST.get("category")
        
        if title=="":
            return redirect("board:pc_board_write")
        board = Board(
            title=request.POST.get("title"),
            contents = contents,
            substance = request.POST.get("substance"),
            writer=writer,
            files=files,
            filename = filename,
            board_name = "Picture",
            category = category,
            )
        logger.info(login_session+"*이," + board.board_name+",게시판종류,"+board.category+",카테고리,글작성")
        board.save()
        return redirect('/kakao/paint')

class BoarddetailView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        num = request.GET['num']
        login_session = request.session.get('nickname')
        if login_session : 
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            
            
            comment_form = CommentForm()
            recom_form=ReCommentForm()
            context = { 
                'session_id': login_session,
                'num' : num,
                "ad_random" : ad_random,
                "comment_form" : comment_form, 
                "recom_form" : recom_form,
                }
            if not login_session == "":
                user = Member.objects.get(nickname=login_session)
                context['user'] = user
            board = get_object_or_404(Board, id=num)
            writeuser = Member.objects.get(nickname=board.writer.nickname)
            context['writeuser'] = writeuser
            if board.writer.nickname == login_session:
                context['writer'] = True
                
            else:
                context['writer'] = False
                
            context['board'] = board
            logger.info(login_session+"*이,"+str(board.board_name)+",게시판종류," +str(board.id)+",게시글번호," + str(board.category)+",카테고리")
            response =  render(request, 'board/pc_board_detail.html', context)
            return response
        else : 
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            
            comment_form = CommentForm()
            recom_form=ReCommentForm()
            context = { 
                'session_id': login_session,
                'num' : num,
                "ad_random" : ad_random,
                "comment_form" : comment_form, 
                "recom_form" : recom_form,
                "user" : login_session,
                }
            board = get_object_or_404(Board, id=num)
            writeuser = Member.objects.get(nickname=board.writer.nickname)
            context['writeuser'] = writeuser
            if board.writer.nickname == login_session:
                context['writer'] = True
            else:
                context['writer'] = False 
            context['board'] = board
            response =  render(request, 'board/pc_board_detail.html', context)
            return response
        
    def post(self):
        pass

class BoardmodifyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request) :
        login_session = request.session.get('nickname')
        if login_session : 
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            template = loader.get_template("board/pc_board_modify.html")
            num = request.GET["num"]
            dto = Board.objects.get(id = num)
            user = Member.objects.get(nickname = login_session)
            context = {
                "num" : num,
                "dto" : dto,
                "ad_random" : ad_random,
                "user":user,
                "session_id" : login_session
                }
            return HttpResponse(template.render(context, request))
        else : 
            return redirect("/kakao/login")
    
    
    def post(self, request):
        login_session = request.session.get('userid', '')
        writer = Member.objects.get(userid=login_session)
        contents = request.POST.get("contents")
        files = request.FILES.get('files')
        filename = files.name
        pk = request.POST["num"]
        dto = get_object_or_404(Board, id=pk)
        dto.title=request.POST["title"]
        dto.contents = contents
        dto.substance = request.POST.get("substance")
        dto.writer=writer
        dto.files=files
        dto.filename = filename
        dto.board_name = "Picture"
        dto.category = request.POST.get("category")
        logger.info(login_session+"*이," + dto.board_name+",게시판종류,"+ str(dto.id)+",게시글번호,수정,"+ dto.category+",카테고리")
        dto.save()
        return redirect('/kakao/paint')
###########################################################################

###########################파일 다운로드####################################
def file_download(request):
    path = request.GET['path']
    print(path)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    file_path = file_path.encode('utf-8')
    nickname = request.session.get('nickname')
    if file_path:
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = b'files; filename=' + os.path.basename(file_path)
        # filesname = files
        board = Board.objects.get(files=path)
        logger.info(str(nickname)+"*이,게시판종류,"+str(board.id)+",게시글번호,"+str(file_path)+",를다운로드")
        return response
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()</script>")
############################################################################3

###################음악 게시판 작성 & 세부내용 & 수정##################################
class MusicWriteView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request) :
        ###글쓰기 페이지###
        template = loader.get_template("board/ms_board_write.html")
        session_id = request.session.get('nickname', '')
        if session_id:
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            user = Member.objects.get(nickname = session_id)
            context = {
                "session_id" : session_id,
                "ad_random" : ad_random,
                "user":user
                }
            if not session_id == "":
                user = Member.objects.get(nickname=session_id)
                context['user'] = user
            return HttpResponse(template.render(context, request))
        else:
            return redirect("kakao:login")
        
    def post(self, request):
        login_session = request.session.get('userid', '')
        writer = Member.objects.get(userid=login_session)
        contents = request.POST.get("contents")
        files = request.FILES.get('files')
        filename = files.name
        category = request.POST.get("category")
        title = request.POST.get("title")
        if not title:
            return redirect("board:ms_board_write")
        board = Board(
            title=request.POST.get("title"),
            contents = contents,
            substance = request.POST.get("substance"),
            writer=writer,
            files=files,
            filename = filename,
            board_name = "Music",
            category = category,
            )
        logger.info(str(login_session)+"*이," + board.board_name+",게시판종류,"+board.category+",카테고리,글작성")
        board.save()
        return redirect('/kakao/music')
     
class MusicDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request):
        num = request.GET['num']
        login_session = request.session.get('nickname', '')
        ads = Adboard.objects.all().filter(accept=True)
        adlist=[]
        for i in ads:
            adlist.append(i)
        ad_random = random.choice(adlist)
        
        comment_form = CommentForm()
        recom_form = ReCommentForm()
        userid = request.session.get('userid')
        if login_session:
            user = Member.objects.get(userid = userid)
            context = { 
                'session_id': login_session,
                'num' : num,
                "ad_random" : ad_random,
                "comment_form" : comment_form,
                "recom_form" : recom_form,
                "user":user,
                }
            
            board = get_object_or_404(Board, id=num)
            writeuser = Member.objects.get(nickname=board.writer.nickname)
            context['writeuser'] = writeuser
            if board.writer.nickname == login_session:
                context['writer'] = True
            else:
                context['writer'] = False    
            context['board'] = board
            
            logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류," +str(board.id)+",게시글번호,"+str(board.category)+",카테고리" )
            return  render(request, 'board/ms_board_detail.html', context)
        else:
            context = { 
                'session_id': login_session,
                'num' : num,
                "ad_random" : ad_random,
                "comment_form" : comment_form,
                "recom_form" : recom_form,
                "user":login_session,
                }
            board = get_object_or_404(Board, id=num)
            writeuser = Member.objects.get(nickname=board.writer.nickname)
            context['writeuser'] = writeuser
            if board.writer.userid == login_session:
                context['writer'] = True
            else:
                context['writer'] = False    
            context['board'] = board
            return  render(request, 'board/ms_board_detail.html', context)
        
    def post(self, request):
        pass
   
class MusicModifyView(View):
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request) :
        template = loader.get_template("board/ms_board_modify.html")
        session_id = request.session.get("nickname",'')
        if session_id :
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random=random.choice(adlist)
            num = request.GET["num"]
            dto = Board.objects.get(id = num)
            user = Member.objects.get(nickname=session_id)
            context = {
                "session_id":session_id,
                "num" : num,
                "dto" : dto,
                "ad_random" : ad_random,
                "user":user
                }
            return HttpResponse(template.render(context, request))
        else:
            return redirect("/kakao/login")
    
    def post(self, request):
        login_session = request.session.get('userid', '')
        writer = Member.objects.get(userid=login_session)
        contents = request.POST.get("contents")
        files = request.FILES.get('files')
        filename = files.name
        pk = request.POST["num"]
        dto = get_object_or_404(Board, id=pk)
        dto.title=request.POST["title"]
        dto.contents = contents
        dto.substance = request.POST.get("substance")
        dto.writer=writer
        dto.files=files
        dto.filename = filename
        dto.board_name = "Music"
        dto.category = request.POST.get("category")
        dto.save()
        logger.info(str(login_session)+"*이," + str(dto.board_name)+",게시판종류,"+ str(dto.id)+",게시글번호,수정,"+ str(dto.category)+",카테고리")
        return redirect('/kakao/music')
#############################################################################

#############################광고 게시판 새글 작성#################################
class adboard_write(View):
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request ) :
        template = loader.get_template( "adwrite.html" )
        session_id=request.session.get('nickname','')
        
        if session_id : 
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            dto = Member.objects.get(nickname = session_id)
            context = {
                "session_id" : session_id,
                "ad_random" : ad_random,
                "dto":dto
                }
            return HttpResponse(template.render(context, request))
        else:
            return redirect("/kakao/login")
    
    def post(self, request ) :
        session_id=request.session.get('nickname','')
        dtos = Member.objects.get(nickname=session_id)
        dtos.user_current_point -= 1000
        dtos.save()
        writer= Member.objects.get(nickname=session_id)
        contents = request.POST.get("contents")
        images= request.FILES.get('images')
        adurl= request.POST.get("adurl")
        dto = Adboard(
                writer = writer,
                contents = contents,
                title = request.POST["title"],
                write_dttm = DateFormat( datetime.now() ).format( "Y-m-d" ),
                images=images,
                board_name = 'Ad',
                id = request.POST.get("id"),
                adurl=adurl
                );
        logger.info(str(session_id)+"*이,"+ str(dto.board_name)+",게시판종류,글작성")
        dto.save()
        return redirect( "kakao:advertise" )
    
class adboard_detail(View):
    def get(self, request, pk ) :
        template = loader.get_template( "addetail.html" )
        login_session = request.session.get('nickname') #현재 로그인한 아이디의 닉네임
        dto = Adboard.objects.get(id=pk ) # 게시글 번호 맞춰 데이터 들고오기
        ads = Adboard.objects.all().filter(accept=True)
        adlist=[]
        for i in ads:
            adlist.append(i)
        ad_random = random.choice(adlist)
        if str(login_session) == str(dto.writer): 
            Gorani= True
        else:
            Gorani= False
        if login_session:
            user= Member.objects.get(nickname=login_session)
            logger.info(str(login_session)+"*이,"+ str(dto.board_name)+",게시판종류,"+str(dto.id)+",게시글번호,디테일확인")
            context = {
                "dto" : dto, 
                'Gorani':Gorani, # 로그인한 사람이랑 로그인 세션값 비교할때 쓰는 boolean값임
                'user':user,
                "ad_random" : ad_random,
                "session_id" : login_session
                }
            return HttpResponse( template.render( context, request ) )
        # 로그인세션없을경우 오류떠서 수정
        else:
            context = {
                "dto" : dto, 
                'Gorani':Gorani, # 로그인한 사람이랑 로그인 세션값 비교할때 쓰는 boolean값임
                "ad_random" : ad_random,
                "session_id" : login_session
                }
            return HttpResponse( template.render( context, request ) )
    def post(self, request,pk ) :         
        dto = Adboard.objects.get(id = pk )
        
        template = loader.get_template( "admodify.html" )
        context = {
            "dto" : dto,
            }
        return HttpResponse( template.render( context, request ) )
###########################################################################

###################### 신고 ##############################
#게시글 신고
class board_report(View):
    @method_decorator( csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    
    def get(self, request,pk ) :
        template = loader.get_template( "breport.html" )
        dto = Board.objects.get( id=pk )
        login_session = request.session.get('nickname')
        report = Report_board(
                report_user = dto.writer,
                report_post = get_object_or_404(Board,pk=pk),
                report_reason = request.GET.get("Gorani"),
                report_date = DateFormat( datetime.now() ).format( "Ymd" ),
                report_detail=request.GET.get('Detail'),
                reported_user = login_session
                );
        if report.report_reason ==None:
            pass
        else:
            logger.info(str(login_session)+"*이,"+str(dto.board_name)+",게시판종류,"+str(dto.id)+",게시글번호," +str(dto.category)+",카테고리," + "신고")
            report.save()
        context={
            'dto':dto,
            'login_session':login_session,
            }
        return HttpResponse( template.render( context, request ) )

    def post(self, request,pk ) :
        dto = Board.objects.get( id=pk )
        
        report = Report_board(
                report_user = dto.writer,
                report_post = get_object_or_404(Board,pk=pk),
                report_reason = request.POST["Gorani"],
                report_date = DateFormat( datetime.now() ).format( "Ymd" ),
                report_detail=request.POST['Detail'],
                );
        report.save()
        
        if dto.board_name == 'Free':
            return redirect('/board/detail/'+str(pk),pk)
        elif dto.board_name == 'Picture':
            return redirect('/board/pc_board_detail?num='+str(pk),pk)
        elif dto.board_name == 'Music':
            return redirect('/board/ms_board_detail?num='+str(pk),pk)
        else:
            return redirect('/board/detail/'+str(pk),pk)

#댓글 신고

class comment_report(View):
    @method_decorator( csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request,pk,comment_id ) :
        template = loader.get_template( "bcomment_report.html" )
        dto = Comment.objects.get( id=comment_id )
        board=Board.objects.get(pk=pk)
        login_session = request.session.get('nickname')
        report = Report_Comment(
                comment_reported_user = dto.writer,
                comment_report_post = get_object_or_404(Comment,id=comment_id),
                comment_report_reason = request.GET.get("Gorani"),
                comment_report_date = DateFormat( datetime.now() ).format( "Ymd" ),
                comment_report_detail=request.GET.get('Detail'),
                comment_report_user = login_session
                );
        if report.comment_report_reason ==None:
            pass
        else:
            report.save()
            logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류," +str(board.id)+",게시글번호,"+str(board.category)+",카테고리,"+str(dto.writer)+",댓글작성자,"+str(dto.id)+",댓글번호신고" )
        context={
            'dto':dto,
            'login_session':login_session,
            'board':board
            }
        return HttpResponse( template.render( context, request ) )

    def post(self, request,pk,comment_id ) :
        dto = Board.objects.get( id=pk )
        
        report = Report_board(
                comment_report_user = dto.writer,
                comment_report_post = get_object_or_404(Board,pk=pk),
                comment_report_reason = request.POST["Gorani"],
                comment_report_date = DateFormat( datetime.now() ).format( "Ymd" ),
                comment_report_detail=request.POST['Detail'],
                );
        report.save()
        if dto.board_name == 'Free':
            return redirect('/board/detail/'+str(pk),pk)
        elif dto.board_name == 'Picture':
            return redirect('/board/pc_board_detail?num='+str(pk),pk)
        elif dto.board_name == 'Music':
            return redirect('/board/ms_board_detail?num='+str(pk),pk)
        else:
            return redirect('/board/detail/'+str(pk),pk)

#대댓글 신고

class recomment_report(View):
    @method_decorator( csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request,pk,comment_id,recomment_id ) :
        
        template = loader.get_template( "brecomment_report.html" )
        dtos = ReComment.objects.get( id=recomment_id )
        dto=Comment.objects.get(id=comment_id)
        board=Board.objects.get(id=pk)
        login_session = request.session.get('nickname')
        report = Report_ReComment(
                recomment_reported_user = dtos.writer,
                recomment_report_post = get_object_or_404(Comment,id=comment_id),
                recomment_report_reason = request.GET.get("Gorani"),
                recomment_report_date = DateFormat( datetime.now() ).format( "Ymd" ),
                recomment_report_detail=request.GET.get('Detail'),
                recomment_report_user = login_session
                );
        if report.recomment_report_reason ==None:
            pass
        else:
            logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류," +str(board.id)+",게시글번호,"+str(board.category)+",카테고리,"+str(board.writer)+",의 게시물,"+str(dto.writer)+",댓글작성자,"+str(dto.id)+",댓글번호," +str(dtos.writer)+",대댓글작성자,"+str(dtos.id)+",대댓글번호신고")
            report.save()
        context={
            'dtos':dtos,
            'dto':dto,
            'login_session':login_session,
            'board':board
            }
        return HttpResponse( template.render( context, request ) )

    def post(self, request,pk,comment_id,recomment_id ) :
        dto = Board.objects.get( id=pk )
        report = Report_board(
                recomment_report_user = dto.writer,
                recomment_report_post = get_object_or_404(Board,pk=pk),
                recomment_report_reason = request.POST["Gorani"],
                recomment_report_date = DateFormat( datetime.now() ).format( "Ymd" ),
                recomment_report_detail=request.POST['Detail'],
                );
        report.save()
        if dto.board_name == 'Free':
            return redirect('/board/detail/'+str(pk),pk)
        elif dto.board_name == 'Picture':
            return redirect('/board/pc_board_detail?num='+str(pk),pk)
        elif dto.board_name == 'Music':
            return redirect('/board/ms_board_detail?num='+str(pk),pk)
        else:
            return redirect('/board/detail/'+str(pk),pk)
##################################################################################

###################### 댓글 ####################################
@login_required
def create_comment(request,pk):    
    login_session = request.session.get('nickname') #현재 로그인한 아이디 닉네임
    filled_form=CommentForm(request.POST)
    user= Member.objects.get(nickname=login_session)
    board = get_object_or_404(Board, id=pk)
    session_id=request.session.get('nickname','')
    dtos = Member.objects.get(nickname=session_id)
    dtos.user_total_point +=3
    dtos.user_current_point +=3
    dtos.save()
    logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+str(board.id)+",게시글번호,댓글작성,"+str(board.category)+",카테고리," + "댓글")
    
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Board,pk=pk)
        finished_form.writer= user  
        finished_form.save()
    
    if board.board_name == 'Free':
        return redirect('/board/detail/'+str(pk),pk)
    elif board.board_name == 'Picture':
        return redirect('/board/pc_board_detail?num='+str(pk),pk)
    elif board.board_name == 'Music':
        return redirect('/board/ms_board_detail?num='+str(pk),pk)
    else:
        return redirect('/board/detail/'+str(pk),pk)


@login_required
def comment_delete(request,pk,comment_id):
    board = get_object_or_404(Board, id=pk)
    login_session = request.session.get('nickname') #현재 로그인한 아이디 닉네임
    user= Member.objects.get(nickname=login_session) 
    user.user_total_point -=3
    user.user_current_point -=3
    user.save()
    mycom =Comment.objects.get(id=comment_id) # 댓글 번호와 내용
    logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+str(board.id)+",게시글번호,"+str(board.category)+",카테고리,"+str(mycom.id)+",댓글번호,"+str(mycom.post)+",의댓글삭제")
    mycom.delete()
    if board.board_name == 'Free':
        return redirect('/board/detail/'+str(pk),pk)
    elif board.board_name == 'Picture':
        return redirect('/board/pc_board_detail?num='+str(pk),pk)
    elif board.board_name == 'Music':
        return redirect('/board/ms_board_detail?num='+str(pk),pk)
    else:
        return redirect('/board/detail/'+str(pk),pk)
##################################################################

###################### 대댓글 ####################################
@login_required
def comment_recomment(request,pk,comment_id):
    login_session = request.session.get('nickname') # 현재 로그인한 아이디 닉네임
    user= Member.objects.get(nickname=login_session) 
    user.user_total_point +=3
    user.user_current_point +=3
    user.save()
    board = get_object_or_404(Board, id=pk)
    logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+str(board.id)+",게시글번호," +str(board.category)+",카테고리" +",대댓글")
    filled_form= ReCommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.writer=user
        finished_form.save()
        
    # logger.info(filled_form.writer)
    
    if board.board_name == 'Free':
        return redirect('/board/detail/'+str(pk),pk)
    elif board.board_name == 'Picture':
        return redirect('/board/pc_board_detail?num='+str(pk),pk)
    elif board.board_name == 'Music':
        return redirect('/board/ms_board_detail?num='+str(pk),pk)
    else:
        return redirect('/board/detail/'+str(pk),pk)

@login_required
def comment_recommentdel(request,pk,comment_id,recomment_id): 
    board = get_object_or_404(Board, id=pk) 
    login_session = request.session.get('nickname') # 현재 로그인한 아이디 닉네임
    user= Member.objects.get(nickname=login_session) 
    user.user_total_point -=3
    user.user_current_point -=3
    user.save()
    mycom =ReComment.objects.get(id=recomment_id) # 댓글 번호와 내용
    logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+str(board.id)+",게시글번호,"+str(board.category)+",카테고리,"+str(mycom.id)+",대댓글번호,"+str(mycom.comment)+",댓글의대댓글삭제" )
    mycom.delete()
    


    if board.board_name == 'Free':
        return redirect('/board/detail/'+str(pk),pk)
    elif board.board_name == 'Picture':
        return redirect('/board/pc_board_detail?num='+str(pk),pk)
    elif board.board_name == 'Music':
        return redirect('/board/ms_board_detail?num='+str(pk),pk)
    else:
        return redirect('/board/detail/'+str(pk),pk)
##################################################################

##################### 좋아요(추천) & 싫어요(비추천)##############################


def likes(request, pk):
    login_session = request.session.get('nickname')

    board= get_object_or_404(Board,id=pk)

    if board.like.filter(nickname=login_session).exists():
        logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+ str(board.id)+",게시글번호,좋아요취소," +str(board.category)+",카테고리")
        board.like.remove(Member.objects.get(nickname=login_session))
        board.like_count -= 1
        board.save()
    else:
        logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+ str(board.id)+",게시글번호,좋아요," +str(board.category)+",카테고리")
        board.like.add(Member.objects.get(nickname=login_session))
        board.like_count += 1
        board.save()
    context = {'like_count' : board.like_count}    
    return HttpResponse(json.dumps(context), content_type='application/json')


def dislikes(request, pk):
    login_session = request.session.get('nickname')
    board= get_object_or_404(Board,id=pk)    
    
    if board.dislike.filter(nickname=login_session).exists(): # 데이터베이스에 현재 로그인한 아이디 닉네임값이 있으면 == 싫어요를 이미 누른사람이 있다면
        logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+ str(board.id)+",게시글번호,싫어요취소," +str(board.category)+",카테고리")
        board.dislike.remove(Member.objects.get(nickname=login_session))
        board.dislike_count -= 1
        board.save()
    else:
        logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+ str(board.id)+",게시글번호,싫어요," +str(board.category)+",카테고리")        
        board.dislike.add(Member.objects.get(nickname=login_session))
        board.dislike_count += 1
        board.save()
    
    context = {'dislike_count' : board.dislike_count}    
    return HttpResponse(json.dumps(context), content_type='application/json')
#################################################################

##################### 팔로우(찜) ##############################

def follow(request, pk):
    login_session = request.session.get('nickname')
    
    board= get_object_or_404(Board,id=pk)
    if board.follow.filter(nickname=login_session).exists():
        logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+ str(board.id)+",게시글번호,찜해제," +str(board.category)+",카테고리")
        board.follow.remove(Member.objects.get(nickname=login_session))
        board.follow_count -= 1
        board.save()
        
    else :
        logger.info(str(login_session)+"*이,"+str(board.board_name)+",게시판종류,"+ str(board.id)+",게시글번호,찜," +str(board.category)+",카테고리")
        board.follow.add(Member.objects.get(nickname=login_session))
        board.follow_count += 1
        board.save()     
    context = {'follow_count' : board.follow_count}    
    return HttpResponse(json.dumps(context), content_type='application/json')
#######################################################################
class notice_detail(View):
    def get(self, request, pk ) :
        template = loader.get_template( "notice_detail.html" )
        login_session = request.session.get('nickname') #현재 로그인한 아이디의 닉네임
        if login_session :
            user= Member.objects.get(nickname=login_session)
            dto = Notice.objects.get( id=pk ) # 게시글 번호 맞춰 데이터 들고오기
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random=random.choice(adlist)
            
            if str(login_session) == str(dto.writer): 
                Gorani= True
            else:
                Gorani= False
            logger.info(str(login_session)+"*이,"+"notice"+",게시판종류," +str(dto.id)+ ",게시글번호,공지글확인")
            context = {
                "dto" : dto, 
                'Gorani':Gorani, # 로그인한 사람이랑 로그인 세션값 비교할때 쓰는 boolean값임
                'user':user,    
                "session_id" : login_session,
                "ad_random":ad_random
                }
            return HttpResponse( template.render( context, request ) )
        else:
            ads = Adboard.objects.all().filter(accept=True)
            adlist=[]
            for i in ads:
                adlist.append(i)
            ad_random = random.choice(adlist)
            dto = Notice.objects.get( id=pk )
            context = { 
                "ad_random" : ad_random,
                "user" : login_session,
                "dto":dto,
                }
            if dto.writer.nickname == login_session:
                context['writer'] = True
            else:
                context['writer'] = False
            context['board'] = board
            response =  render(request, 'notice_detail.html', context)
            return response
        
    def post(self, request,pk ) :           
        dto = Notice.objects.get( id=pk )
        
        template = loader.get_template( "bmodify.html" )
        context = {
            "dto" : dto,
            }
        return HttpResponse( template.render( context, request ) )