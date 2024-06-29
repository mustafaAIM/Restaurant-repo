from django.urls import path
from .views import CustomerRegister,ManagerRegister,CustomLoginView,Profile
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
  path('register',CustomerRegister.as_view(),name = "register"),
  path('login',CustomLoginView.as_view()),
  path('refresh',TokenRefreshView.as_view()),
  path('register-manager',ManagerRegister.as_view()),
  path('profile/<pk>',Profile.as_view())
]