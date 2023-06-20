# Designing the Recipe Search

I don't want the user to have freedom for configuring the charts. I've set up 3 insightful charts to choose from in a dropdown. It's simpler. Custom configured charts would be a headache.

In the Recipes Table, I've decided to display ALL the recipes in a dataframe table.

Then, I've provided inputs to filter the table results by name, and/or by ingredients with JavaScript.

The reasoning for this is that when a user clicks "Generate" a POST request reloads the page and would clear the recipe filtering input field. I don't want the POST request causing the page to constantly reload. That's sluggish, unresponsive, and not practical. With JS filtering the table, the results change instantly with any field input.

That's why the recipes table should be filtered with JavaScript, not QuerySet.