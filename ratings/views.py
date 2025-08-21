from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Rating

class RatingListView(ListView):
    model = Rating
    template_name = 'ratings/list.html'

class RatingDetailView(DetailView):
    model = Rating
    template_name = 'ratings/detail.html'

