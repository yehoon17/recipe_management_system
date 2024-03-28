from django.contrib import admin
from recipes.models import User, Recipe, Ingredient, RecipeIngredient, Tag, RecipeTag, Review, Rating, Comment


admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(RecipeTag)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Comment)
