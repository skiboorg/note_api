from django.urls import path,include
from . import views

urlpatterns = [


    path('me', views.GetUser.as_view()),
    path('update', views.UpdateUser.as_view()),
    path('check12', views.CheckWallet.as_view()),
    path('send', views.Send.as_view()),
    path('claim', views.Claim.as_view()),
    path('recovery', views.SaveForm.as_view()),
]
