from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quizzes/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('submissions/<int:submission_id>/result/', views.quiz_result, name='quiz_result'),
    path('events/', views.event_list, name='event_list'),
]