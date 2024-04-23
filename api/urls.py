from django.urls import path
from . import views

urlpatterns = [
    path('leads/', views.lead_list, name='lead-list'),
    path('leads/<int:pk>', views.lead_detail, name='lead-detail'),
    path('topics/', views.topic_list, name='topic-list'),
    path('topics/<int:pk>', views.topic_detail, name='topic-detail'),
]