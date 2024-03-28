from django.contrib.auth.forms import UserCreationForm
from recipes.models import User

from django import forms
from .models import Recipe


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
        

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 
            'description', 
            'preparation_time', 
            'cooking_time', 
            'difficulty_level', 
            'image',
            ]
