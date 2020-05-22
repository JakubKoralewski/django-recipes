from django.contrib import admin

# Register your models here.

from .models import (
	Recipe, IngredientType, Ingredient, IngredientsOfStep,
	Author, StepsOfRecipe, AmountType
)

admin.site.register(Recipe)
admin.site.register(Author)
admin.site.register(Ingredient)
admin.site.register(IngredientsOfStep)
admin.site.register(StepsOfRecipe)
