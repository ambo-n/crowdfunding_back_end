from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view(),name="project-list"),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('pledges/', views.PledgeList.as_view(), name="pledge-list"),
    path('pledges/<int:pk>/', views.PledgeDetail.as_view(), name="pledge-detail"),
    path('category/', views.CategoryList.as_view(), name="category-list"),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name="category-detail"),
]