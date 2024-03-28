import json
import os
import requests
from urllib.parse import quote
import time
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__name__), '..', '.env')  # Assuming .env is located one level up
load_dotenv(dotenv_path)

api_key = os.environ.get('GOOGLE_API_KEY')
cx = os.environ.get('CX')

# Load recipes from JSON file
with open('recipes.json', 'r') as file:
    recipes = json.load(file)

# Function to search for image URL using Google Custom Search API
def get_image_urls(title, max_urls=3):
    try:
        query = quote(title)
        url = f'https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}&searchType=image'
        print(url)

        # Send GET request to Google Custom Search API
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad responses

        # Parse JSON response
        data = response.json()
        image_urls = []
        if 'items' in data and data['items']:
            for i in range(max_urls):
                image_url = data['items'][i]['link']
                image_urls.append(image_url)
            return image_urls
        
    except Exception as e:
        print(f"Error fetching image for '{title}': {e}")
    return None

# Function to download and save image
def download_image(image_urls, filename, retry_delay=1):
    for image_url in image_urls:
        try:
            # Send GET request to download image
            response = requests.get(image_url)
            response.raise_for_status()  # Raise exception for bad responses

            # Save image to file
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded image for '{filename}'")
            return  # Exit the function if successful
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                print(f"Access forbidden for '{filename}': {e}")
                time.sleep(retry_delay)  # Delay before retrying
            else:
                print(f"Error downloading image for '{filename}': {e}")
                return  # Exit the function on other errors
        except Exception as e:
            print(f"Error downloading image for '{filename}': {e}")
            return  # Exit the function on other errors

    print(f"Max retries reached for '{filename}'")

# Create directory to save images if it doesn't exist
os.makedirs('images', exist_ok=True)

# Loop through recipes
for recipe in recipes:
    title = recipe['recipe']['title']
    image_urls = get_image_urls(title)
    if image_urls:
        # Extract image filename from URL
        image_filename = os.path.join('images', f'{title.replace(" ", "_")}.jpg')
        # Download and save image
        download_image(image_urls, image_filename)
    else:
        print(f"No image found for '{title}'")

