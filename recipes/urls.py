from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, search_recipes
from .import views

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),             # Welcome page
    path('list/', RecipeListView.as_view(), name='recipe-list'),  # List of recipes
    path('list/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/<int:pk>/love/', views.love_recipe, name='love-recipe'),
    path('search/', search_recipes, name='search-recipes'),
    path('add/', views.add_recipe, name='add-recipe'),
    path('about/', views.about_me, name='about-me'),
    path('hearted/', views.hearted_recipes, name='hearted-recipes'),
]