from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Tag

class TagListView(ListView):
    model = Tag
    template_name = 'tags/list.html'

class TagDetailView(DetailView):
    model = Tag
    template_name = 'tags/detail.html'

