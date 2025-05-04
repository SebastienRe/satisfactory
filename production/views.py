import logging
from django.shortcuts import render, get_object_or_404
from production.models import Recette
from .models import Ingredient

# Create your views here.
# logique de calcul (ex: services.py)
VALEUR_VOLUME = 5

def get_ingredient(ingredient_nom):
    try:
        ingredient = Ingredient.objects.get(nom=ingredient_nom)
    except Ingredient.DoesNotExist:
        ingredient = None
    return ingredient

def calculer_valeur(ingredient, quantite=1, niveau=0, visites=None):
    if visites is None:
        visites = set()

    if ingredient.id in visites:
        chemin = [{
            "niveau": niveau,
            "txt": f"Cycle détecté avec {ingredient.nom} (arrêt de la récursion)"
        }]
        return 0, chemin  # Ignorer ce chemin

    visites.add(ingredient.id)

    recettes = Recette.objects.filter(liaisons__ingredient=ingredient, liaisons__type='sortie').distinct()

    if not recettes.exists():
        valeur = 0
        chemin = [{
            "niveau": niveau,
            "txt": f"{quantite:.2f} x {ingredient.nom} (Pas de recette)"
        }]
        visites.remove(ingredient.id)
        return valeur, chemin

    meilleure_valeur = float("inf")
    meilleur_chemin = []

    for recette in recettes:
        entrees = recette.liaisons.filter(type='entree')
        sorties = recette.liaisons.filter(type='sortie')

        valeur_entree = 0
        sous_chemin = []

        quantite_sortie = next((s.quantite for s in sorties if s.ingredient == ingredient), 0)
        if quantite_sortie == 0:
            continue

        nombre_recettes = quantite / quantite_sortie

        for entree in entrees:
            quantite_entree_ajustee = entree.quantite * nombre_recettes
            v, c = calculer_valeur(entree.ingredient, quantite_entree_ajustee, niveau + 1, visites.copy())
            valeur_entree += v * entree.quantite
            sous_chemin += c

        ingredient_elec = get_ingredient("Electricité")
        v_elect, c = calculer_valeur(ingredient_elec, recette.batiment.electricite * nombre_recettes, niveau + 1, visites.copy())
        valeur_entree += v_elect + VALEUR_VOLUME * recette.batiment.volume

        valeur_unitaire = valeur_entree / quantite_sortie

        if valeur_unitaire < meilleure_valeur:
            meilleure_valeur = valeur_unitaire
            meilleur_chemin = [
                {
                    "niveau": niveau,
                    "txt": f"{quantite:.2f} x {ingredient.nom} via '{recette.nom}' (Valeur={valeur_unitaire:.2f}, Batiment={recette.batiment.nom}, Nb_Batiments={nombre_recettes:.2f})"
                }
            ] + sous_chemin

    visites.remove(ingredient.id)

    if meilleure_valeur == float("inf"):
        return 0, [{
            "niveau": niveau,
            "txt": f"Aucun chemin valide trouvé pour {ingredient.nom}"
        }]

    return meilleure_valeur, meilleur_chemin

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