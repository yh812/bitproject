from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from kakao.models import Member
import os
from datetime import datetime
from uuid import uuid4

#시간 계산
from django.utils import timezone
from datetime import datetime, timedelta

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    return '/'.join(['upload_file/', ymd_path, filename])

class Board(models.Model):
    #글
    title = models.CharField(max_length=48, verbose_name='글 제목', null=True)
    contents = models.TextField(verbose_name='글 내용', null=True ,blank=True)
    substance = models.TextField(verbose_name="코멘트", null=True)
    writer = models.ForeignKey('kakao.Member', on_delete=models.CASCADE, verbose_name='작성자', related_name='write_board', null=True)
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='글 작성일', null=True)
    #게시판종류(글 분류)
    board_name = models.CharField(max_length=32, default='주크박스', verbose_name='게시판 종류')
    #글수정일
    update_dttm = models.DateTimeField(auto_now=True, verbose_name='최종 수정일')
    #조회수
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')
    #파일
    files = models.FileField( upload_to="media", null=True, blank=True, verbose_name='파일')
    filename = models.CharField(verbose_name="파일 이름", max_length=600, null=True) #삭제예정
    #광고부분->승인
    accept = models.BooleanField(default=False, verbose_name='광고 승인')
    #좋아요
    like = models.ManyToManyField(Member, related_name='likes',blank=True)
    like_count = models.PositiveIntegerField(default=0) #0또는 양수만 받는 필드
    #싫어요
    dislike = models.ManyToManyField(Member, related_name='dislikes',blank=True)
    dislike_count = models.PositiveIntegerField(default=0) #0또는 양수만 받는 필드
    #음악&그림 카테고리
    category = models.CharField(max_length=200, verbose_name='카테고리' , null=True)
    #찜
    follow = models.ManyToManyField(Member, related_name="follow" ,blank=True)
    follow_count = models.PositiveIntegerField(default=0) #0또는 양수만 받는 필드
    
    def get_filename(self):
        return os.path.basename(self.files.name)
    
    def __str__(self):
        return 'id : {}, title : {}'.format(self.id, self.title, self.contents)
    
    @property
    def update_counter(self):
        self.hits += 1
        self.save()
        
    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.write_dttm

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        else:
            time = datetime.now(tz=timezone.utc).date() - self.write_dttm.date()
            return str(time.days) + '일 전'
        
    class Meta:
        db_table = 'board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'
        
#광고테이블        
class Adboard(models.Model):
    title = models.CharField(max_length=64, verbose_name='제목')
    contents = models.TextField(verbose_name='글 내용',null=True, blank= True)
    writer = models.ForeignKey('kakao.Member', on_delete=models.CASCADE, verbose_name='광고 신청자', related_name='write_adboard')
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='글 작성일')
    board_name = models.CharField(max_length=32, default='전광판', verbose_name='게시판 종류')
    images = models.ImageField(verbose_name="광고 사진", upload_to="adver/")
    accept = models.BooleanField(default=False, verbose_name='광고 승인')
    adurl = models.CharField(max_length=512, verbose_name="광고url", default="https://www.naver.com")

    def __str__(self):
        return self.title

