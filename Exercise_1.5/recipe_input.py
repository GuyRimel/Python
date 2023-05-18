import pickle

# ask the user the recipe name, cooking time, and ingredients
# store the inputs in a dictionary and return the dictionary
def take_recipe():
  name = input('what is the recipe name? ')
  cooking_time = int(input('what is the recipe cooking time in minutes? (integer): '))
  ingredients = input('list all ingredients (separated by ", "): ').split(', ')
  difficulty = calc_difficulty(cooking_time, ingredients)
  recipe = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients,
    'difficulty': difficulty
  }

  return recipe


# parameters: cooking time (integer) and ingredients (list)
# return a difficulty string
def calc_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    return 'Easy'
  if cooking_time < 10 and len(ingredients) >= 4:
    return 'Medium'
  if cooking_time >= 10 and len(ingredients) < 4:
    return 'Intermediate'
  if cooking_time >= 10 and len(ingredients) >= 4:
    return 'Hard'


file_name = input('what is the file name?')

try:
  file_rb = open(file_name, 'rb')
  data = pickle.load(file_rb)

except FileNotFoundError:
  print('file not found!')
  data = {'recipes_list': [], 'all_ingredients': []}

except:
  print('unexpected error!')
  data = {'recipes_list': [], 'all_ingredients': []}

else:
  file_rb.close()

finally:
  print('the data is:', data)
  recipes_list = data['recipes_list']
  all_ingredients = data['all_ingredients']


num = ''

while not type(num) == int:
  try:
    num = int(input('how many recipes will you input? '))
  except:
    print('must be an integer!!!')

for i in range(num):
  recipe = take_recipe()

  recipes_list.append(recipe)

  for ingredient in recipe['ingredients']:
    if ingredient not in all_ingredients:
      all_ingredients.append(ingredient)


data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

with open(file_name, 'wb') as dump_file:
  pickle.dump(data, dump_file)