from django.db import models
from ingredients.models import Ingredient
from categories.models import Category
from tags.models import Tag

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='RecipeCategory')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.name}"

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe.name} in category {self.category.name}"
