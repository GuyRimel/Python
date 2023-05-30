import mysql.connector

conn = mysql.connector.connect(
  host='localhost',
  user='cf-python',
  passwd='password'
)

cursor = conn.cursor()

# only creates DB if it doesn't exist yet
cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')

cursor.execute('USE task_database')


# only creates TABLE if it doesn't exist yet
cursor.execute('''
  CREATE TABLE IF NOT EXISTS Recipes(
    id            INT PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(50),
    ingredients   VARCHAR(255),
    cooking_time  INT,
    difficulty    VARCHAR(20)
  )
''')

def create_recipe(conn, cursor):
  name = input('\nEnter the name of the recipe: ')
  cooking_time = int(input('Enter the cooking time (minutes): '))

  # recipe_ingredients is declared as an input string, split by commas, into an array
  recipe_ingredients = input('list all ingredients (separated by ", "): ').split(', ')
  difficulty = calc_difficulty(cooking_time, recipe_ingredients)

  # now that the difficulty is set, recipe_ingredients is joined into recipe_ingredients_string for SQL processing
  recipe_ingredients_string = ', '.join(recipe_ingredients)
  sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
  val = (name, recipe_ingredients_string, cooking_time, difficulty)

  cursor.execute(sql, val)
  conn.commit()
  print('\nRecipe created!')


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
    print('INPUT ERROR')
    difficulty_level = 'Unknown'

  return difficulty_level


def search_recipe(conn, cursor):
  cursor.execute('SELECT ingredients FROM Recipes')
  results = cursor.fetchall()

  print('======================================================')
  print('ALL INGREDIENTS\n')

  all_ings = []
  for ing_tuple in results:
    for ing in ing_tuple:
      ing_split = ing.split(', ')
      all_ings.extend(ing_split)
    
  for e, ing in enumerate(all_ings):
    print(str(e) + '. ' + ing)
  
  # all_ings is now a list of ingredient strings. Now, the user will input an integer
  # to search the DB for the ingredient at that index in all_ings[]
  
  print('======================================================')
  ing_searched = all_ings[int(input('Which ingredient # would you like to search recipes for?: '))]
  
  cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE '%" + ing_searched + "%'")
  results = cursor.fetchall()

  print('======================================================')
  print('SEARCH RESULTS FOR RECIPES WITH: "' + ing_searched.upper() + '"')
  for row in results:
    print('------------------------------------------------------')
    print('ID: ', row[0])
    print('Name: ', row[1])
    print('Ingredients: ', row[2])
    print('Cooking Time: ', row[3])
    print('Difficulty: ', row[4])
    print('------------------------------------------------------')

def update_recipe(conn, cursor):
  print('======================================================')
  print('UPDATE A RECIPE\n')

  # Display every recipe to the user
  view_all_recipes(conn, cursor)

  # Asks the user to input the ID of the recipe to be deleted
  id_for_update = input("\nEnter the ID of the recipe you want to UPDATE: ")

  # Ask the user if changing the recipe name
  isNameChanging = input('Change NAME of Recipe ' + id_for_update + '? (y/n): ')
  if isNameChanging.lower() == 'y':
    new_name = input("Enter the new name: ")
    cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, id_for_update))
    conn.commit()

  # Ask the user if changing the recipe cook time
  isCookTimeChanging = input('Change COOK TIME of Recipe ' + id_for_update + '? (y/n): ')
  if isCookTimeChanging.lower() == 'y':
    new_cooking_time = int(input("Enter the new cooking time in minutes: "))
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_cooking_time, id_for_update))
    conn.commit()

  # Ask the user if changing the recipe ingredients
  areIngredientsChanging = input('Change INGREDIENTS of Recipe ' + id_for_update + '? (y/n): ')
  if areIngredientsChanging.lower() == 'y':
    new_ings = input('List all ingredients (separated by ", "): ')
    cursor.execute("UPDATE Recipes SET ingredients = %s  WHERE id = %s", (new_ings, id_for_update))
    conn.commit()

  # If the user changed the cook time OR the ingredients, calc and update the difficulty
  if isCookTimeChanging == 'y' or areIngredientsChanging == 'y':
    cursor.execute('SELECT cooking_time, ingredients FROM Recipes WHERE id =' + id_for_update)
    results = cursor.fetchall()

    # results is currently a list with a tuple i.e. results = [( int(ct), list(ings) )]
    # which explains the nested indexes below
    ct = results[0][0]
    ings = results[0][1]
    new_difficulty = calc_difficulty(ct, ings)

    cursor.execute("UPDATE Recipes SET difficulty = %s  WHERE id = %s", (new_difficulty, id_for_update))
    conn.commit()

def delete_recipe(conn, cursor):
  print('======================================================')
  print('DELETE A RECIPE\n')

  # Display every recipe to the user
  view_all_recipes(conn, cursor)

  # Asks the user to input the ID of the recipe to be deleted
  id_for_deletion = int(input("\nEnter the ID of the recipe you want to delete: "))

  # Delete the corresponding recipe into result
  sql = "DELETE FROM Recipes WHERE id = " + str(id_for_deletion)
  cursor.execute(sql)

  # Commits changes made to the Recipes table
  conn.commit()
  print("\n* Recipe Deleted!")


def view_all_recipes(conn, cursor):
  print('======================================================')
  print('ALL RECIPES\n')
  print('------------------------------------------------------')

  cursor.execute('SELECT * FROM Recipes')
  results = cursor.fetchall()

  for row in results:
    print('ID: ', row[0])
    print('Name: ', row[1])
    print('Ingredients: ', row[2])
    print('Cooking Time: ', row[3])
    print('Difficulty: ', row[4])
    print('------------------------------------------------------')


# # # # # # # # # #
# USER INTERFACE

def main_menu(conn, cursor):
  choice = ''
  while (choice != 'quit'):
    print('======================================================')
    print('MAIN MENU\n')
    print('Choices:')
    print('1. Create a new recipe')
    print('2. Search for a recipe by ingredient')
    print('3. Update an existing recipe')
    print('4. Delete a recipe')
    print('5. View all recipes')
    print('Type "quit" to exit the program.')
    print('======================================================')

    choice = input('Your choice: ')

    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)
    elif choice == '5':
      view_all_recipes(conn, cursor)

main_menu(conn, cursor)
