import re
import os
import time

id_pattern = re.compile(r'^.\d+$')


class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "")  # ⚠️ Required
    API_HASH = os.environ.get("API_HASH", "")  # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")  # ⚠️ Required
    MRSYD = os.environ.get("MRSYD", "")
    # database config
    DB_NAME = os.environ.get("DB_NAME", "Sigma_Rename")
    DB_URL = os.environ.get("DB_URL", "")  # ⚠️ Required

    # other configs
    BOT_UPTIME = time.time()
    PICS = os.environ.get("PICS", 'https://envs.sh/XN2.jpg https://envs.sh/XNu.jpg https://envs.sh/yqA.jpg https://envs.sh/XNh.jpg').split()
    ADMIN = [int(admin) if id_pattern.search(
        admin) else admin for admin in os.environ.get('ADMIN', '').split()]  # ⚠️ Required

    FORCE_SUB = os.environ.get("FORCE_SUB", "") # ⚠️ Required Username without @
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))  # ⚠️ Required
    FLOOD = int(os.environ.get("FLOOD", '10'))
    BANNED_USERS = set(int(x) for x in os.environ.get(
        "BANNED_USERS", "1234567890").split())

    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


class Txt(object):
    # part of text configuration
    START_TXT = """<b>ʜᴇʏ {} 👋,
ɪ'ᴍ ᴠɪᴅᴇᴏꜱ ꜱᴀᴍᴩʟᴇ ʙᴏᴛ ᴜꜱᴇᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ꜱᴀᴍᴩʟᴇ ᴠɪᴅᴇᴏꜱ [ᴀɴᴅ ᴍᴏʀᴇ] ᴏꜰ ꜰɪʟᴇꜱ.

ꜱᴇɴᴅ ᴛʜᴇ ꜰɪʟᴇ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ. ☃️</b>"""

    ABOUT_TXT = """<b>╭───────────⍟
➥ Mʏ ɴᴀᴍᴇ : {}
➥ Pʀᴏɢʀᴀᴍᴇʀ : <a href=https://t.me/SyD_Xyz>ꪑ𝘳 𝘴ꪗᦔ 🌐</a> 
➥ Fᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/BOT_cracker>B𝚘ᴛ ᑕяΔ¢к℮ґ 🎋</a>
➥ Lɪʙʀᴀʀy : <a href=https://t.me/+oej8cujHMFJhNmI9>Cᴏʟʟᴇᴄᴛɪᴏɴ...</a>
➥ Lᴀɴɢᴜᴀɢᴇ: <a href=https://t.me/+0Zi1FC4ulo8zYzVl>Bᴀᴄᴋ-Uᴩ 💦</a>
➥ ᴍʏ ꜱᴇʀᴠᴇʀ : <a href=https://t.me/Mod_Moviez_X>Tɢ 🗯️</a>
➥ ᴠᴇʀsɪᴏɴ : v1.0
╰───────────────⍟ """

    HELP_TXT = """Hᴇʀᴇ Iꜱ Mʏ Hᴇʟᴩ Cᴏᴍᴍᴀɴᴅ.
    
<b>⦿ Dᴇᴠᴇʟᴏᴩᴇʀ:</b> <a href=https://t.me/SyD_Xyz>🔅 ᴍ.ʀ Sʏᦔ 🔅</a>
""" 
    PIC_TXT = """ 
◽ <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>
  
<b>•></b> /start Tʜᴇ Bᴏᴛ Aɴᴅ Sᴇɴᴅ Aɴy Pʜᴏᴛᴏ Tᴏ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟy Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /del_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Oʟᴅ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /view_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴɪʟᴇ.

<u><b><blockqoute>Jᴜꜱᴛ Sᴇɴᴅ Tʜᴇ Pɪᴄᴛᴜʀᴇ.. ⚡</blockqoute></u></b>"""

    SUFPRE_TXT = """ 
◽ <b><u>Sᴇᴛ ꜱᴜꜰꜰɪx ᴀɴᴅ ᴩʀᴇꜰɪx.</b></u>
<b>•></b> /set_prefix - Sᴇᴛ ᴩʀᴇꜰɪx(ꜰɪʀꜱᴛ ᴡᴏʀᴅ)
<b>•></b> /set_suffix - Sᴇᴛ ꜱᴜꜰꜰɪx(ʟᴀꜱᴛ ᴡᴏʀᴅ)
<b>•></b> /see_prefix - Sᴇᴇ ᴩʀᴇꜰɪx
<b>•></b> /see_suffix - Sᴇᴇ ꜱᴜꜰꜰɪx
<b>•></b> /del_prefix - Dᴇʟᴇᴛᴇ ᴩʀᴇꜰɪx
<b>•></b> /del_suffix - Dᴇʟᴇᴛᴇ ꜱᴜꜰꜰɪx
"""

    USR_TXT = """Aᴅᴅ Yᴏᴜʀ UꜱᴇʀBᴏᴛ Tᴏ Rᴇɴᴀᴍᴇ 2ɢʙ+ ꜰɪʟᴇꜱ.
◽ <b><u>Cᴏɴᴅɪᴛɪᴏɴ</u></b>
<b>•></b> Yᴏᴜ Mᴜꜱᴛ Hᴀᴠᴇ Pʀᴇᴍɪᴜᴍ"""
    HOW_TXT = """
◽ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
<b>•></b> Sᴇɴᴅ Aɴy Fɪʟᴇ Aɴᴅ Tyᴩᴇ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ \nAɴᴅ Sᴇʟᴇᴄᴛ Tʜᴇ Fᴏʀᴍᴀᴛ [ document, video, audio ].   
Sᴇɴᴅ Fɪʟᴇ Tᴏ Kɴᴏᴡ Mᴏʀᴇ.. 😮‍💨"""
    CAP_TXT = """
◽ <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>

<b>•></b> /set_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴛ ᴀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /see_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /del_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
Exᴀᴍᴩʟᴇ:- <code> /set_caption 📕 Fɪʟᴇ Nᴀᴍᴇ: {filename}
💾 Sɪᴢᴇ: {filesize}
⏰ Dᴜʀᴀᴛɪᴏɴ: {duration} </code>
"""
    
    META_TXT = """
❪ SET CUSTOM METADATA ❫
◽ <b><u>Tᴏ Cʜᴀɴɢᴇ Fɪʟᴇ Iɴꜰᴏʀᴍᴀᴛɪᴏɴꜱ </b></u>
<b>•></b> /metadata - Tᴏ ᴛᴜʀɴ ᴏꜰꜰ/ᴏɴ ᴀɴᴅ ꜱᴇᴇ ᴍᴇᴛᴀᴅᴀᴛᴀ
<b>•></b> /set_metadata - Tᴏ ᴄʜᴀɴɢᴇ ᴍᴇᴛᴅᴀᴛᴀ
☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

◦ <code> --change-title Powered By:- @ --change-author @ --change-video-title By:- @ --change-audio-title By :- @ --change-subtitle-title Subtitled By :- @ </code>

📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛᴀᴄᴛ..: @SyD_XyZ
"""
    DUMP_TXT = """<b><u>Dᴜᴍᴩ Cʜᴀɴɴᴇʟ:</u></b>
A Cʜᴀɴɴᴇʟ Tᴏ Wʜɪᴄʜ Aʟʟ Rᴇɴᴀᴍᴇᴅ Fɪʟᴇꜱ Mᴜꜱᴛ Bᴇ Sᴇɴᴛ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟ
◽ <b><u>Sᴇᴛ ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ.</b></u>
<b>•></b> /set_dump - Sᴇᴛ ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ
<b>•></b> /del_dump - Dᴇʟᴇᴛᴇ ᴅᴜᴍᴩ(ᴅᴇꜰᴜᴀʟᴛ ᴛᴏ ᴛʜᴇ ꜱᴇɴᴅᴇʀ ɪᴅ)
<b>•></b> /see_dump - Sᴇᴇ ᴄᴜʀʀᴇɴᴛ ᴅᴜᴍᴩ ɪᴅ"""
    
    SEND_METADATA = """
❪ SET CUSTOM METADATA ❫

☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

◦ <code> --change-title Powered By:- @ --change-author @ --change-video-title By:- @ --change-audio-title By :- @ --change-subtitle-title Subtitled By :- @ </code>

📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛᴀᴄᴛ..: @SyD_XyZ
"""

    STATS_TXT = """
╔════❰ Sᴇʀᴠᴇʀ sᴛᴀᴛS  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ ᴜᴩᴛɪᴍᴇ: `{0}`
║┣⪼ ᴛᴏᴛᴀʟ sᴘᴀᴄᴇ: `{1}`
║┣⪼ ᴜsᴇᴅ: `{2} ({3}%)`
║┣⪼ ꜰʀᴇᴇ: `{4}`
║┣⪼ ᴄᴘᴜ: `{5}%`
║┣⪼ ʀᴀᴍ: `{6}%`
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪        
"""

    PROGRESS_BAR = """<b>\n
╭━━━━❰Pʀᴏɢʀεss ʙΔʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
┣⪼ 🩷 Bꪗ: @Bot_Cracker 🎋
╰━━━━━━━━━━━━━━━➣ </b>"""
