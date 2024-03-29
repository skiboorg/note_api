from django.urls import path,include
from . import views

urlpatterns = [
    path('note/<uid>', views.GetNote.as_view()),
    path('save', views.Save.as_view()),
    path('update', views.Upadate.as_view()),
    path('fill', views.Fill.as_view()),
    path('dao_request', views.DaoRequestView.as_view()),
    path('captha', views.GetCaptcha.as_view()),
    path('raffles', views.GetRaffles.as_view()),
    path('raffle/<id>', views.GetRaffle.as_view()),
    path('vote', views.MakeVote.as_view()),
    path('user_votes', views.GetUserVotes.as_view()),
    path('stats', views.GetStats.as_view()),




]
