from django.db import models

# Create your models here.

class Recipe(models.Model):
  name = models.CharField(max_length=50)
  cooking_time = models.PositiveIntegerField()
  ingredients = models.TextField(max_length=100)
  difficulty = models.CharField(max_length=50, default='Easy')

  def __str__(self):
    return str(self.name)
