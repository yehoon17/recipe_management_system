import requests
import json
import random


URL = 'http://localhost:8000/graphql/'  


def get_all_user_id():
    query = '''
        query {
            allUsers(isSuperuser: false) {
                id
            }
        }
    '''

    response = requests.post(URL, json={'query': query})

    # Process response  
    user_id_list = []
    if response.status_code == 200:
        data = response.json()
        print('get all user id success')

        for user in data['data']['allUsers']:
            user_id = user['id']
            user_id_list.append(user_id)

    else:
        print(f'Error: {response.status_code} - {response.text}')
    
    return user_id_list

def create_recipe(recipe, user_id):
    mutation = '''
        mutation {
            createRecipe(
                userId: %s
                cookingTime: %d
                description: "%s"
                difficultyLevel: "%s"
                preparationTime: %d
                title: "%s"
                image: ""
            ) {
                recipe {
                id
                }
            }
        }
    ''' % (user_id, recipe['cooking_time'], recipe['description'], recipe['difficulty_level'], recipe['preparation_time'], recipe['title'])

    response = requests.post(URL, json={'query': mutation})
    data = response.json()
    recipe_id = data['data']['createRecipe']['recipe']['id']

    return recipe_id


if __name__ == '__main__':
    user_id_list = get_all_user_id()
    
    with open('recipes.json') as f:
        recipes_data = json.load(f)

    # for recipe in recipes_data:
    recipe = recipes_data[0]
    recipe = recipe['recipe']
    user_id = random.choice(user_id_list)

    recipe_id = create_recipe(recipe, user_id)
    print(recipe_id)

    