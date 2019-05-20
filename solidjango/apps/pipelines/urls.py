from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<pipeline_id>/', views.DetailsView.as_view(), name='details'),
    path('<pipeline_id>/setup/', views.setup, name='setup'),
    path('<pipeline_id>/setup/deploy/', views.deploy, name='deploy'),
]
