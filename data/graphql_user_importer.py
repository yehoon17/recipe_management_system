import argparse
import requests


URL = 'http://localhost:8000/graphql/'  


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_users", type=int, default=10, help="Number of users to create")
    args = parser.parse_args()

    if args.n_users is None:
        print("Please provide a number using -n option")
        return
    
    for i in range(args.n_users):
        mutation = '''
            mutation {
                createUser(
                    username: "user%d",
                    email: "user%s@example.com",
                    password: "password%s"
                ) {
                    user {
                        id
                        username
                        email
                    }
                }
            }
        ''' % (i, i, i)

        response = requests.post(URL, json={'query': mutation})

        # Process response
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f'Error: {response.status_code} - {response.text}')


if __name__ == '__main__':
    main()
    