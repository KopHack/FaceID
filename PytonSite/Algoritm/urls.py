from django.urls import path
 
from . import views
 
urlpatterns = [
    path('', views.index, name='index'),
    path('load_send/', views.load_send, name='load_send'),
    path('load_find/', views.load_find, name='load_find'),
    path('send/', views.send, name='send'),
    path('find/', views.find, name='find'),
]