from django.db import models

# Create your models here.

class Member(models.Model):
    userid = models.CharField(max_length=50, verbose_name="아이디", unique=True)
    nickname = models.CharField(max_length=50, verbose_name="닉네임")
    passwd = models.CharField(max_length=50, verbose_name="비밀번호", null=True)
    tel = models.CharField( max_length=20, verbose_name="전화번호", null=True )
    email = models.EmailField(max_length=128, verbose_name="이메일", null=True)
    gender = models.CharField(max_length=10, verbose_name="성별", null=True, blank = True)
    generation = models.CharField(max_length=10, verbose_name="연령대", null=True)
    birth = models.CharField(max_length=50, verbose_name="생일", null=True)
    userimage = models.CharField(max_length=4096, verbose_name="사용자이미지", null=True, blank=True)
    user_total_point = models.PositiveIntegerField(verbose_name="누적포인트", default=0)
    user_current_point = models.PositiveIntegerField(verbose_name="현재포인트", default=0)
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="가입일", null=True)
    address = models.CharField(max_length=200, verbose_name="주소", null=True)
    address2 = models.CharField( max_length=50, verbose_name="상세주소", null=True, blank=True )
    social = models.CharField(max_length=1, verbose_name="소셜로그인여부", null=True, blank=True)
    userimg = models.ImageField(upload_to="portimg/", null=True, verbose_name='프사', blank=True)
    def __str__(self):
        return self.nickname