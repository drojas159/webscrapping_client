from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('user/', views.users, name='user'),
    path('open_application/', views.open_application, name='open_application'),
    path('publication/', views.publications, name='publication'),
    path('comment/', views.comments, name='comment'),
    path('', views.index, name='index')
]
