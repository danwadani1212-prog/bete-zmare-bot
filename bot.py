import asyncio
import os
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
import yt_dlp

# ================= CONFIGURATION =================
API_ID = 30164211
API_HASH = "4fd262dd417038d3c95d75c312553ab1"
BOT_TOKEN = "8682505041:AAHLy7Gk8gQnUiFDGpiedo0NrQ4jmKRROlQ"
SESSION_STRING = "BAHMRPMAd2IYSQoC8nHAlQQFFgwIh0HcTXgAgU9u5806Ff6pg0U5OVHolhXP530qDXMC7X0PouNpUblBR1Rlje-aGYMQ74qT4wzfxJu5ZJWkvx_9qcCGBNjJveHf3hLx3z0aA0Gd2e9LGTi7x1ANu96Poxc_WZIwDo3RHy3iWzkAuqNzPwfSjIYEvHFGXh1QdyYmdK5xPgScD7C6HEMt6KSUr_NQPsWwy2mLt2qUyYSGFojmMxgfZDNu1iElNFj2mwxy_KRejVZYvToe_2gEggpF2PhBsoAboqWHEVNag3U1ZrHqRCB6DXaExuT-ibSqyxWrlmkkWvu8_hl-Hhj-N4Y5HHsrBgAAAAFMOAkBAA"
OWNER_ID = 7565076160
BANNER_IMAGE = "https://envs.sh/X1v.jpg"
# =================================================

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True) 
user = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, in_memory=True)
calls = PyTgCalls(user)

users_db = set()
groups_db = set()
user_languages = {}

LANGUAGES = {
    "en": {
        "welcome": "👋 **Hello {name}, Welcome!**\n\n🎵 **{bot_name}** can stream mezmurs, videos, and live audio directly in your group's voice chat.\n\nUse `/help` to see commands, or add me to a group and send `/play [song name]`.",
        "play_cmd": "✨ I can stream mezmurs, videos, and live audio directly in your group's voice chat.\nTo change language, send `/lang`.\n\n🎵 `/play [song]` — Audio Stream\n🎬 `/vplay [video]` — Video Stream",
        "searching": "🔍 ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ...",
        "playing_audio": "➜ **ꜱᴛʀᴇᴀᴍɪɴɢ ꜱᴛᴀʀᴛᴇᴅ | ᴇɴᴊᴏʏ ᴍᴜꜱɪᴄ**\n▶️ **ᴛʀᴀᴄᴋ** : {title}\n⏱️ **ᴅᴜʀᴀᴛɪᴏɴ** : {duration}\n👤 **ʀᴇǫᴜᴇꜱᴛᴇʀ** : {user}",
        "playing_video": "➜ **ᴠɪᴅᴇᴏ ꜱᴛʀᴇᴀᴍɪɴɢ | ᴇɴᴊᴏʏ ᴠɪᴅᴇᴏ**\n▶️ **ᴛʀᴀᴄᴋ** : {title}\n⏱️ **ᴅᴜʀᴀᴛɪᴏɴ** : {duration}\n👤 **ʀᴇǫᴜᴇꜱᴛᴇʀ** : {user}",
        "paused": "Playback has been paused.",
        "resumed": "Playback has been resumed.",
        "stopped": "⏹️ **Stream Ended & Cleaned.**",
        "select_lang": "🌐 **ᴘʟᴇᴀꜱᴇ ꜱᴇʟᴇᴄᴛ ʏᴏᴜʀ ʟᴀɴɢᴜᴀɢᴇ:**",
        "help_text": "📖 **ʜᴇʟᴘ ᴍᴇɴᴜ**\n\nClick a button below to view options:",
        "admin_only": "❌ Only group administrators or owners can use this command!",
        "bot_not_admin": "❌ **I need Administrator permissions in this group!**",
        "not_found": "⚠️ **Could not find the requested media.**"
    },
    "am": {
        "welcome": "👋 **ሰላም {name}፣ እንኳን ደህና መጡ!**\n\n🎵 **{bot_name}** በግሩፕዎ ቮይስ ቻት ውስጥ መዝሙሮችን፣ ቪዲዮዎችን እና የቀጥታ ድምፆችን በከፍተኛ ጥራት ማጫወት ይችላል።",
        "play_cmd": "✨ በግሩፕዎ ቮይስ ቻት ውስጥ መዝሙሮችን እና ቪዲዮዎችን ማጫወት እችላለሁ።",
        "searching": "🔍 ጥያቄዎ በመስተናገድ ላይ ነው...",
        "playing_audio": "➜ **የኦዲዮ ዥረት ተጀምሯል**\n▶️ **መዝሙር** : {title}\n⏱️ **የቆይታ ጊዜ** : {duration}\n👤 **አጫዋች** : {user}",
        "playing_video": "➜ **የቪዲዮ ዥረት ተጀምሯል**\n▶️ **ርዕስ** : {title}\n⏱️ **የቆይታ ጊዜ** : {duration}\n👤 **አጫዋች** : {user}",
        "paused": "ሙዚቃው ቆሟል።",
        "resumed": "ሙዚቃው ቀጥሏል።",
        "stopped": "⏹️ **Stream Ended & Cleaned.**",
        "select_lang": "🌐 **እባክዎ የሚፈልጉትን ቋንቋ ይምረጡ:**",
        "help_text": "📖 **የእርዳታ ማዕከል (HELP MENU)**",
        "admin_only": "❌ ይህንን ትዕዛዝ መጠቀም የሚችሉት ግሩፑ አድሚኖች ወይም ባለቤቶች (Owners) ብቻ ናቸው!",
        "bot_not_admin": "❌ **ቦቱ ግሩፑ ውስጥ አድሚን መሆን አለበት!**",
        "not_found": "⚠️ **መዝሙሩን ማግኘት አልተቻለም።**"
    }
}

