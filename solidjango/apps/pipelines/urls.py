from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<pipeline_id>/', views.details, name='details'),
    path('<pipeline_id>/setup/', views.setup, name='setup'),
    path('<pipeline_id>/setup/deploy/', views.deploy, name='deploy'),
]
