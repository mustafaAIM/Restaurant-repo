from django.urls import path
from .views import CustomerRegister,ManagerRegister,CustomLoginView,Profile , ManagerRetrieveUpdateDestroy ,ListManager
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
  path('register',CustomerRegister.as_view()),
  path('login',CustomLoginView.as_view()),
  path('refresh',TokenRefreshView.as_view()),
  path('register-manager',ManagerRegister.as_view()),
  path('my-profile',Profile.as_view()),
  path('managers',ListManager.as_view()),
  path('managers/<pk>',ManagerRetrieveUpdateDestroy.as_view()),

]