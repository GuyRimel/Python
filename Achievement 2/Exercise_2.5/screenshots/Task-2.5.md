# Task 2.5: Model Changes

Here's a list of changes to the Django "Recipe" model used in Best Recipes Ever:

- Cooking Time now has the help text "in minutes"
  Reasoning: it's helpful

- Added "Genre", with a dropdown of possible genres
  Reasoning: can't have 1 million different genres. keep it to a dropdown.

- "Rating" is now a float (for future calculations)
  Reasoning: much later... this will be a calculated value based on all users' rating input

- Removed "Difficulty".
  Reasoning: Duh, this is a calculated value, not an input value


Also a big change was to delete the "Ingredients" app from the project. This would get complicated, so I'm scratching it for the sake of my precious time and sanit.