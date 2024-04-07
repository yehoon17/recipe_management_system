from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient 


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'user',
            'title',
            'description',
            'preparation_time',
            'cooking_time',
            'difficulty_level'
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'name'
        ]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer
    Ingredient =IngredientSerializer

    class Meta:
        model = RecipeIngredient
        fields = [
            'recipe',
            'ingredient',
            'quantity',
            'unit'
        ]
        