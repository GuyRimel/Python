from django.test import TestCase
from .models import Ingredient

# Create your tests here.

class IngredientModelTest(TestCase):
  def setUpTestData():
    # Set up non-modified objects used by all test methods
    Ingredient.objects.create(
      name='Celery',
      category='veggie'
    )

  def test_ingredient_name(self):
    # Get an ingredient object to test
    ing = Ingredient.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its data
    field_label = ing._meta.get_field('name').verbose_name

    # Compare the value to the expected result
    self.assertEqual(field_label, 'name')

  def test_ingredient_name_max_length(self):
    # Get an ingredient object to test
    ing = Ingredient.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its max_length
    max_length = ing._meta.get_field('name').max_length

    # Compare the value to the expected result i.e. 50
    self.assertEqual(max_length, 50)