from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view()),
    path('jobs/create/',views.JobCreateView.as_view()),
    path('jobs/<int:pk>/manage/',views.JobUpdateDeleteView.as_view())
]