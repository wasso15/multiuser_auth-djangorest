from django.urls import path
from .views import FreelanceSignupView, ClientSignupView, CustomAuthToken, LogoutView, FreelanceOnlyView, CLientOnlyView
urlpatterns = [
    path('signup/freelance/', FreelanceSignupView.as_view()),
    path('signup/client/', ClientSignupView.as_view()),
    path('login', CustomAuthToken.as_view(), name='auth-token'),
    path('logout', LogoutView.as_view(), name='Logout'),

    path('freelance/dashboard', FreelanceOnlyView.as_view(), name='Dashboard Freelancer'),
    path('client/dashboard', CLientOnlyView.as_view(), name='Dashboard Client'),





]