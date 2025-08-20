from django.test import TestCase
from .models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name='Appetizer')

    def test_category_str(self):
        appetizer = Category.objects.get(name='Appetizer')
        self.assertEqual(str(appetizer), 'Appetizer')
