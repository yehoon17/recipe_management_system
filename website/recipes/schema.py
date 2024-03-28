import graphene
from graphene_django.types import DjangoObjectType
from .models import Recipe, Ingredient
from .mutations import CreateRecipeMutation

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class Query(graphene.ObjectType):
    all_recipes = graphene.List(RecipeType)
    def resolve_all_recipes(root, info):
        return Recipe.objects.all()

    all_ingredients = graphene.List(IngredientType)
    def resolve_all_ingredients(root, info):
        return Ingredient.objects.all()
    
    recipe_by_id = graphene.Field(RecipeType, id=graphene.Int())
    def resolve_recipe_by_id(self, info, id):
        return Recipe.objects.get(id=id)

# Define Mutation class with mutation fields
class Mutation(graphene.ObjectType):
    # Include mutation classes from mutations.py
    create_recipe = CreateRecipeMutation.Field()

# Create Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
