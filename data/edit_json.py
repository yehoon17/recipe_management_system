import json

if __name__ == '__main__':
    # Load JSON file
    with open('recipes.json', 'r') as file:
        original_data = json.load(file)

    # Removing the 'recipe' key from each dictionary
    updated_data = [recipe["recipe"] for recipe in original_data]
    
    # Writing the updated data back to the file
    with open('updated_recipes.json', 'w') as file:
        json.dump(updated_data, file, indent=2)
