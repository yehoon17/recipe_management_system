from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Recipe, Comment


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
        

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Search for recipes', max_length=100)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
