import pickle

class Recipe(object):
  all_ingredients = []

  def __init__(self, name = 'no name', ingredients = [], cooking_time = -1):
    self.name = name
    self.ingredients = ingredients
    self.cooking_time = cooking_time
    self.difficulty = None

  def get_name(self):
    return self.name

  def set_name(self, new_name):
    self.name = new_name

  def ask_name(self):
    self.name = input('Enter the recipe name: ')

  def get_cooking_time(self):
    return self.cooking_time

  def set_cooking_time(self, new_cooking_time):
    self.cooking_time = new_cooking_time

  def ask_cooking_time(self):
    self.cooking_time = int(input('Enter the cooking time in minutes: '))

  def get_ingredients(self):
    return self.ingredients

  def ask_ingredients(self):
    self.ingredients = input('Enter all ingredients separated by ", ": ').split(', ')

  # takes a tuple or list, then adds them to self.ingredients[]
  def add_ingredients(self, new_ingredients):
    for ing in new_ingredients:
      self.ingredients.extend(ing)
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
    for ing in self.ingredients:
      if ing not in Recipe.all_ingredients:
        Recipe.all_ingredients.extend(ing)

  # this defines the whats returned when the recipe is called as a string type
  def __str__(self):
    ingredients_string = ''

    for e, ing in enumerate(self.ingredients):
      if e != len(self.ingredients) - 1:
        ingredients_string += ing + ', '
      else:
        ingredients_string += ing + '\n'
    
    output = '- - - - - - - - - - - - - - - - - - - - -\n' + \
    'Recipe Name: ' + self.name + '\n' + \
    'Cooking Time: ' + str(self.cooking_time) + '\n' + \
    'Ingredients: '+ ingredients_string + \
    'Difficulty: ' + self.get_difficulty() + '\n' + \
    '- - - - - - - - - - - - - - - - - - - - -\n'

    return output
  

# data is Recipe objects, search_term is the ingredient to search for
def recipe_search(data, search_term):
  for recipe in data:
    if search_term in recipe.ingredients:
      print(recipe)


recipe_0 = Recipe(name = 'Tea', ingredients = ['Tea Leaves', 'Sugar', 'Water'], cooking_time = 5)
recipe_1 = Recipe('Coffee', ['Coffee Powder', 'Sugar', 'Water'], 5)
recipe_2 = Recipe('Cake', ['Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk'], 50)
recipe_3 = Recipe('Banana Smoothie', ['Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes'], 5)

print('*** Printing a single recipe: ')
print(recipe_2)

recipes_list = [recipe_0, recipe_1, recipe_2, recipe_3]

print('*** Recipes containing "Water": ')
recipe_search(recipes_list, 'Water')

print('*** Recipes containing "Sugar": ')
recipe_search(recipes_list, 'Sugar')

print('*** Recipes containing "Bananas": ')
recipe_search(recipes_list, 'Bananas')