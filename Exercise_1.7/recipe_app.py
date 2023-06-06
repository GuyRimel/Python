from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


# think of engine as the bridge connection between the SQL DB and this Python code
engine = create_engine("mysql://cf-python:password@localhost/my_database")

# Session is the class that binds to engine
Session = sessionmaker(bind=engine)

# session interacts with the DB
session = Session()

# Base is an object template from sqlalchemy used to create the Recipe class
Base = declarative_base()

class Recipe(Base):
  __tablename__ = "practice_recipes"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"

try:
  Base.metadata.create_all(engine)
except:
  print("Problem with: Base.metadata.create_all(engine)")


####################
### CREATE RECIPE
def create_recipe():
  print('======================================================================')
  print('CREATE RECIPE')
  print('======================================================================')
  
  # get the recipe NAME
  recipe_name = ''
  while not recipe_name:
    recipe_name = input('>>> Enter the new RECIPE NAME: ')

    if len(recipe_name) < 2 or len(recipe_name) > 50:
      print('### Try again! Name must be between 2 and 50 characters and alphanumeric.')
      recipe_name = ''

  # get the recipe COOKING TIME
  recipe_cooking_time = None
  while not recipe_cooking_time:
    try:
      recipe_cooking_time = int(input('>>> Enter the recipe COOK TIME (in minutes): '))
    except:
      print("### WRONG! Cooking time must be a number!")

  # get the recipe INGREDIENTS
  # recipe_ingredients is declared as an input string, split by commas, into an array
  recipe_ingredients = []
  while not recipe_ingredients or recipe_ingredients[0].isnumeric():
    recipe_ingredients = input('>>> List all ingredients (separated by ", "): ')

  recipe_ingredients = recipe_ingredients.split(', ')

  # calculate recipe difficulty with a cooking time (int) and recipe_ingredients (list)
  recipe_difficulty = calc_difficulty(recipe_cooking_time, recipe_ingredients)

  # now that the difficulty is set, recipe_ingredients is joined into recipe_ingredients_string for SQL processing
  recipe_ingredients_string = ', '.join(recipe_ingredients)

  recipe = Recipe(
    name = recipe_name,
    cooking_time = recipe_cooking_time,
    ingredients = recipe_ingredients_string,
    difficulty = recipe_difficulty
  )

  session.add(recipe)
  session.commit()

  return print('### Recipe created!')


# recipe_ingredients should come in as a list or tuple
def calc_difficulty(cooking_time, recipe_ingredients):
  if (cooking_time < 10) and (len(recipe_ingredients) < 4):
    difficulty_level = 'Easy'
  elif (cooking_time < 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = 'Medium'
  elif (cooking_time >= 10) and (len(recipe_ingredients) < 4):
    difficulty_level = 'Intermediate'
  elif (cooking_time >= 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = 'Hard'
  else:
    print('### INPUT ERROR')
    difficulty_level = 'Unknown'

  return difficulty_level


####################
# UPDATE RECIPE
def update_recipe():
  print('======================================================================')
  print('UPDATE RECIPE')
  print_all_recipes()

  recipe_id = None
  valid_ids = []
  
  # make a list of all currently available ids
  for id_tuple in session.query(Recipe.id).all():
    valid_ids.append(id_tuple[0])

  # if the user enters "back" they'll go back to the menu
  while not recipe_id in valid_ids:
    recipe_id = input('>>> Enter the ID of the recipe you\'d like to update (or go "back"): ')
    if recipe_id == 'back':
      return None

  # if id is not valid, keep looping
    try:
      recipe_id = int(recipe_id)
      if not recipe_id in valid_ids:
        print('### WRONG! There is no recipe with that ID!')

    except:
      print('### WRONG! Recipe ID must be an integer!')

  print('======================================================================')
  print('SELECTED RECIPE:')
  print_recipe(session.query(Recipe).filter(Recipe.id == recipe_id).one())
  print('----------------------------------------------------------------------')

  # update the recipe name
  name_is_changing = input('>>> Want to update the recipe NAME? (y/n): ').lower()

  if name_is_changing == 'y':
    new_name = ''
    while not new_name:
      new_name = input('>>> Enter the new NAME (or "back"): ')
      if new_name == 'back':
        return print('### Returning to main menu')
      if  len(new_name) < 1 or len(new_name) > 50:
        print('### Recipe name must be between 1 and 50 characters!')
      else:
        new_name = ''

    print('### Recipe name has been changed to "' + new_name + '".')
    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.name: new_name})

  # update the recipe cooking_time
  ct_is_changing = input('>>> Want to update the recipe COOK TIME? (y/n): ').lower()

  if ct_is_changing == 'y':
    new_ct = 0
    while not new_ct:
      try:
        new_ct = int(input('>>> Enter the new recipe COOK TIME (in minutes): '))
        break

      except:
        print("### WRONG! Cooking time must be a NUMBER.")
    
    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.cooking_time: new_ct})

  # update the recipe ingredients
  ings_are_changing = input('>>> Want to update the recipe INGREDIENTS? (y/n): ').lower()

  if ings_are_changing == 'y':
    new_ings = input('>>> Enter the new INGREDIENTS (separated by ", "): ').lower()
    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: new_ings})

  # if the cooking_time OR ingredients update, update the difficulty
  if ct_is_changing == 'y' or ings_are_changing == 'y':
    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).one()
    ct = recipe.cooking_time
    ings_list = recipe.ingredients.split(', ')
    new_difficulty = calc_difficulty(ct, ings_list)

    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: new_difficulty})

  session.commit()
  return print('### Recipe Updated!')


