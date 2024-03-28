import json

# User data
n_users = 10
users = []
for i in range(n_users):
    user = {
        "username": f"user{i}",
        "email": f"user{i}@example.com",
        "password": f"password{i}"
    }
    
    users.append(user)

# Write user data to users.json
with open('./users.json', 'w') as json_file:
    json.dump(users, json_file, indent=4)

print("users.json file created successfully!")
