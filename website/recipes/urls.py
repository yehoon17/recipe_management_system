from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
]
