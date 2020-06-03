import pandas as pd
from passlib.hash import sha256_crypt
from model import collection_user

user = pd.read_csv('./csv/users_super_final.csv')

# print(user)

all_user_id = user['user_id'].unique()
for user in all_user_id:
    print(user)
    password = sha256_crypt.encrypt(user)
    total = {
        'userid': user,
        'username': user,
        'password': password
    }
    collection_user.insert_one(total)