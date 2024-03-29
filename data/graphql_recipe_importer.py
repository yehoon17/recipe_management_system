import requests
import json


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


if __name__ == '__main__':
    user_id_list = get_all_user_id()
    
    with open('recipes.json') as f:
        recipes_data = json.load(f)

    recipe = recipes_data[0]
    print(recipe)

    