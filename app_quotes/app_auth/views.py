from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


# Create your views here.
class RegisterView(View):
    template_name = 'app_auth/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('app_photo:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Greeting {username}, your account has been created.')
            return redirect('app_auth:signin')
        return render(request, self.template_name, {'form': form})
