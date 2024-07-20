from django.urls import path
from .views import CustomerRegister,ManagerRegister,CustomLoginView,Profile , ManagerRetrieveUpdateDestroy ,ListManager,SiteView,RequestPasswordResetEmail,SetNewPasswordAPIView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
  path('register',CustomerRegister.as_view()),
  path('login',CustomLoginView.as_view()),
  path('refresh',TokenRefreshView.as_view()),
  path('register-manager',ManagerRegister.as_view()),
  path('my-profile',Profile.as_view()),
  path('managers',ListManager.as_view()),
  path('managers/<pk>',ManagerRetrieveUpdateDestroy.as_view()),
  path("request-reset-password",RequestPasswordResetEmail.as_view(),name = 'request-reset-password'),
  path('password-reset-complete', SetNewPasswordAPIView.as_view(),name = 'password-reset-complete'),
  path('about',SiteView.as_view()),
]