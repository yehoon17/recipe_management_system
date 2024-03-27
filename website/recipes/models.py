from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pass

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    preparation_time = models.PositiveIntegerField()  # in minutes
    cooking_time = models.PositiveIntegerField()  # in minutes
    difficulty_level = models.CharField(max_length=50)

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    recipes = models.ManyToManyField(Recipe, related_name='ingredients')

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
