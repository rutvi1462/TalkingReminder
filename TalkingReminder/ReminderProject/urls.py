from django.urls import path, include
from ReminderProject import views

urlpatterns = [
    path('', views.home, name="home"),
    path('addReminder/', views.addReminder, name="addReminder"),
    path('chooseVoice/', views.chooseVoice, name="chooseVoice"),
    path('deleteReminder/', views.deleteReminder, name="deleteReminder"),
]