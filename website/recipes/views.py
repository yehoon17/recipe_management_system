from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag
from django.contrib.auth.views import LoginView
from recipes.forms import CustomUserCreationForm
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required


def homepage(request):
    featured_recipes = Recipe.objects.all()[:3]  
    tags = Tag.objects.all() 
    
    context = {
        'featured_recipes': featured_recipes,
        'tags': tags,
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
    if request.user == recipe.user:  # Check if the current user is the owner of the recipe
        can_edit = True
    else:
        can_edit = False 
        
    # Retrieve ingredients associated with the recipe
    ingredients = recipe.recipeingredient_set.all()

    context = {'recipe': recipe, 'can_edit': can_edit, 'ingredients': ingredients}

    return render(request, 'recipes/recipe_detail.html', context)


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Assign the current user to the recipe
            recipe.save()

            # Handle ingredient submission
            ingredient_names = request.POST.getlist('ingredient_name[]')
            ingredient_quantities = request.POST.getlist('ingredient_quantity[]')
            ingredient_units = request.POST.getlist('ingredient_unit[]')

            for name, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units):
                # Create or get Ingredient object
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                # Create RecipeIngredient object and associate it with the recipe
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity, unit=unit)

            # Handle tag submission
            tag_input = request.POST.get('tag')
            tag_names = [tag.strip() for tag in tag_input.split(',') if tag.strip()]
            for tag_name in tag_names:
                # Create or get Tag object
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # Associate the tag with the recipe
                RecipeTag.objects.create(recipe=recipe, tag=tag)

            return redirect('recipe_detail', pk=recipe.pk)  # Redirect to the recipe detail page
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.user:  # Check if the current user is the owner of the recipe
        return redirect('recipe_detail', pk=pk)  # Redirect to recipe detail page if user doesn't have permission
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=pk)  # Redirect to recipe detail page after editing
    else:
        # Initialize the form with instance data including ingredients
        form = RecipeForm(instance=recipe)
        # Retrieve ingredients associated with the recipe
        ingredients = recipe.recipeingredient_set.all()

    context = {'recipe': recipe, 'ingredients': ingredients, 'form': form}

    return render(request, 'recipes/recipe_edit.html', context)

@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.user:  # Check if the current user is the owner of the recipe
        recipe.delete()
    return redirect('homepage')

