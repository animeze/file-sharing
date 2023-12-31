import time
import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
wcollection = database['wes-users']


async def wes_add_premium(user_id, time_limit_days):
    expiration_timestamp = int(time.time()) + time_limit_days * 24 * 60 * 60
    premium_data = {
        "user_id": user_id,
        "expiration_timestamp": expiration_timestamp,
    }
    wcollection.insert_one(premium_data)

async def wes_remove_premium(user_id):
    result = wcollection.delete_one({"user_id": user_id})

async def wes_remove_expired_users():
    current_timestamp = int(time.time())

    # Find and delete expired users
    expired_users = wcollection.find({"expiration_timestamp": {"$lte": current_timestamp}})
    
    for expired_user in expired_users:
        user_id = expired_user["user_id"]
        wcollection.delete_one({"user_id": user_id})

async def wes_premium_user(user_id):
    user = wcollection.find_one({"user_id": user_id})
    return user is not None