def get_lang(user_id):
    return user_languages.get(user_id, "en")

def format_duration(seconds):
    if not seconds:
        return "Unknown"
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes)}:{int(remaining_seconds):02d}"

def search_media(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "default_search": "ytsearch1",
        "extractor_args": {"youtube": {"player_client": ["android", "web", "mweb"]}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if "entries" in info and info["entries"]:
                video = info["entries"][0]
                duration = format_duration(video.get("duration"))
                return video["url"], video["title"], video.get("thumbnail", BANNER_IMAGE), duration, video.get("duration", 0)
            elif "url" in info:
                duration = format_duration(info.get("duration"))
                return info["url"], info["title"], info.get("thumbnail", BANNER_IMAGE), duration, info.get("duration", 0)
        except Exception:
            pass
        return None, None, None, "Unknown", 0

def search_video_media(query):
    ydl_opts = {
        "format": "best",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "default_search": "ytsearch1",
        "extractor_args": {"youtube": {"player_client": ["android", "web", "mweb"]}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if "entries" in info and info["entries"]:
                video = info["entries"][0]
                duration = format_duration(video.get("duration"))
                return video["url"], video["title"], video.get("thumbnail", BANNER_IMAGE), duration, video.get("duration", 0)
            elif "url" in info:
                duration = format_duration(info.get("duration"))
                return info["url"], info["title"], info.get("thumbnail", BANNER_IMAGE), duration, info.get("duration", 0)
        except Exception:
            pass
        return None, None, None, "Unknown", 0

async def is_admin(client, chat_id, user_id):
    if not user_id:
        return False
    if int(user_id) == int(OWNER_ID):
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ["administrator", "creator"]:
            return True
    except Exception:
        pass
    return False

async def is_bot_admin(client, chat_id):
    try:
        bot_member = await client.get_chat_member(chat_id, client.me.id)
        if bot_member.status in ["administrator", "creator"]:
            return True
    except Exception:
        pass
    return False

# 1. 🟢 /start ኮማንድ ማስተካከያ (ለግል መልእክት ምላሽ ይሰጣል)
@bot.on_message(filters.command("start") & filters.private)
async def start_private(client, message):
    users_db.add(message.chat.id)
    user_id = message.from_user.id
    bot_username = client.me.username
    bot_name = client.me.first_name
    
    lang_code = get_lang(user_id)
    lang_data = LANGUAGES[lang_code]
    
    text = lang_data["welcome"].format(
        name=message.from_user.first_name if message.from_user else 'User',
        bot_name=bot_name
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("⚙️ ꜱᴇᴛᴛɪɴɢꜱ / ʜᴇʟᴘ", callback_data="help_menu")],
        [
            InlineKeyboardButton("📢 ʙᴏᴛ ᴜᴘᴅᴀᴛᴇꜱ", url="https://t.me/Botupdate_BZ7"),
            InlineKeyboardButton("💬 ʙᴏᴛ ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/Bot_SupportBZ")
        ]
    ])
    
    try:
        await message.reply_photo(photo=BANNER_IMAGE, caption=text, reply_markup=keyboard)
    except Exception:
        await message.reply_text(text, reply_markup=keyboard)

@bot.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client, message):
    if int(message.from_user.id) != int(OWNER_ID):
        return
    if len(message.command) < 2:
        return
    
    query = message.text.split(None, 1)[1]
    sent_count = 0
    
    for uid in users_db:
        try:
            await client.send_message(uid, f"📢 **ᴀɴɴᴏᴜɴᴄᴇᴍᴇɴᴛ:**\n\n{query}")
            sent_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass
            
    for gid in groups_db:
        try:
            await client.send_message(gid, f"📢 **ᴀɴɴᴏᴜɴᴄᴇᴍᴇɴᴛ:**\n\n{query}")
            sent_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass
            
    await message.reply(f"✅ ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴇɴᴛ ᴛᴏ {sent_count} ᴜꜱᴇʀꜱ/ɢʀᴏᴜᴘꜱ!")

@bot.on_message(filters.command("lang"))
async def lang_command(client, message):
    user_id = message.from_user.id if message.from_user else None
    if message.chat.type in ["supergroup", "group"] and not await is_admin(client, message.chat.id, user_id):
        return
    lang_data = LANGUAGES[get_lang(user_id)]
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="set_am"),
            InlineKeyboardButton("English 🇬🇧", callback_data="set_en")
        ]
    ])
    await message.reply_text(lang_data["select_lang"], reply_markup=keyboard)

