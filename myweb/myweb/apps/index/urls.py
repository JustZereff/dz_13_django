from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('authors/', views.authors, name='authors'),
    path('add_author/', views.add_author, name='add_author'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout_view'),
    path('custom_login/', LoginView.as_view(template_name='registration/login.html'), name='custom_login'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]