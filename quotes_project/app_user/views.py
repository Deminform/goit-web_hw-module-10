from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


class RegisterView(View):
    template_name = 'app_user/signup.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('quotes:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account created for {username}')
            return redirect('app_quotes:index')
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app_user/password_reset_html.html'
    email_template_name = 'app_user/password_reset_email.html'
    html_email_template_name = 'app_user/password_reset_email.html'
    success_url = reverse_lazy('app_user:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'app_user/password_reset_subject.txt'