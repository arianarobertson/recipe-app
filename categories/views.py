from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category

class CategoryListView(ListView):
    model = Category
    template_name = 'categories/list.html'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/detail.html'
