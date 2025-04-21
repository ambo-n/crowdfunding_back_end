from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view(), name="users-list"),
    path('users/<int:pk>/', views.CustomUserDetail.as_view(), name="user-details")
]
