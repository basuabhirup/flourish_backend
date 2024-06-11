
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events", views.all_events, name="all_events"),
    path("events/<int:event_id>", views.event_detail, name="event_detail"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('profile/', views.profile, name='profile'),    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_group/', views.create_group, name='create-group'),
]