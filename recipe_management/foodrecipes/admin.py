from django.contrib import admin

from foodrecipes.models import Ingredient,RecipeUser,Recipe,Favorite,StepImage

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(RecipeUser)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(StepImage)