@bot.on_message(filters.new_chat_members)
async def welcome_group(client, message):
    groups_db.add(message.chat.id)
    for member in message.new_chat_members:
        if member.id == client.me.id:
            bot_username = client.me.username
            lang_data = LANGUAGES["en"]
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🌐 ʟᴀɴɢᴜᴀɢᴇ", callback_data="lang_menu"),
                    InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇꜱ", url="https://t.me/Botupdate_BZ7")
                ],
                [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{bot_username}?startgroup=true")]
            ])
            text = (
                f"🎵 **ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ** @{bot_username}\n\n"
                f"👤 **ᴀᴅᴅᴇᴅ ʙʏ:** {message.from_user.first_name if message.from_user else 'Admin'}\n"
                f"👥 **ɢʀᴏᴜᴘ:** {message.chat.title}\n"
                f"🆔 **ᴄʜᴀᴛ ɪᴅ:** {message.chat.id}\n\n"
                f"{lang_data['play_cmd']}"
            )
            try:
                await message.reply_photo(photo=BANNER_IMAGE, caption=text, reply_markup=keyboard)
            except Exception:
                await message.reply_text(text, reply_markup=keyboard)

@bot.on_message(filters.video_chat_started)
async def voice_chat_started_handler(client, message):
    await message.reply("😍 **ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ꜱᴛᴀʀᴛᴇᴅ!** 🎉\n\n🎵 Ready for streaming mezmurs and music.")

@bot.on_message(filters.video_chat_ended)
async def voice_chat_ended_handler(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{client.me.username}?startgroup=true"),
         InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
    ])
    await message.reply("⏸️ **ꜱᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ & ᴄʟᴇᴀɴᴇᴅ.**", reply_markup=keyboard)