####################
# DELETE RECIPE
def delete_recipe():
  print('======================================================================')
  print('DELETE RECIPE')
  print_all_recipes()

  recipe_id = None
  recipe_obj = None

  while not recipe_id:

    recipe_id = input('>>> Enter the ID of the recipe you\'d like to delete (or go "back"): ')
    if recipe_id == 'back':
      return None

    else:
      try:
        recipe_obj = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        break

      except:
        print('### WRONG! There is no recipe with that id!')
        recipe_id = None
  
  print('======================================================================')
  print('SELECTED RECIPE:')
  print_recipe(recipe_obj)

  will_delete = input('Are your SURE you want to delete "' + recipe_obj.name + '"? (y/n): ')
  if will_delete == 'y':
    session.delete(recipe_obj)
    session.commit()
    return print('### Recipe deleted!')
  else:
    print('### Fear not. Nothing was deleted.')
    return None

####################
# SEARCHING FOR RECIPES BY MULTIPLE INGREDIENTS IS COMPLICATED
# here are the basic logical steps:
#
# 01. collect all ingredients from all recipes (duplicates included) (unfiltered_ingredients)
# 02. filter out duplicate values. Now we've got a list of all unique ingredients (all_ingredients)
# 03. enumerate and list all unique ingredients for the user to input which ingredient(s) to search with (ings_searched)
# 04. user input (ings searched) comes in as a string, of integers, separated by spaces... yes. e.g. "1 5 13"
# 05. split the user input by spaces and push the values into a list (ings_searched_str_list) e.g. ['1', '5', '13']
# 06. NOW THEN. loop through ings_searched_str_list and try to convert each to an integer. pass each integer as an index
#     of the all_ingredients list, and push that ingredient string into a list (ings_searched_list) e.g. ['water', 'sugar', 'lemon']
# 07. the final desired outcome is a list of filtered recipes. This list variable is declared (filtered_recipes) and starts with the value of ALL recipes
# 08. for each ingredient searched, loop through each recipe. If the recipe does NOT include one of the searched ingredients, that recipe is removed.
# 09. What you end up with is only recipes that include ALL of the searched ingredients e.g. "Lemonade"
# 10. Loop through the filtered recipe and print each one
# Note: case-sensitive
def search_recipes_by_ingredients():
  print('======================================================================')
  print('SEARCH RECIPES BY INGREDIENTS')
  if session.query(Recipe).count() < 1:
    return print("### There are no recipes to search yet! - going back to main menu")

  results = session.query(Recipe.ingredients).all()

  # 01. collect all ingredients from all recipes (duplicates included) (unfiltered_ingredients)
  unfiltered_ingredients = []

  for recipe_ingredients_list in results:
    for recipe_ingredients in recipe_ingredients_list:
      recipe_ingredient_split = recipe_ingredients.split(", ")
      unfiltered_ingredients.extend(recipe_ingredient_split)

  # 02. filter out duplicate values. Now we've got a list of all unique ingredients (all_ingredients)
  all_ingredients = []
  for ing in unfiltered_ingredients:
    if ing not in all_ingredients:
      all_ingredients.append(ing)

  # 03. enumerate and list all unique ingredients for the user to input which ingredient(s) to search with (ings_searched)
  print('ALL INGREDIENTS:')
  print('----------------------------------------------------------------------')
  for e, ing in enumerate(all_ingredients):
    print(str(e) + '.) ' + ing)

  # 04. user input (ings searched) comes in as a string, of integers, separated by spaces... yes. e.g. "1 5 13"
  ings_searched = ''
  while not ings_searched:
    ings_searched = input('Input one or more ingredient numbers separated by a space to search (or go "back"): ')

    if ing_searched == "back":
      return None

  # 05. split the user input by spaces and push the values into a list (ings_searched_str_list) e.g. ['1', '5', '13']
  ings_searched_str_list = ings_searched.split(' ')

  # 06. NOW THEN. loop through ings_searched_str_list and try to convert each to an integer. pass each integer as an index
  #     of the all_ingredients list, and push that ingredient string into a list (ings_searched_list) e.g. ['water', 'sugar', 'lemon']
  ings_searched_list = []

  for ing in ings_searched_str_list:
    try:
      ing = all_ingredients[int(ing)]
      ings_searched_list.append(ing)
    except:
      return print('### Something BROKE. Going back to main menu.')

  # 07. the final desired outcome is a list of filtered recipes. This variable is declared (filtered_recipes) and starts with the value of all recipes (list)
  filtered_recipes = session.query(Recipe).all()

  # 08. for each ingredient searched, loop through each recipe. If the recipe does NOT include one of the searched ingredients, that recipe is removed.
  for ing_searched in ings_searched_list:
    for recipe in filtered_recipes:
      if ing_searched not in recipe.ingredients:
        filtered_recipes.remove(recipe)

  # 09. What you end up with is only recipes that include ALL of the searched ingredients e.g. "Lemonade"
  print('SEARCH RESULTS:')
  print('RECIPES CONTAINING: ', ings_searched_list)
