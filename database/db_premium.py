import time
import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
collection = database['premium-users']


async def add_premium(user_id, time_limit_months):
    expiration_timestamp = int(time.time()) + time_limit_months * 24 * 60 * 60
    premium_data = {
        "user_id": user_id,
        "expiration_timestamp": expiration_timestamp,
    }
    collection.insert_one(premium_data)

async def remove_premium(user_id):
    result = collection.delete_one({"user_id": user_id})

async def remove_expired_users():
    current_timestamp = int(time.time())

    # Find and delete expired users
    expired_users = collection.find({"expiration_timestamp": {"$lte": current_timestamp}})
    
    for expired_user in expired_users:
        user_id = expired_user["user_id"]
        collection.delete_one({"user_id": user_id})

async def list_premium_users():

    premium_users = collection.find({})
    
    premium_user_list = []

    for user in premium_users:
        user_id = user["user_id"]
        user_info = Bot.get_users(user_id)
        username = user_info.username if user_info.username else user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        premium_user_list.append(f"{user_id} - {username} - Expiration Timestamp: {expiration_timestamp}")

    return premium_user_list