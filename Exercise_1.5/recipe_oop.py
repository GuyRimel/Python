class Recipe(object):
  all_ingredients = []

  def __init__(self):
    self.name = input('Enter the recipe name: ')
    self.ingredients = input('Enter all ingredients separated by ", ": ').split(', ')
    self.cooking_time = int(input('Enter the cooking time in minutes: '))
    self.difficulty = None

  def get_name(self):
    return self.name

  def set_name(self, new_name):
    self.name = new_name

  def get_cooking_time(self):
    return self.cooking_time

  def set_cooking_time(self, new_cooking_time):
    self.cooking_time = new_cooking_time

  def get_ingredients(self):
    return self.ingredients

  def add_ingredients(self, new_ingredients):
    self.update_all_ingredients()

  def calculate_difficulty(self):
    ings = len(self.ingredients)
    ct = self.cooking_time

    if ct < 10 and ings < 4:
      result = 'Easy'
    elif ct < 10 and ings >= 4:
      result = 'Medium'
    elif ct >= 10 and ings < 4:
      result = 'Intermediate'
    elif ct >= 10 and ings >= 4:
      result = 'Hard'
    
    self.difficulty = result

  def get_difficulty(self):
    if self.difficulty == None:
      self.calculate_difficulty()
    
    return self.difficulty

  def update_all_ingredients(self):
    # need a class variable called all_ingredients...
  

recipe_1 = Recipe()

print(recipe_1.get_difficulty())