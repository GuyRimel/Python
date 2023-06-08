from django.test import TestCase
from .models import Recipe

# Create your tests here.

class RecipeModelTest(TestCase):
  def setUpTestData():
    # Set up non-modified objects used by all test methods
    Recipe.objects.create(
      name = 'Tasty Cito Salsa',
      cooking_time = 9,
      ingredients = ['tomato', 'onion', 'jalepeno'],
    )

  def test_recipe_name(self):
    # Get a recipe object to test
    ing = Recipe.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its data
    field_label = ing._meta.get_field('name').verbose_name

    # Compare the value to the expected result
    self.assertEqual(field_label, 'name')

  def test_recipe_name_max_length(self):
    # Get a recipe object to test
    ing = Recipe.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its max_length
    max_length = ing._meta.get_field('name').max_length

    # Compare the value to the expected result i.e. 50
    self.assertEqual(max_length, 50)