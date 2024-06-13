
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events-and-groups", views.all_events, name="all_events"),
    path("events/<int:event_id>", views.event_detail, name="event_detail"),
    path("groups/<int:group_id>", views.group_detail, name="group_detail"),
    path('profile/', views.profile, name='profile'),    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API Views    
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('create_group', views.create_group, name='create-group'),
    path('edit_group/<int:group_id>', views.edit_group, name='edit-group'),
    path('create_event', views.create_event, name='create-event'),
    path('categories', views.categories, name='categories'),
]