from django.urls import path

from ..views import pages_views

from django.contrib.auth import views as auth_views
from django.urls import path


app_name = 'pages_app'


urlpatterns = [
    path('', pages_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', pages_views.HomeView.as_view(), name='home'),
]
