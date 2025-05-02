from django.contrib import admin
from .models import Ingredient, Batiment, Recette, IngredientRecette

class IngredientRecetteInline(admin.TabularInline):
    model = IngredientRecette
    extra = 1

class RecetteAdmin(admin.ModelAdmin):
    inlines = [IngredientRecetteInline]

admin.site.register(Ingredient)
admin.site.register(Batiment)
admin.site.register(Recette, RecetteAdmin)
