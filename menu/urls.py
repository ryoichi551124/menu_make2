from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('next', views.next, name='next'),
    path('predict', views.predict, name='predict'),
    path('next_predict', views.next_predict, name='next_predict'),
    path('loading', views.loading, name='loading'),
    path('decision', views.decision, name='decision'),

    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='menu/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]


