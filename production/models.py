from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    def getRecettes(self, type_recette):
        return IngredientRecette.objects.filter(ingredient=self, type=type_recette)

    def get_admin_url(self):
        return reverse('admin:production_ingredient_change', args=[self.id])


class Batiment(models.Model):
    nom = models.CharField(max_length=100)
    volume = models.FloatField()
    electricite = models.FloatField()

    def __str__(self):
        return self.nom

    def get_admin_url(self):
        return reverse('admin:production_batiment_change', args=[self.id])


class Recette(models.Model):
    nom = models.CharField(max_length=100)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    def get_admin_url(self):
        return reverse('admin:production_recette_change', args=[self.id])


class IngredientRecette(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='liaisons')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantite = models.FloatField()
    type = models.CharField(max_length=10, choices=[('entree', 'Entrée'), ('sortie', 'Sortie')])

    def __str__(self):
        return f"{self.type} - {self.ingredient.nom} ({self.quantite})"

    def get_admin_url(self):
        return reverse('admin:production_ingredientrecette_change', args=[self.id])
