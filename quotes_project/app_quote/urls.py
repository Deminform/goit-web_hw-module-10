from django.urls import path

from . import views


app_name = 'app_quotes'

urlpatterns = [
    path('', views.index, name='index'),
    path('init/', views.initialize_database, name='init'),
    path('my-quotes/', views.my_quotes, name='my-quotes'),
    path('author/<int:pk>', views.author, name='author'),
    path('add-quotes/', views.QuoteView.as_view(), name='add-quotes'),
    path('add-author/', views.AuthorView.as_view(), name='add-author'),
    path('remove/<int:pk>', views.remove_quote, name='remove'),
    path('edit-quote/<int:pk>/', views.QuoteUpdateView.as_view(), name='edit-quote'),
    path('tag/<str:tag>', views.tags, name='tag')
]
