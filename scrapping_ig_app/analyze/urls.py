from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze, name='analyze'),
    path('split_words/', views.split_words, name='split_words'),
    path('predict_users/', views.predict_users, name='predict_users'),
]