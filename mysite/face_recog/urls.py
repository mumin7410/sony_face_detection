from django.urls import path

from . import views

urlpatterns = [
    path("camera", views.index, name="index"),
    path('api/Members', views.getMembers, name='Members'),
    path('api/Transaction', views.getTransaction, name='Transaction'),
]