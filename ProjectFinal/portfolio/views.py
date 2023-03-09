from django.shortcuts import render
from django.views.generic.base import View
from kakao.models import Member
from board.models import Board
import logging
from kakao.decorators import login_required
from django.utils.decorators import method_decorator
logger = logging.getLogger(__name__)


class PortfolioView(View):
    def get(self, request):
        user_name = request.GET['user_name']
        nickname = request.session.get('nickname')
        user_info = Member.objects.get(nickname=user_name)
        logger.info(str(nickname) +"*이"+str(user_info)+"의포트폴리오방문")
        ms_board_post = Board.objects.filter(writer=user_info, board_name='Music').order_by('-write_dttm')
        pc_board_post = Board.objects.filter(writer=user_info, board_name='Picture').order_by('-write_dttm')
        login_session = request.session.get('nickname', '')
        pc_follow = Board.objects.filter(follow=user_info, board_name='Picture').order_by('-write_dttm')
        ms_follow = Board.objects.filter(follow=user_info, board_name='Music').order_by('-write_dttm')
        
        context = {
            'user_name' : user_name,
            "nickname" : nickname,
            'user_info' : user_info,
            'ms_board_post' : ms_board_post,
            'pc_board_post' : pc_board_post,
            'login_session' : login_session,
            'pc_follow' : pc_follow,
            'ms_follow' : ms_follow,
            }
        
        return render(request, 'portfolio.html', context)
    
        
        
        