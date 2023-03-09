from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
        
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class Person(models.Model):
    bs_nickname= models.CharField(max_length=50)
    def __str__(self):
        return '%s' % (self.bs_nickname)
    
class Survey_Status(models.Model):
    bs_id = models.ForeignKey('kakao.Member', on_delete=models.CASCADE, verbose_name='작성자')
    status = models.CharField(null=False, max_length=1, default="y")
    def __str__(self):
        return '%s' % (self.status)
    
class Table(models.Model):
    bs_id = models.ForeignKey('kakao.Member', on_delete=models.CASCADE, verbose_name='작성자')
    question_name = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text_name = models.ForeignKey(Choice, on_delete=models.CASCADE)
