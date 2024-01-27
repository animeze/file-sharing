#(©)CodeXBotz




import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import *
from database.db_premium import *
from database.db_wes import *
from database.db_jav import *
from database.db_hentai import *
from database.db_only import *
from database.db_desi import *



@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        if string.startswith("pay2get"):
            if not await is_premium_user(message.from_user.id):
                if not await jav_premium_user(message.from_user.id):
                    await message.reply_text("You're not a premium user. if you want buy premium services then contact @HandsumGuyOp")
                    return

        if string.startswith("wesporn"):
            if not await is_premium_user(message.from_user.id):
                if not await wes_premium_user(message.from_user.id):
                    await message.reply_text("You're not a premium user. if you want buy premium services then contact @HandsumGuyOp")
                    return

        if string.startswith("onlyfans"):
            if not await is_premium_user(message.from_user.id):
                if not await only_premium_user(message.from_user.id):
                    await message.reply_text("You're not a premium user. if you want buy premium services then contact @HandsumGuyOp")
                    return
                    
        if string.startswith("hentaix"):
            if not await is_premium_user(message.from_user.id):
                if not await hentai_premium_user(message.from_user.id):
                    await message.reply_text("You're not a premium user. if you want buy premium services then contact @HandsumGuyOp")
                    return

        if string.startswith("desi"):
            if not await is_premium_user(message.from_user.id):
                if not await jav_premium_user(message.from_user.id):
                    await message.reply_text("You're not a premium user. if you want buy premium services then contact @HandsumGuyOp")
                    return
                argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return
    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

