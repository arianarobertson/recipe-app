from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin  
from django.views.generic import ListView, DetailView       
from .models import Recipe                                  


def home(request):
    return render(request, 'recipes/welcome.html')


# 🔒 Protect CBVs with LoginRequiredMixin
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    login_url = '/login/'     # falls back to LOGIN_URL in settings.py if omitted
    redirect_field_name = 'next'


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    login_url = '/login/'
    redirect_field_name = 'next'
