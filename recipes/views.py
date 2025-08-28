from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Recipe, Category, Tag
from .forms import RecipeSearchForm
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
