from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, search_recipes

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),             # Welcome page
    path('list/', RecipeListView.as_view(), name='recipe-list'),  # List of recipes
    path('list/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('search/', search_recipes, name='search-recipes'),
]