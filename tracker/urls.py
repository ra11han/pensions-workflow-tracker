"""URL routes for tracker pages and case CRUD actions."""

from django.urls import path
from . import views

# Defines the public landing page plus authenticated tracker workflows.
urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cases/', views.case_list, name='case_list'),
    path('cases/new/', views.case_create, name='case_create'),
    path('cases/<int:pk>/', views.case_detail, name='case_detail'),
    path('cases/<int:pk>/edit/', views.case_update, name='case_update'),
    path('cases/<int:pk>/delete/', views.case_delete, name='case_delete'),
]
