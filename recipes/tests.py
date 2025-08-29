from django.test import TestCase, Client
from django.urls import reverse
from categories.models import Category
from django.contrib.auth.models import User
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient
from tags.models import Tag
from .forms import RecipeSearchForm
from .models import Recipe

# ----------------------------
# Recipe Model Tests
# ----------------------------
class RecipeModelTest(TestCase):
    def setUp(self):
        dessert = Category.objects.create(name='Dessert')
        tag_easy = Tag.objects.create(name='Easy')
        sugar = Ingredient.objects.create(name='Sugar', is_allergen=False)

        self.recipe = Recipe.objects.create(
            name='Test Cake',
            description='A delicious test cake.',
            prep_time=15,
            cook_time=30,
            instructions='Mix ingredients and bake.'
        )
        self.recipe.categories.add(dessert)
        self.recipe.tags.add(tag_easy)
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=sugar, quantity='1 cup')

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Test Cake')

    def test_recipeingredient_str(self):
        ri = RecipeIngredient.objects.get(recipe=self.recipe)
        self.assertEqual(str(ri), '1 cup of Sugar for Test Cake')

    def test_categories_and_tags(self):
        self.assertEqual(self.recipe.categories.count(), 1)
        self.assertEqual(self.recipe.tags.count(), 1)

# ----------------------------
# Recipe Form Tests
# ----------------------------
class RecipeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Breakfast")
        cls.tag = Tag.objects.create(name="Easy")

    def test_form_fields_exist(self):
        form = RecipeSearchForm()
        self.assertIn('recipe_name', form.fields)
        self.assertIn('categories', form.fields)
        self.assertIn('tags', form.fields)
        self.assertIn('ingredient', form.fields)
        self.assertIn('chart_type', form.fields)

    def test_form_accepts_valid_data(self):
        form_data = {
            'recipe_name': 'Pancakes',
            'categories': self.category.id,
            'tags': self.tag.id,
            'ingredient': 'flour',
            'chart_type': '#1',
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

def test_recipe_form_submission(self):
    self.user = User.objects.create_user(username='tester', password='testpass')
    self.client.login(username='tester', password='testpass')

    category = Category.objects.create(name='Test Category')
    tag = Tag.objects.create(name='Test Tag')
    ingredient = Ingredient.objects.create(name='Flour', is_allergen=False)

    response = self.client.post('/recipes/add/', {
        'name': 'Test Recipe',
        'description': 'Test description',
        'prep_time': 10,
        'cook_time': 15,
        'instructions': 'Test instructions',
        'categories': [category.id],
        'tags': [tag.id],
        'ingredients': [ingredient.id], 
    })

    if response.status_code != 302:
        print("\nForm errors:")
        print(response.context['form'].errors)

    self.assertEqual(response.status_code, 302)  # Expecting redirect after successful submission




# ----------------------------
# Recipe Views Tests
# ----------------------------
class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='pass1234')
        
        # Create test category and tag
        cls.category = Category.objects.create(name="Breakfast")
        cls.tag = Tag.objects.create(name="Easy")
        
        # Create test recipe with required fields
        cls.recipe = Recipe.objects.create(
            name="Pancakes",
            description="Delicious pancakes",
            prep_time=10,   # prep time in minutes
            cook_time=5,    # cook time in minutes
            instructions="Mix and fry."
        )
        cls.recipe.categories.add(cls.category)
        cls.recipe.tags.add(cls.tag)

    def setUp(self):
        self.client = Client()

    def test_home_view_accessible(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_requires_login(self):
        response = self.client.get(reverse('recipes:recipe-list'))
        self.assertRedirects(response, '/login/?next=' + reverse('recipes:recipe-list'))

    def test_list_view_logged_in(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('recipes:recipe-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pancakes")

    def test_search_view_requires_login(self):
        response = self.client.get(reverse('recipes:search-recipes'))
        self.assertRedirects(response, '/login/?next=' + reverse('recipes:search-recipes'))

    def test_search_view_filters_by_category(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(reverse('recipes:search-recipes'), {'categories': self.category.id})
        self.assertContains(response, "Pancakes")

    def test_search_view_filters_by_tag(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(reverse('recipes:search-recipes'), {'tags': self.tag.id})
        self.assertContains(response, "Pancakes")

    def test_search_view_filters_by_name(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(reverse('recipes:search-recipes'), {'recipe_name': 'Pancakes'})
        self.assertContains(response, "Pancakes")

# ----------------------------
# Love Recipe Test
# ----------------------------
class RecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            description="Test Description",
            prep_time=5,
            cook_time=10,
            instructions="Test instructions"
        )

    def test_love_recipe(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('recipes:love-recipe', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects after loving the recipe
        self.assertTrue(self.recipe in self.user.loved_recipes.all())
