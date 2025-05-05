from django.contrib import admin
from django.utils.html import format_html
from .models import Ingredient, Batiment, Recette, IngredientRecette

class IngredientRecetteInline(admin.TabularInline):    
    model = IngredientRecette
    extra = 0  # Nombre de lignes vides à afficher par défaut
    
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'recettes_entrees', 'recettes_sorties')
    search_fields = ['nom']  # Barre de recherche sur le champ 'nom'
    ordering = ['nom']  # Trier par le champ 'nom' (ajustez selon le champ de votre modèle)

    def recettes_entrees(self, obj):
        ingredientRecettes = obj.getRecettes('entree')
        return format_html(
            "<br/>".join([f'<a href="{ingredientRecette.recette.get_admin_url()}">{ingredientRecette.recette.nom}</a>' for ingredientRecette in ingredientRecettes])
        )
    recettes_entrees.short_description = "Recettes (Entrées)"

    def recettes_sorties(self, obj):
        ingredientRecettes = obj.getRecettes('sortie')
        return format_html(
            "<br/>".join([f'<a href="{ingredientRecette.recette.get_admin_url()}">{ingredientRecette.recette.nom}</a>' for ingredientRecette in ingredientRecettes])
        )
    recettes_sorties.short_description = "Recettes (Sorties)"

class RecetteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'batiment')
    search_fields = ['nom', 'batiment__nom']  # Barre de recherche sur le champ 'nom' et 'batiment'
    ordering = ['nom']  # Trier par le champ 'nom' (ajustez selon le champ de votre modèle)
    list_filter = ('batiment',)  # Filtrer par le champ 'batiment'
    inlines = [IngredientRecetteInline]
    
class BatimentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'electricite', 'volume')
    search_fields = ['nom']  # Barre de recherche sur le champ 'nom'
    ordering = ['nom']  # Trier par le champ 'nom' (ajustez selon le champ de votre modèle)
    


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Batiment, BatimentAdmin)
admin.site.register(Recette, RecetteAdmin)
