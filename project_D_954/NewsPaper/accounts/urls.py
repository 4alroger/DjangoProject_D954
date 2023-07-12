from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),

]
