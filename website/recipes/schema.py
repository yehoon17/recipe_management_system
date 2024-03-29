import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from .models import Recipe, Ingredient, Tag, User, RecipeIngredient, RecipeTag 


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
    all_users = graphene.List(UserType, is_superuser=graphene.Boolean())
    all_recipes = graphene.List(RecipeType)
    all_ingredients = graphene.List(IngredientType)
    all_tags = graphene.List(TagType)
    recipes_by_title = graphene.List(RecipeType, title=graphene.String())
    
    def resolve_all_users(self, info, is_superuser=None):
        queryset = User.objects.all()
        if is_superuser is not None:
            queryset = queryset.filter(is_superuser=is_superuser)
        return queryset
    
    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.all()
    
    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()
    
    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_recipes_by_title(self, info, title):
        return Recipe.objects.filter(title__icontains=title)
    
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
        user_id = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        preparation_time = graphene.Int()
        cooking_time = graphene.Int()
        difficulty_level = graphene.String()
        image = Upload(required=False)
    
    recipe = graphene.Field(RecipeType)

    def mutate(self, info, user_id, title, description, preparation_time, cooking_time, difficulty_level, image):
        user = User.objects.get(pk=user_id)

        new_recipe = Recipe.objects.create(
            user=user,
            title=title, 
            description=description, 
            preparation_time=preparation_time, 
            cooking_time=cooking_time, 
            difficulty_level=difficulty_level, 
            image=image
            )
        return CreateRecipe(recipe=new_recipe)


class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
