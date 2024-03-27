from django.contrib import admin
from recipes.models import User, Recipe, Ingredient, Category, Review, Rating, Comment


admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Comment)
