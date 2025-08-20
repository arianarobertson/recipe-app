from django.test import TestCase
from categories.models import Category
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient, RecipeCategory
from tags.models import Tag

class RecipeModelTest(TestCase):
    def setUp(self):
        # Create Category
        dessert = Category.objects.create(name='Dessert')
        main_course = Category.objects.create(name='Main Course')

        # Create Tags
        tag_easy = Tag.objects.create(name='Easy')
        tag_quick = Tag.objects.create(name='Quick')

        # Create Ingredients
        sugar = Ingredient.objects.create(name='Sugar', is_allergen=False)
        flour = Ingredient.objects.create(name='Flour', is_allergen=False)

        # Create Recipe
        recipe = Recipe.objects.create(
            name='Test Cake',
            description='A delicious test cake.',
            prep_time=15,
            cook_time=30,
            instructions='Mix ingredients and bake.'
        )

        # Add categories and tags
        recipe.categories.add(dessert)
        recipe.tags.add(tag_easy, tag_quick)

        # Add RecipeIngredient
        RecipeIngredient.objects.create(recipe=recipe, ingredient=sugar, quantity='1 cup')
        RecipeIngredient.objects.create(recipe=recipe, ingredient=flour, quantity='2 cups')

    def test_recipe_str(self):
        recipe = Recipe.objects.get(name='Test Cake')
        self.assertEqual(str(recipe), 'Test Cake')

    def test_recipeingredient_str(self):
        sugar = Ingredient.objects.get(name='Sugar')
        recipe = Recipe.objects.get(name='Test Cake')
        ri = RecipeIngredient.objects.get(recipe=recipe, ingredient=sugar)
        self.assertEqual(str(ri), '1 cup of Sugar for Test Cake')

    def test_categories_and_tags(self):
        recipe = Recipe.objects.get(name='Test Cake')
        self.assertEqual(recipe.categories.count(), 1)
        self.assertEqual(recipe.tags.count(), 2)
