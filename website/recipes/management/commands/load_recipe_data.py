import json
import random
from django.core.management.base import BaseCommand
from recipes.models import User, Recipe, Ingredient, RecipeIngredient, Tag, RecipeTag

random.seed(42)


class Command(BaseCommand):
    help = 'Load data from JSON file'

    
    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=False).values_list('id', flat=True)

        file_path = '../data/updated_recipes.json'
        with open(file_path, 'r') as f:
            data = json.load(f)

            for recipe in data:
                ingredients = recipe.pop('ingredients')
                tags = recipe.pop('tags')
                user = random.choice(users)
                
                new_recipe = Recipe.objects.create(user=user, **recipe)
                self.create_recipe_ingredient(new_recipe, ingredients)
                self.create_recipe_tag(new_recipe, tags)

                self.stdout.write(self.style.SUCCESS(f"Created recipe with ID: {new_recipe.id}"))


    def create_recipe_ingredient(self, recipe, ingredients):
        for ingredient in ingredients:
            ingredient_, created = Ingredient.objects.get_or_create(name=ingredient['name'])
            RecipeIngredient.objects.create(
                recipe=recipe, 
                ingredient=ingredient, 
                quantity=ingredient['quantity'], 
                unit=ingredient['unit']
                )

    def create_recipe_tag(self, recipe, tags):
        for tag in tags:
            tag_, created = Tag.objects.get_or_create(name=tag)
            RecipeTag.objects.create(
                recipe=recipe, 
                tag=tag_, 
                )
