from django.urls import path,include
from . import views

urlpatterns = [
    path('note/<uid>', views.GetNote.as_view()),
    path('save', views.Save.as_view()),




]
