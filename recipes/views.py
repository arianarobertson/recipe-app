from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Recipe, Category, Tag
from .forms import RecipeSearchForm
from .forms import RecipeForm
from .utils import get_chart


def home(request):
    """Welcome page view"""
    return render(request, 'recipes/welcome.html')


# 🔒 Protected CBVs
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    login_url = '/login/'
    redirect_field_name = 'next'


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    login_url = '/login/'
    redirect_field_name = 'next'


# ------------------------------
# Search View
# ------------------------------
@login_required(login_url='/login/')
def search_recipes(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_qs = Recipe.objects.none()  # default empty queryset
    chart = None

    if request.method == 'POST' and form.is_valid():
        recipe_name = form.cleaned_data.get('recipe_name')
        category = form.cleaned_data.get('categories')
        ingredient = form.cleaned_data.get('ingredient')
        tag = form.cleaned_data.get('tags')
        chart_type = form.cleaned_data.get('chart_type')

        # Start with all recipes and filter step by step
        recipes_qs = Recipe.objects.all()

        if recipe_name:
            recipes_qs = recipes_qs.filter(name__icontains=recipe_name)

        if category:
            recipes_qs = recipes_qs.filter(categories=category)  # exact M2M filter

        if tag:
            recipes_qs = recipes_qs.filter(tags=tag)  # exact M2M filter

        if ingredient:
            recipes_qs = recipes_qs.filter(recipe_ingredients__ingredient__name__icontains=ingredient)

        recipes_qs = recipes_qs.distinct()

        # Generate chart if there are results
        if recipes_qs.exists():
            chart = get_chart(chart_type, recipes_qs)

    context = {
        'form': form,
        'recipes': recipes_qs,
        'chart': chart
    }
    return render(request, 'recipes/search.html', context)

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes:recipe-list')
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})

def about_me(request):
    return render(request, 'recipes/about_me.html')

def love_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.user.is_authenticated:
        if recipe in request.user.loved_recipes.all():
            # User has already loved this recipe, so we "unlove" it
            request.user.loved_recipes.remove(recipe)
        else:
            # User loves this recipe
            request.user.loved_recipes.add(recipe)
        return redirect('recipes:recipe-detail', pk=recipe.pk)
    else:
        return redirect('login')  # Redirect to login if user is not authenticated
    
def hearted_recipes(request):
    if request.user.is_authenticated:
        hearted_recipes = request.user.loved_recipes.all()
        return render(request, 'recipes/hearted_recipes.html', {'hearted_recipes': hearted_recipes})
    else:
        return redirect('login')  # Redirect to login if user is not authenticated


