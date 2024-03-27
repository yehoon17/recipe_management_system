from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Category
from django.contrib.auth.views import LoginView
from recipes.forms import CustomUserCreationForm
from .forms import RecipeForm


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


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Assign the current user to the recipe
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)  # Redirect to the recipe detail page
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})
