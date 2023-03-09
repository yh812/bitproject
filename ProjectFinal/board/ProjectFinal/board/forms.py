from django import forms
from board.models import Board
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from board.models import Comment, ReComment
from django.forms.widgets import TextInput

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields=['comment'] 
        widgets={
            'comment': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 1000px;',
                
                })
            }
       
        
class ReCommentForm(forms.ModelForm):
    class Meta:
        model = ReComment
        fields=['body','comment']
        widgets={
            'body' : TextInput(attrs={
                'class': "form-control",
                'style': 'max-width:910px;',
                })
            
            }

        