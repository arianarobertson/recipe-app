from django import forms
from .models import Recipe
from .models import Category, Tag
from ingredients.models import Ingredient
from .models import RecipeIngredient

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


class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Ingredients"
    )

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'prep_time', 'cook_time', 'instructions', 'image', 'categories', 'tags']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 6}),
        }

    def save(self, commit=True):
        # First, save the Recipe instance
        recipe = super().save(commit=False)

        if commit:
            recipe.save()

        # Now save the associated RecipeIngredients
        ingredients = self.cleaned_data.get('ingredients')
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity='1'  # Default quantity, you may modify based on your requirement
            )

        return recipe
