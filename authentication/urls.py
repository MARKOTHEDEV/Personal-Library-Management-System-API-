from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('create-user',views.RegisterUserViewset,basename='create-user')



urlpatterns =[
    path('login/',views.LoginView.as_view(),name='login'),
     path( "refresh/token/",views.CustomTokenRefreshView.as_view(),name="token-refresh",)
] +router.urls