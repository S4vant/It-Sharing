from django.contrib.auth import authenticate
from django.urls import path
from . import views

#Хранилище урлов main приложения
urlpatterns = [
    path('', views.index, name='home'),
    path('companies/', views.company_list, name='company'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('reg/',views.RegisterUser.as_view(), name ='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LoginUser.logout_user, name='logout'),
    path('profile/', views.PersonalPage, name='PersonalPage'),
    path('profile/edit/', views.edit_profile, name='PersonalPage_edit'),
    path('company/detail/<int:company_id>/', views.company_detail, name='company_detail'),
    path('company/edit/<int:company_id>/', views.edit_company, name='edit_company'),
]