# 10. try and loop through the filtered recipes and print each one
  try:
    for recipe in filtered_recipes:
      print_recipe(recipe)
  except:
    print('Something went wrong! Returning to the main menu.')


####################
# MAIN MENU
def show_main_menu():
  def print_menu():
    print('======================================================================')
    print('BEST RECIPES EVER! (CLI): MAIN MENU')
    print('======================================================================')
    print('1. Create a new recipe ("new")')
    print('2. View all recipes ("all")')
    print('3. Search for a recipe by ingredients ("search")')
    print('4. Update a recipe ("update")')
    print('5. Delete a recipe ("delete")')
    print('6. Quit ("quit")')
    print('----------------------------------------------------------------------')
  
  user_selection = None

  # Here's the main loop. If ever a user enters '6' or 'quit' (at this menu) they'll exit the program
  while user_selection != '6' or user_selection != 'quit':
    print_menu()
    user_selection = input('>>> Enter a number or command: ').lower()

    if user_selection == '1' or user_selection == 'new':
      create_recipe()
    elif user_selection == '2' or user_selection == 'all':
      print_all_recipes()
    elif user_selection == '3' or user_selection == 'search':
      search_recipes_by_ingredients()
    elif user_selection == '4' or user_selection == 'update':
      update_recipe()
    elif user_selection == '5' or user_selection == 'delete':
      delete_recipe()
    elif user_selection == '6' or user_selection == 'quit':
      print("### Goodbye, Chef!")
      break
    else:
      print('### WRONG! Valid numbers are 1, 2, 3, 4, 5, or 6. Valid commands are single words in parentheses.')


def print_all_recipes():
  recipes_list = session.query(Recipe).all()
  print('======================================================================')
  print('ALL RECIPES')
  for e, recipe in enumerate(recipes_list):
    print('----------------------------------------------------------------------')
    print("Recipe ID:\t", recipe.id)
    print("Recipe Name:\t", recipe.name)
    print("Ingredients:\t", recipe.ingredients)
    print("Cooking Time:\t", recipe.cooking_time)
    print("Difficulty:\t", recipe.difficulty)


def print_recipe(recipe):
  print('----------------------------------------------------------------------')
  print("Recipe ID:\t", recipe.id)
  print("Recipe Name:\t", recipe.name)
  print("Ingredients:\t", recipe.ingredients)
  print("Cooking Time:\t", recipe.cooking_time)
  print("Difficulty:\t", recipe.difficulty)

show_main_menu()