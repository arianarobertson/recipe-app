from django import forms
from .models import Category, Tag

CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
)

class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(
        max_length=120, 
        label="Recipe Name", 
        required=False
    )
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False,
        label="Category"
    )
    ingredient = forms.CharField(
        max_length=120, 
        label="Ingredient", 
        required=False
    )
    tags = forms.ModelChoiceField(
        queryset=Tag.objects.all(), 
        required=False,
        label="Tag"
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        label="Chart Type",
        required=False
    )
