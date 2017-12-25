from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload'),
    path('<test_id>/analyze/', views.analyze, name='analyze'),
    path('tests/', views.list_tests, name='all_tests'),
]