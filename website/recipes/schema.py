import graphene
from graphene_django.types import DjangoObjectType
from .models import Recipe, Ingredient

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class Query(graphene.ObjectType):
    all_recipes = graphene.List(RecipeType)
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_recipes(root, info):
        return Recipe.objects.all()

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.all()

schema = graphene.Schema(query=Query)
