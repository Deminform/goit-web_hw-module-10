from django.urls import path
from django.contrib.auth.views import TemplateView

from . import views
from .forms import QuoteForm


app_name = 'quotes'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-quotes/', TemplateView.as_view(
        template_name='app_quote/my-quotes.html',
        form_class=QuoteForm), name='my-quotes'),
]