# for premium user
@Bot.on_message(filters.private & filters.command('addpremium') & filters.user(ADMINS))
async def add_premium_user(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("Format: /addpremium user_id time_limit_months both must be integers")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a premium user with a {time_limit_months}-days subscription.")
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removepremium') & filters.user(ADMINS))
async def pre_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("Format: /removeuser user_id must be an integer")
        return
    try:
        user_id = int(msg.command[1])
        await remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

@Bot.on_message(filters.private & filters.command('listpremium') & filters.user(ADMINS))
async def list_premium_users_command(client, message):
    premium_users = collection.find({})
    premium_user_list = ['Premium Users in database:']

    for user in premium_users:
        user_ids = user["user_id"]
        user_info = await client.get_users(user_ids)
        username = user_info.username
        first_name = user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        xt = (expiration_timestamp-(time.time()))
        x = round(xt/(24*60*60))
        premium_user_list.append(f"User id:<code>{user_ids}</code>\nUsername: @{username}\nName: <code>{first_name}</code>\nExpiration Timestamp: {x} days")

    if premium_user_list:
        formatted_list = [f"{user}" for user in premium_user_list]
        await message.reply_text("\n\n".join(formatted_list))
    else:
        await message.reply_text("No premium users found in the database.")

#for western porn

@Bot.on_message(filters.private & filters.command('addam') & filters.user(ADMINS))
async def wes_premium_user_command(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("Format: /addam user_id time_limit_days both must be integers")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await wes_add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a premium user for Other Porn with a {time_limit_months}-days subscription.")
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removeam') & filters.user(ADMINS))
async def wes_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("Format: /removeam user_id must be an integer")
        return
    try:
        user_id = int(msg.command[1])
        await wes_remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed from otherp0rn database.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

@Bot.on_message(filters.private & filters.command('listam') & filters.user(ADMINS))
async def wes_premium_users_command(client, message):
    wes_users = wcollection.find({})
    wes_user_list = ['Other p0rn Premium Users in database:']

    for user in wes_users:
        user_ids = user["user_id"]
        user_info = await client.get_users(user_ids)
        username = user_info.username
        first_name = user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        xt = (expiration_timestamp-(time.time()))
        x = round(xt/(24*60*60))
        wes_user_list.append(f"User id:<code>{user_ids}</code>\nUsername: @{username}\nName: <code>{first_name}</code>\nExpiration Timestamp: {x} days")

    if wes_user_list:
        formatted_list = [f"{user}" for user in wes_user_list]
        await message.reply_text("Premium Users For Adult Porn in the Database:\n\n".join(formatted_list))
    else:
        await message.reply_text("No premium users found in the database.")

#for jav

@Bot.on_message(filters.private & filters.command('adddesi') & filters.user(ADMINS))
async def jav_premium_user_add(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("Format: /adddesi user_id time_limit_days both must be integers")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await jav_add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a premium user for Desi Leak with a {time_limit_months}-days subscription.")
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removedesi') & filters.user(ADMINS))
async def jav_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("Format: /removedesi user_id must be an integer")
        return
    try:
        user_id = int(msg.command[1])
        await jav_remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed from desi database.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

@Bot.on_message(filters.private & filters.command('listdesi') & filters.user(ADMINS))
async def jav_premium_users_command(client, message):
    jav_users = jcollection.find({})
    jav_user_list = ['Jav Premium User in database:']

    for user in jav_users:
        user_ids = user["user_id"]
        user_info = await client.get_users(user_ids)
        username = user_info.username
        first_name = user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        xt = (expiration_timestamp-(time.time()))
        x = round(xt/(24*60*60))
        jav_user_list.append(f"User id:<code>{user_ids}</code>\nUsername: @{username}\nName: <code>{first_name}</code>\nExpiration Timestamp: {x} days")

    if jav_user_list:
        formatted_list = [f"{user}" for user in jav_user_list]
        await message.reply_text("Premium Users For Desi Leak in the Database:\n\n".join(formatted_list))
    else:
        await message.reply_text("No premium users found in the database.")

#for hentai 

@Bot.on_message(filters.private & filters.command('addhentai') & filters.user(ADMINS))
async def hentai_premium_user_add(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("Format: /addjav user_id time_limit_days both must be integers")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await hentai_add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a premium user for Desi Leak with a {time_limit_months}-days subscription.")
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removehentai') & filters.user(ADMINS))
async def hentai_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("Format: /removedesi user_id must be an integer")
        return
    try:
        user_id = int(msg.command[1])
        await hentai_remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed from desi database.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

@Bot.on_message(filters.private & filters.command('listhentai') & filters.user(ADMINS))
async def hentai_premium_users_command(client, message):
    hentai_users = hcollection.find({})
    hentai_user_list = ['Hentai Premium User in database:']

    for user in hentai_users:
        user_ids = user["user_id"]
        user_info = await client.get_users(user_ids)
        username = user_info.username
        first_name = user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        xt = (expiration_timestamp-(time.time()))
        x = round(xt/(24*60*60))
        hentai_user_list.append(f"User id:<code>{user_ids}</code>\nUsername: @{username}\nName: <code>{first_name}</code>\nExpiration Timestamp: {x} days")

    if hentai_user_list:
        formatted_list = [f"{user}" for user in  hentai_list_user]
        await message.reply_text("Premium Users For Hentai in the Database:\n\n".join(formatted_list))
    else:
        await message.reply_text("No premium users found in the database.")

#for Onlyfans

@Bot.on_message(filters.private & filters.command('addonly') & filters.user(ADMINS))
async def only_premium_user_command(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("Format: /addonly user_id time_limit_days both must be integers")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await only_add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a premium user for Onlyfans with a {time_limit_months}-days subscription.")
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removeonly') & filters.user(ADMINS))
async def only_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("Format: /removeonly user_id must be an integer")
        return
    try:
        user_id = int(msg.command[1])
        await only_remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed from onlyfans database.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

@Bot.on_message(filters.private & filters.command('listonly') & filters.user(ADMINS))
async def only_premium_users_command(client, message):
    only_users = ocollection.find({})
    only_user_list = ['OnlyFans Premium Users in database:']

    for user in only_users:
        user_ids = user["user_id"]
        user_info = await client.get_users(user_ids)
        username = user_info.username
        first_name = user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        xt = (expiration_timestamp-(time.time()))
        x = round(xt/(24*60*60))
        only_user_list.append(f"User id:<code>{user_ids}</code>\nUsername: @{username}\nName: <code>{first_name}</code>\nExpiration Timestamp: {x} days")

    if only_user_list:
        formatted_list = [f"{user}" for user in only_user_list]
        await message.reply_text("Premium Users For OnlyFans in the Database:\n\n".join(formatted_list))
    else:
        await message.reply_text("No premium users found in the database.")

#for Desi

@Bot.on_message(filters.private & filters.command('addjav') & filters.user(ADMINS))
async def desi_premium_user_command(client: Client, msg: Message):
    if len(msg.command) != 3:
        await msg.reply_text("Format: /addjav user_id time_limit_days both must be integers")
        return
    try:
        user_id = int(msg.command[1])
        time_limit_months = int(msg.command[2])
        await desi_add_premium(user_id, time_limit_months)
        await msg.reply_text(f"User {user_id} added as a premium user for Jav with a {time_limit_months}-days subscription.")
    except ValueError:
        await msg.reply_text("Invalid user_id or time_limit. Please recheck.")

@Bot.on_message(filters.private & filters.command('removejav') & filters.user(ADMINS))
async def desi_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("Format: /removejav user_id must be an integer")
        return
    try:
        user_id = int(msg.command[1])
        await desi_remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed from jav database.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")

@Bot.on_message(filters.private & filters.command('listjav') & filters.user(ADMINS))
async def desi_premium_users_command(client, message):
    desi_users = dcollection.find({})
    desi_user_list = ['Jav Premium Users in database:']

    for user in desi_users:
        user_ids = user["user_id"]
        user_info = await client.get_users(user_ids)
        username = user_info.username
        first_name = user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        xt = (expiration_timestamp-(time.time()))
        x = round(xt/(24*60*60))
        desi_user_list.append(f"User id:<code>{user_ids}</code>\nUsername: @{username}\nName: <code>{first_name}</code>\nExpiration Timestamp: {x} days")

    if desi_user_list:
        formatted_list = [f"{user}" for user in desi_user_list]
        await message.reply_text("Premium Users For Jav in the Database:\n\n".join(formatted_list))
    else:
        await message.reply_text("No premium users found in the database.")

    
