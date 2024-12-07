from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.UpdateNewsView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteNewsView.as_view(), name='delete'),
]