from django.shortcuts import render
from production.models import Recette

# Create your views here.
# logique de calcul (ex: services.py)

def calculer_valeur(ingredient, quantite=1):

    recettes = Recette.objects.filter(liaisons__ingredient=ingredient, liaisons__type='sortie').distinct() # Récupérer les recettes qui produisent cet ingrédient

    if not recettes.exists(): # Si aucune recette ne produit cet ingrédient, on retourne la valeur de l'ingrédient lui-même
        valeur = 1
        chemin = [f"{quantite:.2f} x {ingredient.nom} (foreuse)"]
        return valeur, chemin

    meilleure_valeur = float("inf")
    meilleur_chemin = []

    for recette in recettes:
        entrees = recette.liaisons.filter(type='entree') # Récupérer les ingrédients d'entrée de la recette
        sorties = recette.liaisons.filter(type='sortie') # Récupérer les ingrédients de sortie de la recette

        valeur_entree = 0
        sous_chemin = []

        quantite_sortie = next((s.quantite for s in sorties if s.ingredient == ingredient), 0) # Récupérer la quantité de l'ingrédient de sortie dans la recette
        if quantite_sortie == 0:
            continue

        # Calcul du nombre de fois que la recette doit être effectuée
        nombre_recettes = quantite / quantite_sortie

        for entree in entrees:
            quantite_entree_ajustee = entree.quantite * nombre_recettes # Ajustement des quantités des ingrédients d'entrée
            v, c = calculer_valeur(entree.ingredient, quantite_entree_ajustee) # Appel récursif pour chaque ingrédient d'entrée
            valeur_entree += v * entree.quantite
            sous_chemin += c

        valeur_entree += recette.batiment.cout_valeur()

        valeur_unitaire = valeur_entree / quantite_sortie

        if valeur_unitaire < meilleure_valeur:
            meilleure_valeur = valeur_unitaire
            meilleur_chemin = sous_chemin + [
                f"{quantite:.2f} x {ingredient.nom} via '{recette.nom}' (Valeur={valeur_unitaire:.2f}, Batiment={recette.batiment.nom}, Nb_Batiments={nombre_recettes:.3f})"
            ]
            
    return meilleure_valeur, meilleur_chemin

from django.shortcuts import render, get_object_or_404
from .models import Ingredient
from .views import calculer_valeur

def calculer_production(request):
    resultat = None
    chemin = None

    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient')
        quantite = float(request.POST.get('quantite', 1))
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)

        # Appel à la fonction calculer_valeur
        resultat, chemin = calculer_valeur(ingredient, quantite)

    ingredients = Ingredient.objects.all().order_by('nom')  # Récupérer tous les ingrédients pour le formulaire
    return render(request, 'calculer_production.html', {
        'ingredients': ingredients,
        'resultat': resultat,
        'chemin': chemin,
    })