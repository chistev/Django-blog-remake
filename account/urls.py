from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'account'
urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', LogoutView.as_view(next_page='home', http_method_names=['post']), name='logout'),
]
