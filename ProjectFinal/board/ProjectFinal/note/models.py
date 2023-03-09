from django.db import models
from kakao.models import Member

# Create your models here.

class Notelist(models.Model):
    receive_user = models.ForeignKey("kakao.Member",null=False , on_delete=models.CASCADE, verbose_name="받은사람", related_name='receive_user')
    send_user = models.ForeignKey("kakao.Member",null=False, on_delete=models.CASCADE, verbose_name="보낸사람", related_name='send_user')
    read_status = models.CharField(null=False, max_length=1, default="N")
    note_title = models.CharField(verbose_name="쪽지제목", null=False, default="", max_length=300)
    note_content = models.TextField(verbose_name="쪽지내용", null=False, default="")
    send_date = models.DateTimeField(auto_now_add=True, verbose_name="보낸 시간")
    