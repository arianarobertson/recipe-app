from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Recipe
from .models import Rating

class RatingModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='tester', password='pass123')
        recipe = Recipe.objects.create(
            name='Simple Salad',
            description='Fresh salad.',
            prep_time=10,
            cook_time=0,
            instructions='Mix veggies.'
        )
        Rating.objects.create(recipe=recipe, user=user, rating=4, comment='Very good!')

    def test_rating_str(self):
        rating = Rating.objects.get(rating=4)
        self.assertIn('Rating 4', str(rating))
