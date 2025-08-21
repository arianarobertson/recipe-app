from django.test import TestCase
from .models import Recipe
from categories.models import Category
from tags.models import Tag

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create categories and tags if needed
        category = Category.objects.create(name="Dessert")
        tag = Tag.objects.create(name="Sweet")

        # Create a recipe without ingredients, servings, or cuisine fields
        cls.recipe = Recipe.objects.create(
            name="Test Recipe",
            description="A delicious test recipe",
            prep_time=15,
            cook_time=30,
            instructions="Mix all ingredients and cook.",
        )
        # Add many-to-many relationships after creating the recipe
        cls.recipe.categories.add(category)
        cls.recipe.tags.add(tag)

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, "Test Recipe")
        self.assertEqual(self.recipe.prep_time, 15)
        self.assertEqual(self.recipe.cook_time, 30)
        self.assertEqual(self.recipe.categories.first().name, "Dessert")
        self.assertEqual(self.recipe.tags.first().name, "Sweet")
