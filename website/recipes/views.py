from django.shortcuts import render
from .models import Recipe, Category
from django.contrib.auth.views import LoginView

def homepage(request):
    featured_recipes = Recipe.objects.all()[:3]  
    categories = Category.objects.all() 
    
    context = {
        'featured_recipes': featured_recipes,
        'categories': categories,
    }
    
    return render(request, 'recipes/homepage.html', context)

class CustomLoginView(LoginView):
    template_name = 'recipes/login.html'
