from django.contrib import admin
from polls.models import Question, Choice, Table, Survey_Status

class Choiceinline(admin.TabularInline):
    model = Choice
    extra = 5
    list_display = ('id', 'question_id', 'choice_text', 'votes')
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),  
        ]
    inlines = [Choiceinline]
    list_display = ('question_text', 'pub_date')
class SurveyStatusyesornot(admin.ModelAdmin):
    list_display = ('bs_id', 'status')

class SurveyTable(admin.ModelAdmin):
    list_display = ('bs_id', 'question_name', 'choice_text_name')
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Table)
admin.site.register(Survey_Status)

    