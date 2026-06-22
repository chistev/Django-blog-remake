from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),
    path('toggle-like/', views.toggle_like, name='toggle_like'), 
]