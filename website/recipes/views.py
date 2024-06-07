from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag, Rating, Comment
from django.contrib.auth.views import LoginView
from .forms import RecipeForm, RecipeSearchForm, CustomUserCreationForm, ProfileEditForm, ProfileForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Q
from rest_framework import generics
from .serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer
from django.contrib import messages
from oauth2_provider.decorators import protected_resource
from django.http import JsonResponse

@protected_resource()
def my_protected_view(request):
    return JsonResponse({'message': 'This is a protected view'})


class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class IngredientListCreate(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeIngredientListCreate(generics.ListCreateAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


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

@login_required
def profile(request):
    recipes = Recipe.objects.filter(user=request.user)
    context = {'recipes': recipes}
    return render(request, 'profile/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        # Handle profile image form
        profile_image_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_image_form.is_valid():
            profile_image_form.save()
        
        # Handle user information form
        user_form = ProfileEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()

        return redirect('profile')  # Redirect to the profile page after editing
    else:
        profile_image_form = ProfileForm(instance=request.user.profile)
        user_form = ProfileEditForm(instance=request.user)
    return render(request, 'profile/profile_edit.html', {'profile_image_form': profile_image_form, 'user_form': user_form})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.user:  # Check if the current user is the owner of the recipe
        can_edit = True
    else:
        can_edit = False 
        
    # Retrieve ingredients associated with the recipe
    ingredients = recipe.recipeingredient_set.all()

    average_rating = recipe.rating_set.aggregate(Avg('value'))['value__avg']

    # comment
    comments = Comment.objects.filter(recipe=recipe)
    comments_tree = {}
    comments_dict = {}

    for comment in comments:
        comments_dict[comment.id] = {
            'id': comment.id,
            'user': comment.user.username,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'parent_comment_id': comment.parent_comment_id,
            'replies': [],
            'can_edit': request.user == comment.user
        }

    for comment_id, comment_data in comments_dict.items():
        parent_comment_id = comment_data['parent_comment_id']
        if parent_comment_id:
            parent_comment = comments_dict[parent_comment_id]
            parent_comment['replies'].append(comment_data)
        else:
            comments_tree[comment_id] = comment_data

    context = {
        'recipe': recipe,
        'can_edit': can_edit, 
        'ingredients': ingredients,
        'average_rating': average_rating,
        'comments': list(comments_tree.values()),
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

            ingredients = []
            for name, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units):
                # Create or get Ingredient object
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                ingredients.append(ingredient)
                # Create RecipeIngredient object and associate it with the recipe
                defaults = {
                    'quantity': quantity,
                    'unit': unit
                }
                RecipeIngredient.objects.update_or_create(
                    recipe=recipe,
                    ingredient=ingredient,
                    defaults=defaults
                )
            # Delete if not in input but in database
            recipe_ingredient_to_delete = RecipeIngredient.objects.filter(
                recipe=recipe
            ).exclude(
                Q(ingredient__in=ingredients)
            )
            recipe_ingredient_to_delete.delete()


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
    paginator = Paginator(all_recipes, 9)  # Adjust the number of recipes per page as needed
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

@login_required
def create_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.save()
            return redirect('recipe_detail', pk=recipe_id)
        
@login_required
def reply_comment(request, recipe_id, comment_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.parent_comment = get_object_or_404(Comment, pk=comment_id)
            comment.save()
            return redirect('recipe_detail', pk=recipe_id)


@login_required
def update_comment(request, recipe_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if the authenticated user is the owner of the comment
    if request.user != comment.user:
        return HttpResponseForbidden("You are not allowed to update this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe_id)
    else:
        form = CommentForm(instance=comment)

@login_required
def delete_comment(request, recipe_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if the authenticated user is the owner of the comment
    if request.user != comment.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('recipe_detail', pk=recipe_id)
