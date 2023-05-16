import pickle

def take_recipe():
  name = input('what is the recipe name? ')
  cooking_time = int(input('what is the recipe cooking time in minutes? (integer): '))
  ingredients = input('list all ingredients (separated by ", "): ')
  calc_difficulty()

def calc_difficulty():
  print('that is hard!')

take_recipe()