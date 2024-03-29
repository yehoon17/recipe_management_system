import graphene
from graphene_django.types import DjangoObjectType
from .models import Recipe, Ingredient, Tag, User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        
class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class TagType(DjangoObjectType):
    class Meta:
        model = Tag

class Query(graphene.ObjectType):
    all_recipes = graphene.List(RecipeType)
    all_ingredients = graphene.List(IngredientType)
    all_tags = graphene.List(TagType)
    
    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.all()
    
    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()
    
    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return CreateUser(user=user)

class CreateRecipe(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        preparation_time = graphene.Int()
        cooking_time = graphene.Int()
        difficulty_level = graphene.String()
        image = graphene.String()
    
    recipe = graphene.Field(RecipeType)

    def mutate(self, info, title, description, preparation_time, cooking_time, difficulty_level, image):
        # Your logic to create a new recipe with provided data
        new_recipe = Recipe.objects.create(title=title, description=description, preparation_time=preparation_time, cooking_time=cooking_time, difficulty_level=difficulty_level, image=image)
        return CreateRecipe(recipe=new_recipe)

class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
