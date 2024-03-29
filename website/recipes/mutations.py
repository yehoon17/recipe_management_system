import graphene
from graphene_django.types import DjangoObjectType
from .models import Recipe

# Define mutation input types
class RecipeInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    # Add more fields as needed

# Define mutation classes
class CreateRecipeMutation(graphene.Mutation):
    class Arguments:
        input = RecipeInput(required=True)

    recipe = graphene.Field(RecipeType)

    def mutate(self, info, input):
   
