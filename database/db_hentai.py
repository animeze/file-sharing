import time
import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
hcollection = database['h-users']


async def hentai_add_premium(user_id, time_limit_days):
    expiration_timestamp = int(time.time()) + time_limit_days * 24 * 60 * 60
    premium_data = {
        "user_id": user_id,
        "expiration_timestamp": expiration_timestamp,
    }
    hcollection.insert_one(premium_data)

async def hentai_remove_premium(user_id):
    result = hcollection.delete_one({"user_id": user_id})

async def hentai_remove_expired_users():
    current_timestamp = int(time.time())

    # Find and delete expired users
    expired_users = hcollection.find({"expiration_timestamp": {"$lte": current_timestamp}})
    
    for expired_user in expired_users:
        user_id = expired_user["user_id"]
        hcollection.delete_one({"user_id": user_id})

async def hentai_premium_user(user_id):
    user = hcollection.find_one({"user_id": user_id})
    return user is not None
