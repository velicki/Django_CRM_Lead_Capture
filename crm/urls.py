from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('leads/', views.leads_view, name='leads'),
    path('delete/<str:pk>', views.delete_lead, name='delete'),
    path('delete_topic/<str:pk>', views.delete_topic, name='delete_topic'),
    path('edit_lead/<str:pk>', views.edit_lead, name='edit'),
    path('add_lead/', views.add_lead, name='add_lead'),
    path('topics/', views.add_remove_topic, name='topic'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('superuser/', views.superuser_admin, name='superuser'),
    path('superuser_users/', views.superuser_users, name='superuser_users'),
    path('delete_user/<str:pk>', views.delete_user, name='delete_user'),
    path('superuser_topic/<str:pk>', views.superuser_topic, name='superuser_topic'),
    path('superuser_leads/<str:pk>', views.superuser_leads, name='superuser_leads'),
]