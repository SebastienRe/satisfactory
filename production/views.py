from django.shortcuts import render
from production.models import Recette

# Create your views here.
# logique de calcul (ex: services.py)

def calculer_valeur(ingredient, quantite=1, cache=None):
    if cache is None:
        cache = {}

    if ingredient.id in cache:
        return cache[ingredient.id]

    recettes = Recette.objects.filter(liaisons__ingredient=ingredient, liaisons__type='sortie').distinct()

    if not recettes.exists():
        valeur = 1
        chemin = [f"{quantite} x {ingredient.nom} (foreuse)"]
        cache[ingredient.id] = (valeur, chemin)
        return valeur, chemin

    meilleure_valeur = float("inf")
    meilleur_chemin = []

    for recette in recettes:
        entrees = recette.liaisons.filter(type='entree')
        sorties = recette.liaisons.filter(type='sortie')

        valeur_entree = 0
        sous_chemin = []

        for entree in entrees:
            v, c = calculer_valeur(entree.ingredient, entree.quantite, cache)
            valeur_entree += v * entree.quantite
            sous_chemin += c

        valeur_entree += recette.batiment.cout_valeur()

        quantite_sortie = next((s.quantite for s in sorties if s.ingredient == ingredient), 0)
        if quantite_sortie == 0:
            continue

        valeur_unitaire = valeur_entree / quantite_sortie

        if valeur_unitaire < meilleure_valeur:
            meilleure_valeur = valeur_unitaire
            meilleur_chemin = sous_chemin + [f"{quantite} x {ingredient.nom} via {recette.nom} (valeur={valeur_unitaire:.2f})"]

    cache[ingredient.id] = (meilleure_valeur, meilleur_chemin)
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

    ingredients = Ingredient.objects.all()
    return render(request, 'calculer_production.html', {
        'ingredients': ingredients,
        'resultat': resultat,
        'chemin': chemin,
    })