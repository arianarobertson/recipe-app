from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Ingredient

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/list.html'

class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'ingredients/detail.html'

