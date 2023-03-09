from django.urls import path, include
from board import views


app_name = 'board'
urlpatterns = [
    #그림게시판 작성&세부내용&수정
        path('pc_board_write', views.BoardWriteView.as_view(), name='pc_board_write'),
        path('pc_board_detail', views.BoarddetailView.as_view(), name='pc_board_detail'),
        path('pc_board_modify', views.BoardmodifyView.as_view(), name='pc_board_modify'),
        
    #음악게시판 작성&세부내용&수정
        path('ms_board_write', views.MusicWriteView.as_view(), name='ms_board_write'),
        path('ms_board_detail', views.MusicDetailView.as_view(), name='ms_board_detail'),
        path('ms_board_modify', views.MusicModifyView.as_view(), name='ms_board_modify'),
        
    #자유게시판
        path('bwrite/', views.board_write.as_view(), name= 'bwrite'),
        path('detail/<int:pk>/', views.board_detail.as_view(), name='board_detail'),
        path('detail/<int:pk>/delete/', views.board_delete.as_view(), name='board_delete'),
        path('detail/<int:pk>/modify/', views.board_modify.as_view(), name='board_modify'),
        path('notice/<int:pk>/', views.notice_detail.as_view(), name='notice_detail'),
        
    #광고게시판
        path('adwrite/', views.adboard_write.as_view(), name= 'adwrite'),
        path('addetail/<int:pk>/', views.adboard_detail.as_view(), name='adboard_detail'),
    
    #파일 다운로드   
        path( "download/", views.file_download, name="file_download" ),
        
    #댓글 & 대댓글
        path('create_comment/<int:pk>/', views.create_comment, name='create_comment'),
        path('comment_delete/<int:pk>/<int:comment_id>', views.comment_delete, name='comment_delete'), 
        path('comment_recomment/<int:pk>/<int:comment_id>', views.comment_recomment, name='comment_recomment'),
        path('comment_recommentdel/<int:pk>/<int:comment_id>/<int:recomment_id>', views.comment_recommentdel, name='comment_recommentdel'),
    
    #좋아요 & 싫어요
        path('likes/<int:pk>/', views.likes, name="likes"),
        path('dislikes/<int:pk>/', views.dislikes, name="dislikes"),
    
    # 팔로우
        path('follow/<int:pk>/', views.follow, name="follow"),
    
    #신고
        path('detail/<int:pk>/report/', views.board_report.as_view(), name='board_report'),
        path('detail/<int:pk>/<int:comment_id>/comment_report/', views.comment_report.as_view(), name='comment_report'),
        path('detail/<int:pk>/<int:comment_id>/<int:recomment_id>/recomment_report/', views.recomment_report.as_view(), name='comment_report'),
    ]  