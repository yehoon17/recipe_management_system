import os
import json
import random
from django.core.management.base import BaseCommand
from recipes.models import User, Recipe, Ingredient, RecipeIngredient, Tag, RecipeTag

random.seed(42)


class Command(BaseCommand):
    help = 'Load data from JSON file'

    
    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=False)

        file_path = '../data/updated_recipes.json'
        with open(file_path, 'r') as f:
            data = json.load(f)

            for recipe in data:
                ingredients = recipe.pop('ingredients')
                tags = recipe.pop('tags')
                user = random.choice(users)
                
                new_recipe = Recipe.objects.create(user=user, **recipe)
                self.load_image(new_recipe)

                self.create_recipe_ingredient(new_recipe, ingredients)
                self.create_recipe_tag(new_recipe, tags)

                self.stdout.write(self.style.SUCCESS(f"Created recipe with ID: {new_recipe.id}"))


    def load_image(self, recipe):
        image_name = f"{recipe.title.replace(' ', '_')}.jpg"
        image_path = os.path.join('../data/images/', image_name)

        # Check if the image file exists
        if os.path.exists(image_path):
            # Open and read the image file
            with open(image_path, 'rb') as img_file:
                # Assign the image file to the image field of the new recipe
                recipe.image.save(image_name, img_file, save=True)

            # Print message when image is found
            self.stdout.write(self.style.SUCCESS(f"Image found for recipe: {recipe.title}"))
        else:
            # Print message when image is not found
            self.stdout.write(self.style.WARNING(f"No image found for recipe: {recipe.title}"))

    def create_recipe_ingredient(self, recipe, ingredients):
        for ingredient in ingredients:
            ingredient_, created = Ingredient.objects.get_or_create(name=ingredient['name'])
            RecipeIngredient.objects.create(
                recipe=recipe, 
                ingredient=ingredient_, 
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
