from django.urls import path

from . import views

urlpatterns = [
    path('video_feed/', views.index, name='video_feed'),
    path('api/Members', views.getMembers, name='Members'),
    path('api/Transaction', views.getTransaction, name='Transaction'),
]