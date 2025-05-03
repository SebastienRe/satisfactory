from django.db import models

VALEUR_VOLUME = 5
VALEUR_ELECTRICITE = 0.4

class Ingredient(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Batiment(models.Model):
    nom = models.CharField(max_length=100)
    volume = models.FloatField()
    electricite = models.FloatField()

    def __str__(self):
        return self.nom

    def cout_valeur(self):
        return self.volume * VALEUR_VOLUME + self.electricite * VALEUR_ELECTRICITE


class Recette(models.Model):
    nom = models.CharField(max_length=100)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class IngredientRecette(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='liaisons')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantite = models.FloatField()
    type = models.CharField(max_length=10, choices=[('entree', 'Entrée'), ('sortie', 'Sortie')])

    def __str__(self):
        return f"{self.type} - {self.ingredient.nom} ({self.quantite})"
