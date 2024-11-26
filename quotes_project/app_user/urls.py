from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import RegisterView
from .forms import LoginForm
from . import views

app_name = 'app_user'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(
        template_name='app_user/signin.html',
        form_class=LoginForm,
        redirect_authenticated_user=True), name='signin'),
    path('logout/', LogoutView.as_view(template_name='app_user/logout.html'), name='logout'),

    # ==================================================================================================

    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='app_user/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='app_user/password_reset_confirm.html',
                                          success_url='/user/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='app_user/password_reset_complete.html'),
         name='password_reset_complete'),
]
