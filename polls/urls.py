from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('polls/', views.questions, name='questions'),
    path('question/<int:question_id>/', 
    	views.question, name='question'),
    path('question/<int:question_id>/results/', 
    	views.results, name='results'),
    path('question/<int:question_id>/vote/', 
    	views.vote, name='vote'),
]