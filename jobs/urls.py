from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
]