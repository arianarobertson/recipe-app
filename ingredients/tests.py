from django.test import TestCase
from .models import Ingredient

class IngredientModelTest(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='Salt', is_allergen=False)

    def test_ingredient_str(self):
        salt = Ingredient.objects.get(name='Salt')
        self.assertEqual(str(salt), 'Salt')
