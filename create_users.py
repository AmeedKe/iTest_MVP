import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["iTest_DB"]
users_col = db["users"]

# מחיקת משתמשים קיימים כדי לא ליצור כפילויות (אופציונלי)
# users_col.delete_many({})

users = [
    {"username": "gadi", "password": "123"},
    {"username": "ameed", "password": "123"},
    {"username": "student", "password": "123"}
]

for u in users:
    if not users_col.find_one({"username": u["username"]}):
        users_col.insert_one(u)

print("Users created successfully!")
print("Authorized usernames: gadi, ameed, student")
print("Password for all: 123")
