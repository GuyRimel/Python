import pickle

# parameters:
#   recipe = dictionary
def display_recipe(recipe):
  print('- - - - - - - - - - - - - - -\n')
  for key in recipe:
    print(str(key), ': ', recipe[key], '\n')
  print('- - - - - - - - - - - - - - -\n')

# parameters:
#   data = dictionary
def search_ingredient(data):
  all_ingredients = data['all_ingredients']
  recipes_list = data['recipes_list']
  print('- - - - - - - - - - - - - - -')
  print('ALL INGREDIENTS')
  for e, i in enumerate(all_ingredients):
    print(e,': ', i)
  print('- - - - - - - - - - - - - - -\n')

  try:
    ingredient_searched = all_ingredients[int(input('Which ingredient number? (integer): '))]

  except:
    print('ERROR!')

  else:
    for recipe in recipes_list:
      if ingredient_searched in recipe['ingredients']:
        display_recipe(recipe)

file_rb = open('thing.bin', 'rb')
data = pickle.load(file_rb)

search_ingredient(data)