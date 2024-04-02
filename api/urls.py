from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('update/<int:pk>', views.updateLead),
    path('add/', views.addLead),
]