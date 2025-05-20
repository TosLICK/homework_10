from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .forms import LoginForm


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name = 'users/login.html', form_class = LoginForm, redirect_authenticated_user=True), name='login'),
    # path('logout/', LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('logout/', views.logoutuser, name='logout'),
]
