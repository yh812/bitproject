from django.contrib import admin
from note.models import Notelist

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ( "receive_user","send_user", "note_title", "note_content" ,"send_date", "read_status")

admin.site.register(Notelist, NoteAdmin)