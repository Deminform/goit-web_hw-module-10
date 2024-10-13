from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView
from .forms import LoginForm


app_name = 'app_user'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(
        template_name='app_user/signin.html',
        form_class=LoginForm,
        redirect_authenticated_user=True), name='signin'),
    path('logout/', LogoutView.as_view(template_name='app_user/logout.html'), name='logout'),
]
