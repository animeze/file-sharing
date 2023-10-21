import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.db_wes import *

@Bot.on_message(filters.private & filters.command('addwes') & filters.user(ADMINS))
async def wes_premium_user(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("Format: /addpremium user_id time_limit_days both must be integers")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await wes_add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a premium user for western Porn with a {time_limit_months}-days subscription.")
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removewes') & filters.user(ADMINS))
async def remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("Format: /removeuser user_id must be an integer")
        return
    try:
        user_id = int(msg.command[1])
        await wes_remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed from wes database.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

@Bot.on_message(filters.private & filters.command('listwes') & filters.user(ADMINS))
async def wes_premium_users_command(client, message):
    premium_users = collection.find({})
    premium_user_list = []

    for user in premium_users:
        user_ids = user["user_id"]
        user_info = await client.get_users(user_ids)
        username = user_info.username if user_info.username else user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        xt = (expiration_timestamp-(time.time()))
        x = round(xt/(24*60*60))
        premium_user_list.append(f"User id:`{user_ids}`\n Username `{username}`\nExpiration Timestamp: {x} days")

    if premium_user_list:
        formatted_list = [f"{user}" for user in premium_user_list]
        await message.reply_text("Premium Users For Western Porn in the Database:\n\n".join(formatted_list))
    else:
        await message.reply_text("No premium users found in the database.")
