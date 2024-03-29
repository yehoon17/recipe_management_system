from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag, Rating
from django.contrib.auth.views import LoginView
from recipes.forms import CustomUserCreationForm
from .forms import RecipeForm, RecipeSearchForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg


def homepage(request):
    featured_recipes = Recipe.objects.all()[:3]  
    tags = Tag.objects.all() [:10] 
    
    form = RecipeSearchForm(request.GET)

    context = {
        'featured_recipes': featured_recipes,
        'tags': tags,
        'form': form, 
    }
    
    return render(request, 'recipes/homepage.html', context)

def search_recipes(request):
    if request.method == 'GET':
        form = RecipeSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Call a function to perform the search
            search_results = Recipe.objects.filter(title__icontains=query)
            return render(request, 'recipes/search_results.html', {'search_results': search_results})
    else:
        form = RecipeSearchForm()
    return render(request, 'recipes/search.html', {'form': form})
    
def tag_recipes(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    recipe_tags = RecipeTag.objects.filter(tag=tag)
    recipes = [recipe_tag.recipe for recipe_tag in recipe_tags]
    return render(request, 'recipes/tag_recipes.html', {'tag': tag, 'recipes': recipes})


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

    average_rating = recipe.rating_set.aggregate(Avg('value'))['value__avg']

    context = {
        'recipe': recipe,
        'can_edit': can_edit, 
        'ingredients': ingredients,
        'average_rating': average_rating,
        }

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

            # Handle ingredient submission
            ingredient_names = request.POST.getlist('ingredient_name[]')
            ingredient_quantities = request.POST.getlist('ingredient_quantity[]')
            ingredient_units = request.POST.getlist('ingredient_unit[]')

            for name, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units):
                # Create or get Ingredient object
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                # Create RecipeIngredient object and associate it with the recipe
                RecipeIngredient.objects.get_or_create(recipe=recipe, ingredient=ingredient, quantity=quantity, unit=unit)

            # Handle tag submission
            tag_input = request.POST.get('tag')
            tag_names = [tag.strip() for tag in tag_input.split(',') if tag.strip()]
            for tag_name in tag_names:
                # Create or get Tag object
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # Associate the tag with the recipe
                RecipeTag.objects.get_or_create(recipe=recipe, tag=tag)

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

def all_recipes(request):
    all_recipes = Recipe.objects.all()
    paginator = Paginator(all_recipes, 10)  # Adjust the number of recipes per page as needed
    page_number = request.GET.get('page')
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    return render(request, 'recipes/all_recipes.html', {'recipes': recipes})

def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        value = request.POST.get('rating')
        if value and 1 <= int(value) <= 5:
            if request.user.is_authenticated:  # Check if user is logged in
                rating = Rating.objects.create(recipe=recipe, user=request.user, value=value)
                return redirect('recipe_detail', pk=recipe_id)
            else:
                # Redirect to login page if user is not logged in
                return redirect('login')  # Assuming 'login' is the name of your login URL pattern
    return redirect('homepage')
