from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, Recipe, Comment, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class ProfileEditForm(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']        

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