@bot.on_message(filters.command("help"))
async def help_command(client, message):
    user_id = message.from_user.id if message.from_user else None
    if message.chat.type in ["supergroup", "group"] and not await is_admin(client, message.chat.id, user_id):
        return
    lang_data = LANGUAGES[get_lang(user_id)]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 /play", callback_data="cmd_play"), InlineKeyboardButton("🎬 /vplay", callback_data="cmd_vplay")],
        [InlineKeyboardButton("⏸ /pause", callback_data="pause"), InlineKeyboardButton("▶️ /resume", callback_data="resume")],
        [InlineKeyboardButton("⏹ /end", callback_data="end"), InlineKeyboardButton("⏭ /skip", callback_data="cmd_skip")],
        [InlineKeyboardButton("🌐 /lang", callback_data="lang_menu"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
    ])
    try:
        await message.reply_photo(photo=BANNER_IMAGE, caption=lang_data["help_text"], reply_markup=keyboard)
    except Exception:
        await message.reply_text(lang_data["help_text"], reply_markup=keyboard)

@bot.on_message(filters.command("play"))
async def play_audio_handler(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None
    lang_data = LANGUAGES[get_lang(user_id)]

    if message.chat.type in ["supergroup", "group"]:
        if not await is_admin(client, chat_id, user_id):
            try:
                await message.delete()
            except Exception:
                pass
            return
        if not await is_bot_admin(client, chat_id):
            await message.reply(lang_data["bot_not_admin"])
            return
        
    if len(message.command) < 2:
        await message.reply("Please provide a song name! Example: `/play mezmur`" if get_lang(user_id) == "en" else "እባክዎ የመዝሙሩን ስም ይጻፉ! ምሳሌ፦ `/play መዝሙር`")
        return
    query = message.text.split(None, 1)[1]
    msg = await message.reply(lang_data["searching"])
    try:
        url, title, thumbnail, duration, duration_secs = await asyncio.to_thread(search_media, query)
        if not url:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]])
            await msg.edit(lang_data["not_found"], reply_markup=keyboard)
            return

        user_name = message.from_user.first_name if message.from_user else "User"
        
        try:
            invite_link = await client.export_chat_invite_link(chat_id)
            if invite_link:
                await user.join_chat(invite_link)
        except Exception:
            pass

        try:
            await calls.join_group_call(
                chat_id, 
                MediaStream(url, audio_parameters=AudioQuality.STUDIO, video_flags=MediaStream.Flags.IGNORE)
            )
        except Exception:
            await calls.play(
                chat_id, 
                MediaStream(url, audio_parameters=AudioQuality.STUDIO, video_flags=MediaStream.Flags.IGNORE)
            )
        
        controls = InlineKeyboardMarkup([
            [InlineKeyboardButton("⏸ ᴘᴀᴜꜱᴇ", callback_data="pause"), InlineKeyboardButton("▶️ ʀᴇꜱᴜᴍᴇ", callback_data="resume")],
            [InlineKeyboardButton("⏭ ꜱᴋɪᴘ", callback_data="cmd_skip"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")],
            [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{client.me.username}?startgroup=true")]
        ])
        
        text = lang_data["playing_audio"].format(title=title, duration=duration, user=user_name)
        try:
            sent_msg = await message.reply_photo(photo=thumbnail, caption=text, reply_markup=controls)
        except Exception:
            sent_msg = await message.reply_text(text, reply_markup=controls)
        await msg.delete()

        # 2. 🟢 ዥረቱ ሲያልቅ ፖስቱ በራሱ እንዲጠፋ እና ዩዘር ቦቱ እንዲወጣ የሚያደርግ
        if duration_secs > 0:
            async def auto_leave():
                await asyncio.sleep(duration_secs + 3)
                try:
                    await calls.leave_group_call(chat_id)
                except Exception:
                    pass
                try:
                    await user.leave_chat(chat_id)
                except Exception:
                    pass
                try:
                    await sent_msg.delete()
                except Exception:
                    pass
            asyncio.create_task(auto_leave())

    except Exception as e:
        await msg.edit(f"Error: {str(e)}")

@bot.on_message(filters.command("vplay"))
async def play_video_handler(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None
    lang_data = LANGUAGES[get_lang(user_id)]

    if message.chat.type in ["supergroup", "group"]:
        if not await is_admin(client, chat_id, user_id):
            try:
                await message.delete()
            except Exception:
                pass
            return
        if not await is_bot_admin(client, chat_id):
            await message.reply(lang_data["bot_not_admin"])
            return
        
    if len(message.command) < 2:
        await message.reply("Please provide a video name! Example: `/vplay mezmur`" if get_lang(user_id) == "en" else "እባክዎ የቪዲዮውን ስም ይጻፉ! ምሳሌ፦ `/vplay መዝሙር`")
        return
    query = message.text.split(None, 1)[1]
    msg = await message.reply(lang_data["searching"])
    try:
        url, title, thumbnail, duration, duration_secs = await asyncio.to_thread(search_video_media, query)
        if not url:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]])
            await msg.edit(lang_data["not_found"], reply_markup=keyboard)
            return

        user_name = message.from_user.first_name if message.from_user else "User"
        
        try:
            invite_link = await client.export_chat_invite_link(chat_id)
            if invite_link:
                await user.join_chat(invite_link)
        except Exception:
            pass

        try:
            await calls.join_group_call(
                chat_id, 
                MediaStream(url, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.HD_720p)
            )
        except Exception:
            await calls.play(
                chat_id, 
                MediaStream(url, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.HD_720p)
            )
        
        controls = InlineKeyboardMarkup([
            [InlineKeyboardButton("⏸ ᴘᴀᴜꜱᴇ", callback_data="pause"), InlineKeyboardButton("▶️ ʀᴇꜱᴜᴍᴇ", callback_data="resume")],
            [InlineKeyboardButton("⏭ ꜱᴋɪᴘ", callback_data="cmd_skip"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")],
            [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{client.me.username}?startgroup=true")]
        ])
        
        text = lang_data["playing_video"].format(title=title, duration=duration, user=user_name)
        try:
            sent_msg = await message.reply_photo(photo=thumbnail, caption=text, reply_markup=controls)
        except Exception:
            sent_msg = await message.reply_text(text, reply_markup=controls)
        await msg.delete()

        if duration_secs > 0:
            async def auto_leave_video():
                await asyncio.sleep(duration_secs + 3)
                try:
                    await calls.leave_group_call(chat_id)
                except Exception:
                    pass
                try:
                    await user.leave_chat(chat_id)
                except Exception:
                    pass
                try:
                    await sent_msg.delete()
                except Exception:
                    pass
            asyncio.create_task(auto_leave_video())

    except Exception as e:
        await msg.edit(f"Error: {str(e)}")

@bot.on_message(filters.command(["end", "pause", "resume", "skip"]))
async def control_commands(client, message):
    user_id = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    if message.chat.type in ["supergroup", "group"]:
        if not await is_admin(client, chat_id, user_id):
            try:
                await message.delete()
            except Exception:
                pass
            return
    cmd = message.command[0].lower()
    lang_data = LANGUAGES[get_lang(user_id)]
    try:
        if cmd == "end" or cmd == "skip":
            await calls.leave_group_call(message.chat.id)
            try:
                await user.leave_chat(chat_id)
            except Exception:
                pass
            await message.delete()
        elif cmd == "pause":
            await calls.pause(message.chat.id)
            await message.reply(lang_data["paused"])
        elif cmd == "resume":
            await calls.resume(message.chat.id)
            await message.reply(lang_data["resumed"])
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

# 3. 🟢 የአዝራሮች ማጣሪያ (አድሚን ያልሆኑ ሰዎች ፓውዝ/ሪዝዩም/ስኪፕ ማድረግ አይችሉም)
@bot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id if callback_query.from_user else None
    
    # 🛑 ጥብቅ ማጣሪያ፦ ከአድሚን እና ኦነር ውጪ ማንም አዝራሮቹን መንካት አይችልም!
    if callback_query.message.chat.type in ["supergroup", "group"]:
        is_user_admin = await is_admin(client, chat_id, user_id)
        if not is_user_admin:
            await callback_query.answer("🚫 ONLY ADMINS CAN USE THIS.", show_alert=True)
            return

    lang_code = get_lang(user_id)
    lang_data = LANGUAGES[lang_code]

    try:
        if data == "pause":
            await calls.pause(chat_id)
            await callback_query.answer(lang_data["paused"], show_alert=True)
        elif data == "resume":
            await calls.resume(chat_id)
            await callback_query.answer(lang_data["resumed"], show_alert=True)
        elif data == "end":
            await calls.leave_group_call(chat_id)
            try:
                await user.leave_chat(chat_id)
            except Exception:
                pass
            await callback_query.answer("Stream stopped.", show_alert=True)
            try:
                await callback_query.message.delete()
            except Exception:
                pass
        elif data == "skip" or data == "cmd_skip":
            await callback_query.answer("⏭ Skipping track...", show_alert=True)
            await calls.leave_group_call(chat_id)
            try:
                await user.leave_chat(chat_id)
            except Exception:
                pass
            try:
                await callback_query.message.delete()
            except Exception:
                pass
        elif data == "close":
            await callback_query.message.delete()
        elif data == "help_menu":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎵 /play", callback_data="cmd_play"), InlineKeyboardButton("🎬 /vplay", callback_data="cmd_vplay")],
                [InlineKeyboardButton("⏸ /pause", callback_data="pause"), InlineKeyboardButton("▶️ /resume", callback_data="resume")],
                [InlineKeyboardButton("⏹ /end", callback_data="end"), InlineKeyboardButton("⏭ /skip", callback_data="cmd_skip")],
                [InlineKeyboardButton("🌐 /lang", callback_data="lang_menu"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="close")]
            ])
            try:
                await callback_query.message.edit_media(
                    media=InputMediaPhoto(BANNER_IMAGE, caption=lang_data["help_text"]),
                    reply_markup=keyboard
                )
            except Exception:
                await callback_query.message.edit_text(lang_data["help_text"], reply_markup=keyboard)
        elif data == "back_start":
            bot_username = client.me.username
            text = lang_data["welcome"].format(
                name=callback_query.from_user.first_name if callback_query.from_user else 'User',
                bot_name=client.me.first_name
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ", url=f"https://t.me/{bot_username}?startgroup=true")],
                [InlineKeyboardButton("⚙️ ꜱᴇᴛᴛɪɴɢꜱ / ʜᴇʟᴘ", callback_data="help_menu")],
                [
                    InlineKeyboardButton("📢 ʙᴏᴛ ᴜᴘᴅᴀᴛᴇꜱ", url="https://t.me/Botupdate_BZ7"),
                    InlineKeyboardButton("💬 ʙᴏᴛ ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/Bot_SupportBZ")
                ]
            ])
            try:
                await callback_query.message.edit_media(
                    media=InputMediaPhoto(BANNER_IMAGE, caption=text),
                    reply_markup=keyboard
                )
            except Exception:
                await callback_query.message.edit_text(text, reply_markup=keyboard)
        elif data == "lang_menu":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="set_am"), InlineKeyboardButton("English 🇬🇧", callback_data="set_en")],
                [InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="help_menu")]
            ])
            try:
                await callback_query.message.edit_caption(lang_data["select_lang"], reply_markup=keyboard)
            except Exception:
                await callback_query.message.edit_text(lang_data["select_lang"], reply_markup=keyboard)
        elif data.startswith("set_"):
            selected_lang = data.split("_")[1]
            if selected_lang in LANGUAGES:
                user_languages[user_id] = selected_lang
                new_lang_data = LANGUAGES[selected_lang]
                msg_text = "✅ Language set to English!" if selected_lang == "en" else "✅ ቋንቋው ወደ አማርኛ ተቀይሯል!"
                await callback_query.answer(msg_text, show_alert=True)
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="help_menu")]
                ])
                try:
                    await callback_query.message.edit_caption(f"{msg_text}\n\n{new_lang_data['help_text']}", reply_markup=keyboard)
                except Exception:
                    await callback_query.message.edit_text(f"{msg_text}\n\n{new_lang_data['help_text']}", reply_markup=keyboard)
        elif data.startswith("cmd_"):
            await callback_query.answer("Please send this command in group chat!", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Note: {str(e)}", show_alert=True)

async def main():
    await bot.start()
    await user.start()
    await calls.start()
    print("✅ Bete Zmare Bot is fully operational with strict admin blocking and auto-leave!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())