from django.shortcuts import render
from django.views.generic import ListView
from .models import Recipe
from django.views.generic import DetailView

def home(request):
    return render(request, 'recipes/welcome.html')

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'

