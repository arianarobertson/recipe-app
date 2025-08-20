from django.test import TestCase
from .models import Tag

class TagModelTest(TestCase):
    def setUp(self):
        Tag.objects.create(name='Vegan')

    def test_tag_str(self):
        vegan = Tag.objects.get(name='Vegan')
        self.assertEqual(str(vegan), 'Vegan')
