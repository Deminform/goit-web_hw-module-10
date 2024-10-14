from django.urls import path

from . import views
from .forms import QuoteForm, AuthorForm


app_name = 'quotes'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-quotes/', views.my_quotes, name='my-quotes'),
    path('add-quotes/', views.QuoteView.as_view(
        template_name='app_quote/add-quote.html',
        form_class=QuoteForm), name='add-quotes'),
    path('add-author/', views.AuthorView.as_view(
        template_name='app_quote/add-author.html',
        form_class=AuthorForm), name='add-author'),
]
