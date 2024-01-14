#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats','adduser','removeuser','listuser','listdesi','listam','adddesi','addam','removedesi','removeam','addhentai','removehentai','listhentai' ,'addonly','removeonly','listonly']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"

    string = f"get-{converted_id}"
    string = string.replace("get-", "pay2get-")
    base64_string = await encode(string)
    link1 = f"https://telegram.me/{client.username}?start={base64_string}"

    string = f"get-{converted_id}"
    string = string.replace("get-", "wesporn-")
    base64_string = await encode(string)
    link2 = f"https://telegram.me/{client.username}?start={base64_string}"

    string = f"get-{converted_id}"
    string = string.replace("get-", "hentaix-")
    base64_string = await encode(string)
    link3 = f"https://telegram.me/{client.username}?start={base64_string}"

    string = f"get-{converted_id}"
    string = string.replace("get-", "onlyfans-")
    base64_string = await encode(string)
    link4 = f"https://telegram.me/{client.username}?start={base64_string}"
    

   reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Link", url=f"{link}")], [InlineKeyboardButton("Jav Link", url=f"{link1}")], [InlineKeyboardButton("Wes Link", url=f"{link2}")], [InlineKeyboardButton("Hentai Link", url=f"{link3}")], [InlineKeyboardButton("OnlyFans Link", url=f"{link4}")]])
