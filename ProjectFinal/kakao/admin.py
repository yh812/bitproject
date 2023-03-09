from django.contrib import admin
from .models import Member


@admin.register(Member)
# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'userid',
        'nickname',
        'passwd',
        'email',
        'gender',
        'generation',
        'birth',
        'regdate',
        'user_current_point'
        )
    search_fields = ['nickname', 'userid']