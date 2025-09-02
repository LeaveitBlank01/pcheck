from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as account_views


app_name = "account"

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', account_views.custom_logout_view, name='logout'),
    path('', account_views.dashboard, name='dashboard'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    path('register/', account_views.register, name='register'),
    path('verify/<email>/', account_views.verify, name='verify'),
    # path('edit-profile/', account_views.edit_profile, name='edit-profile'),
]