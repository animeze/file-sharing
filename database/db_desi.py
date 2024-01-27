import time
import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
dcollection = database['desi-users']


async def desi_add_premium(user_id, time_limit_days):
    expiration_timestamp = int(time.time()) + time_limit_days * 24 * 60 * 60
    premium_data = {
        "user_id": user_id,
        "expiration_timestamp": expiration_timestamp,
    }
    dcollection.insert_one(premium_data)

async def desi_remove_premium(user_id):
    result = dcollection.delete_one({"user_id": user_id})

async def desi_remove_expired_users():
    current_timestamp = int(time.time())

    # Find and delete expired users
    expired_users = dcollection.find({"expiration_timestamp": {"$lte": current_timestamp}})
    
    for expired_user in expired_users:
        user_id = expired_user["user_id"]
        dcollection.delete_one({"user_id": user_id})

async def desi_premium_user(user_id):
    user = dcollection.find_one({"user_id": user_id})
    return user is not None
