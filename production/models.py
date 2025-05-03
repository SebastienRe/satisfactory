from django.db import models


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Batiment(models.Model):
    nom = models.CharField(max_length=100)
    volume = models.FloatField()
    electricite = models.FloatField()

    def __str__(self):
        return self.nom


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
