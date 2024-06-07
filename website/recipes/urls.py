from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('protected/', views.my_protected_view),
    path('', views.homepage, name='homepage'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Profile Management
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    
    # Recipe Management
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('all-recipes/', views.all_recipes, name='all_recipes'),
    
    # Recipe Search
    path('search-recipes/', views.search_recipes, name='search_recipes'),

    # Tag Filtering
    path('tag/<int:tag_id>/', views.tag_recipes, name='tag_recipes'),

    # Rating
    path('rate/<int:recipe_id>/', views.rate_recipe, name='rate_recipe'),

    # GraphQL Endpoint
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    # REST API Endpoints
    path('rest-api/recipe/', views.RecipeListCreate.as_view()),
    path('rest-api/ingredient/', views.IngredientListCreate.as_view()),
    path('rest-api/recipe-ingredient/', views.RecipeIngredientListCreate.as_view()),

    # REST API Endpoints
    path('recipe/<int:recipe_id>/comment/create/', views.create_comment, name='create_comment'),
    path('recipe/<int:recipe_id>/comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('recipe/<int:recipe_id>/comment/<int:comment_id>/update/', views.update_comment, name='update_comment'),
    path('recipe/<int:recipe_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
