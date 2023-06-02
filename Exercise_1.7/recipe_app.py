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


def create_recipe():
  print('======================================================================')
  print('CREATE RECIPE')
  print('======================================================================')
  
  recipe_name = input('>>> Enter the recipe NAME: ')
  recipe_cooking_time = None

  while not recipe_cooking_time:
    try:
      recipe_cooking_time = int(input('>>> Enter the recipe COOK TIME (in minutes): '))
    except:
      print("### WRONG! Cooking time must be an integer.")


  # recipe_ingredients is declared as an input string, split by commas, into an array
  recipe_ingredients = input('>>> List all ingredients (separated by ", "): ').split(', ')
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

  print('### Recipe created!')


def update_recipe():
  print('======================================================================')
  print('UPDATE RECIPE')
  print_all_recipes()

  recipe_id = None
  valid_ids = []
  
  for id_tuple in session.query(Recipe.id).all():
    valid_ids.append(id_tuple[0])

  print(valid_ids)

  while not recipe_id in valid_ids:
    recipe_id = input('>>> Enter the ID of the recipe you\'d like to update (or go "back"): ')
    if recipe_id == 'back':
      return show_main_menu()

    try:
      recipe_id = int(recipe_id)
      if not recipe_id in valid_ids:
        print('### WRONG! There is no recipe with that ID!')

    except:
      print('### WRONG! Recipe ID must be an integer!')


  print('======================================================================')
  print('SELECTED RECIPE:')
  print_recipe(session.query(Recipe).filter(Recipe.id == recipe_id).one())

  # update the recipe name
  name_is_changing = input('>>> Want to update the recipe NAME? (y/n): ').lower()

  if name_is_changing == 'y':
    new_name = input('>>> Enter the new NAME: ')
    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.name: new_name})

  # update the recipe cooking_time
  ct_is_changing = input('>>> Want to update the recipe COOK TIME? (y/n): ').lower()

  if ct_is_changing == 'y':
    new_ct = None
    while not new_ct:
      try:
        new_ct = int(input('>>> Enter the new recipe COOK TIME (in minutes): '))
        break

      except:
        print("### WRONG! Cooking time must be an integer.")
    
    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.cooking_time: new_ct})

  # update the recipe ingredients
  ings_are_changing = input('>>> Want to update the recipe INGREDIENTS? (y/n): ').lower()

  if ings_are_changing == 'y':
    new_ings = input('>>> Enter the new INGREDIENTS (separated by ", "): ')
    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: new_ings})

  # if the cooking_time OR ingredients update, update the difficulty
  if ct_is_changing == 'y' or ings_are_changing == 'y':
    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).one()
    ct = recipe.cooking_time
    ings_list = recipe.ingredients.split(', ')
    new_difficulty = calc_difficulty(ct, ings_list)

    session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.difficulty: new_difficulty})

  session.commit()
  print('### Recipe Updated!')


def delete_recipe():
  print('======================================================================')
  print('DELETE RECIPE')
  print_all_recipes()

  recipe_id = None
  recipe_obj = None

  while not recipe_id:

    recipe_id = input('>>> Enter the ID of the recipe you\'d like to delete (or go "back"): ')
    if recipe_id == 'back':
      return show_main_menu()

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
    print('### Recipe deleted!')
  else:
    print('### Fear not. Nothing was deleted.')



def search_recipes_by_ingredients():
  print('======================================================================')
  print('SEARCH RECIPES BY INGREDIENTS')


def show_main_menu():
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

  while user_selection is not '6' or user_selection is not 'quit':
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
    if e + 1 == len(recipes_list):
      print('----------------------------------------------------------------------')


def print_recipe(recipe):
  print('----------------------------------------------------------------------')
  print("Recipe ID:\t", recipe.id)
  print("Recipe Name:\t", recipe.name)
  print("Ingredients:\t", recipe.ingredients)
  print("Cooking Time:\t", recipe.cooking_time)
  print("Difficulty:\t", recipe.difficulty)
  print('----------------------------------------------------------------------')


def get_recipe(id):
  return session.query(Recipe).get(id)


def filter_recipe_by_name(name):
  return session.query(Recipe).filter(Recipe.name == name).one()


def filter_recipes_by_name(name):
  return session.query(Recipe).filter(Recipe.name == name).all()


def filter_recipes_by_ingredient(ing):
  return session.query(Recipe).filter(Recipe.ingredients.like('%' + ing + '%')).all()

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

show_main_menu()