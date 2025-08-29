from django.db import models
from django.urls import reverse
from ingredients.models import Ingredient
from categories.models import Category
from tags.models import Tag
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipes', default='no_image.jpg')  # <-- NEW
    categories = models.ManyToManyField(Category, through='RecipeCategory')
    tags = models.ManyToManyField(Tag, blank=True)
    # Relationship to track "loved" recipes
    loved_by = models.ManyToManyField(User, related_name='loved_recipes', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:recipe-detail', kwargs={'pk': self.pk})

    def total_time(self):
        return self.prep_time + self.cook_time

    def difficulty(self):
        time = self.total_time()
        num_ingredients = self.recipe_ingredients.count()
        if time < 30 and num_ingredients < 5:
            return "Easy"
        elif time < 60 and num_ingredients < 10:
            return "Medium"
        else:
            return "Hard"

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
