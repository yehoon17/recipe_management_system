import json
import re

# Function to convert fractions to decimals
def fraction_to_decimal(match):
    fraction = match.group(0)
    parts = fraction.split('/')
    if len(parts) == 2:
        try:
            result = float(parts[0]) / float(parts[1])
            return str(result)
        except ZeroDivisionError:
            pass
    return fraction

# Load JSON file
with open('recipes_fraction.json', 'r') as file:
    data = file.read()

# Find and replace fractions with decimals
modified_data = re.sub(r'\d+/\d+', fraction_to_decimal, data)

# Write modified data back to JSON file
with open('recipes.json', 'w') as file:
    file.write(modified_data)

print("Fractions converted to decimals and saved in 'output.json'.")
