from django.urls import path
from . import views

urlpatterns=[
    path('signup/',views.SignupView.as_view(), name='signup'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('recruiters/<int:pk>/status/',views.ApproveRecruiterView.as_view(), name='approve recruiter'),
    path('users/', views.UserListView.as_view()),
    path('users/recruiters/', views.RecruiterUserListView.as_view()),
    path('recruiters/', views.RecruiterProfileListView.as_view()),

]