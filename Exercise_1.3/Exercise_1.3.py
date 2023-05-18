global_recipes_list = []
global_ingredients_list = []

def take_recipe(name = '', cooking_time = -1, ingredients = []):
  if not name:
    name = input('what is the name of this recipe?: ')
  if cooking_time < 0:
    cooking_time = int(input('what is the recipe cooking time in minutes? (integer): '))
  if ingredients == []:
    total_ingredients = int(input('how many ingredients? (integer): '))

    for e, i in enumerate(range(total_ingredients), start = 1):
      i = input('what is ingredient #' + str(e) + ': ')
      ingredients.append(i)
    
  for ingredient in ingredients:
    if ingredient not in global_ingredients_list:
      global_ingredients_list.append(ingredient)

  recipe = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients
  }

  for ingredient in ingredients:
    if not ingredient in global_ingredients_list:
      global_ingredients_list.append(ingredient)
  
  global_recipes_list.append(recipe)

  return recipe

def assign_recipe_difficulties():
  for recipe in global_recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
      recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
      recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
      recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
      recipe['difficulty'] = 'Hard'

def print_recipes():
  print('current global recipes list:',global_recipes_list)

def print_ingredients():
  print('current global_ingredients are:',global_ingredients_list)

n = int(input('How many recipes will you enter?: '))

for i in range(n):
  recipe = take_recipe()

assign_recipe_difficulties()

print_recipes()

print_ingredients()