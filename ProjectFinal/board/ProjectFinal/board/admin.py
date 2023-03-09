from django.contrib import admin
from .models import Board
from django_summernote.admin import SummernoteModelAdmin
from board.models import Comment, ReComment, Report_board, Adboard,\
    Report_Comment, Report_ReComment, Notice, Recom


@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'title',
        'writer',
        'board_name',
        'hits',
        'write_dttm',
        'update_dttm',
        'files',
        'category',
        )
    search_fields = ['title', 'writer__nickname', 'board_name']
 
    list_display_links = list_display
    
    
admin.site.register(Comment)
admin.site.register(ReComment)
@admin.register(Report_board)
class Report_board(admin.ModelAdmin):
    list_display = ['reported_user','report_user','report_reason', 'report_post','report_date' ] 
    
@admin.register(Adboard)
class Adboard(admin.ModelAdmin):
    list_display = ['title',
    'contents',
    'writer',
    'board_name',
    'images',
    'accept',
    'adurl',
    ]
    search_fields = ['title', 'writer__nickname']

@admin.register(Report_Comment)
class Report_Comment(admin.ModelAdmin):
    list_display = ['comment_report_user','comment_reported_user','comment_report_reason', 'comment_report_post','comment_report_date' ]
    
@admin.register(Report_ReComment)
class Report_ReComment(admin.ModelAdmin):
    list_display = ['recomment_report_user','recomment_reported_user','recomment_report_reason', 'recomment_report_post','recomment_report_date' ]
    
@admin.register(Notice)
class Notice(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('contents',)
    list_display = ['title', 'contents', 'writer', 'write_dttm']
    
@admin.register(Recom)
class Recom(admin.ModelAdmin):
    list_display = [
        'user_nickname',
        'recom_board1', 
        'recom_board2',
        'recom_board3', 
        'recom_board4',
        'recom_board5',
        'recom_board6',
        'recom_board7',
        'recom_board8', 
        'recom_board9', 
        'recom_board10', 
        'recom_board11',
        'recom_board12',  
        'recom_board13', 
        'recom_board14', 
        'recom_board15', 
        'recom_board16', 
        'recom_board17', 
        'recom_board18', 
        'recom_board19', 
        'recom_board20' 
    ]
    search_fields = ['title', 'writer__nickname']
      