from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('<slug:slug>/wyniki', views.ResultsView.as_view(), name='results'),
    path('<slug:slug>/glosowanie', views.VoteView.as_view(), name='vote'),
    path('<slug:slug>/komentarze', views.CommentView.as_view(), name='comment'),
    path('<slug:slug>/usuniete_komentarze',login_required(views.DeleteCommentView.as_view()), name='delete')
]