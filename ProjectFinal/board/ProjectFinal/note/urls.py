from django.urls.conf import path
from note import views

app_name = 'note'
urlpatterns = [
    path('notelist', views.NoteListView.as_view(), name='notelist'),
    path('notewrite', views.NoteWriteView.as_view(), name='notewrite'),
    path('notedetail', views.NoteDetailView.as_view(), name='notedetail'),
    path('notedelete', views.NoteDeleteView.as_view(), name='notedelete'),
]




