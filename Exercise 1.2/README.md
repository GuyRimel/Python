# Learning Python with CareerFoundry

## Excercise 1.2

### Recipe Structure Type and Justification
The data required for a recipe would best be stored in a Python 'dictionary', which is like an object with key/value pairs. The keys would be the names of the data being held such as "name" which would store the value of a string, "cooking_time" which would hold the value of an integer, and "ingredients" which would store a list of strings (ingredients). Retrieving data from a dictionary would allow for more natural logical syntax, for example ```recipe_1['name']``` would output ```'Tea'```.

### All Recipes Structure Type and Justification
All of the recipes (dictionaries) would best be held in an array (list). This would allow for simpler deletion of a recipe, or insertion of a new recipe, or sorting, as opposed to a more static tuple.