#댓글 테이블
class Comment(models.Model):
    comment = models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Board, null=True ,blank=True , on_delete=models.CASCADE)
    writer = models.ForeignKey('kakao.Member',on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.comment

#댓글 개수
class Comment_count(models.Model):
    comments = models.PositiveIntegerField(verbose_name='댓글수', null=True)
    
#대댓글 테이블
class ReComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    body = models.CharField('대댓글',max_length=150)
    date=models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey('kakao.Member',on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.body
    
##################신고 테이블#####################
#게시글
class Report_board(models.Model):
    report_choice= (
        ('abuse','욕설'),
        ('overlap','도배'),
        ('ad','홍보/상업성'),
        ('lewdness','음란성'),
        ('illegal_filming','불법촬영물'),
        ('etc','기타'),
        )
    report_user=models.ForeignKey('kakao.Member',on_delete=models.CASCADE,null=True,verbose_name='피신고자') # 이름에 속지말것 '피신고자'임
    reported_user=models.CharField(max_length=200,null=True,verbose_name='신고자')    #신고자
    report_date=models.DateTimeField(auto_now_add=True,verbose_name='신고 날짜')
    report_post=models.ForeignKey(Board, null=True ,blank=True , on_delete=models.CASCADE,verbose_name='신고 글')
    report_reason=models.CharField(max_length=20, choices=report_choice,null=True,verbose_name='신고 사유')
    report_detail=models.CharField(max_length=200,null=True,verbose_name='신고 상세내역')

#댓글    
class Report_Comment(models.Model):
    comment_report_choice= (
        ('abuse','욕설'),
        ('overlap','도배'),
        ('ad','홍보/상업성'),
        ('lewdness','음란성'),
        ('illegal_filming','불법촬영물'),
        ('etc','기다'),
        )
    comment_reported_user=models.ForeignKey('kakao.Member',on_delete=models.CASCADE,null=True,verbose_name='피신고자') # 이름에 속지말것 '피신고자'임
    comment_report_user=models.CharField(max_length=200,null=True,verbose_name='신고자')    #신고자
    comment_report_date=models.DateTimeField(auto_now_add=True,verbose_name='신고 날짜')
    comment_report_post=models.ForeignKey(Comment, null=True ,blank=True , on_delete=models.CASCADE,verbose_name='신고 댓글')
    comment_report_reason=models.CharField(max_length=20, choices=comment_report_choice,null=True,verbose_name='신고 사유')
    comment_report_detail=models.CharField(max_length=200,null=True,verbose_name='신고 상세내역')   

#대댓글    
class Report_ReComment(models.Model):
    recomment_report_choice= (
        ('abuse','욕설'),
        ('overlap','도배'),
        ('ad','홍보/상업성'),
        ('lewdness','음란성'),
        ('illegal_filming','불법촬영물'),
        ('etc','기다'),
        )
    recomment_reported_user=models.ForeignKey('kakao.Member',on_delete=models.CASCADE,null=True,verbose_name='피신고자') # 이름에 속지말것 '피신고자'임
    recomment_report_user=models.CharField(max_length=200,null=True,verbose_name='신고자')    #신고자
    recomment_report_date=models.DateTimeField(auto_now_add=True,verbose_name='신고 날짜')
    recomment_report_post=models.ForeignKey(Comment, null=True ,blank=True , on_delete=models.CASCADE,verbose_name='신고 댓글')
    recomment_report_reason=models.CharField(max_length=20, choices=recomment_report_choice,null=True,verbose_name='신고 사유')
    recomment_report_detail=models.CharField(max_length=200,null=True,verbose_name='신고 상세내역')
    
class Notice(models.Model):
    title= models.CharField(max_length=64, verbose_name='제목')
    contents = models.TextField(verbose_name='글 내용', blank=True)
    writer = models.ForeignKey("kakao.Member", on_delete=models.CASCADE)
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

class Recom(models.Model):
    user_nickname = models.CharField(max_length=50)
    recom_board1 = models.IntegerField(null=False)
    recom_board2 = models.IntegerField(null=False)
    recom_board3 = models.IntegerField(null=False)
    recom_board4 = models.IntegerField(null=False)
    recom_board5 = models.IntegerField(null=False)
    recom_board6 = models.IntegerField(null=False)
    recom_board7 = models.IntegerField(null=False)
    recom_board8 = models.IntegerField(null=False)
    recom_board9 = models.IntegerField(null=False)
    recom_board10 = models.IntegerField(null=False)
    recom_board11 = models.IntegerField(null=False)
    recom_board12 = models.IntegerField(null=False)
    recom_board13 = models.IntegerField(null=False)
    recom_board14 = models.IntegerField(null=False)
    recom_board15 = models.IntegerField(null=False)
    recom_board16 = models.IntegerField(null=False)
    recom_board17 = models.IntegerField(null=False)
    recom_board18 = models.IntegerField(null=False)
    recom_board19 = models.IntegerField(null=False)
    recom_board20 = models.IntegerField(null=False)