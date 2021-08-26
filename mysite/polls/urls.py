from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('<slug:slug>/wyniki', views.ResultsView.as_view(), name='results'),
    path('<slug:slug>/wybory', views.vote, name='wybory'),
    path('<slug:slug>/komentarze', views.add_comment_to_question, name='komentarze'),
    path('<slug:slug>/delete/',views.delete_comment, name='delete')
]