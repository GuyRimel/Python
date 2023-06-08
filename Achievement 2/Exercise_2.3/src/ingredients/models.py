from django.db import models

# Create your models here.

ingredient_category_choices = (
  ('other', 'Other'),
  ('meat', 'Meat'),
  ('fruit', 'Fruit'),
  ('veggie', 'Veggie'),
  ('dry', 'Dry Seasoning/Powders'),
  ('wet', 'Liquids/Oils'),
  ('sauce', 'Sauce'),
  ('dairy', 'Dairy'),
  ('grain', 'Rice/Pasta'),
  ('product', 'Off-the-Shelf')
)

class Ingredient(models.Model):
  name = models.CharField(max_length=50)
  category = models.CharField(max_length=50, choices=ingredient_category_choices)

  def __str__(self):
    return str(self.name)