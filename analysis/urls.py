"""
Urls paths definitiion
"""

from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.index, name='index'),
    path('uploadfile', views.upload, name='uploadfile'),
    path('upload', views.upload_file, name='upload'),
    path('tests', views.list_tests, name='all_tests'),
    path('<test_id>/view', views.view, name='view'),
    path('<test_id>/analyze/<sup>/<conf>', views.analyze, name='analyze'),
    path('<test_id>/getdata', views.getdata, name='getdata'),
]
