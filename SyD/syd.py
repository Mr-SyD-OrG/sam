import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
active_users = set()
queued_users = {}
RESOLUTIONS = ["360", "480", "720", "1080"]

async def get_duration_from_telegram(client, file_id):
    tg_file = await client.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{Config.MRSYD}/{tg_file.file_path}"

    proc = await asyncio.create_subprocess_exec(
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return float(stdout.decode().strip())

def humanbytes(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def generate_progress_bar(percentage):
    filled = int(percentage // 10)
    return "[" + "█" * filled + "░" * (10 - filled) + "]"

def calculate_times(diff, current, total, speed):
    elapsed = time.strftime("%H:%M:%S", time.gmtime(diff))
    try:
        remaining = (total - current) / speed
        estimated = diff + remaining
        return elapsed, time.strftime("%H:%M:%S", time.gmtime(remaining)), time.strftime("%H:%M:%S", time.gmtime(estimated))
    except:
        return elapsed, "?", "?"

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.0) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed, eta, total_time = calculate_times(diff, current, total, speed)
        progress = generate_progress_bar(percentage)

        try:
            await message.edit(
                f"{ud_type}\n\n"
                f"{progress}\n"
                f"**{round(percentage, 2)}%** | {humanbytes(current)} of {humanbytes(total)}\n"
                f"📶 ѕᴘᴇᴇᴅ: {humanbytes(speed)}/s | 🕐 ᴇᴛᴀ: {eta}"
            )
        except:
            pass

async def get_duration(file_path: str) -> float:
    proc = await asyncio.create_subprocess_exec(
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return float(stdout.decode().strip())

async def run_ffmpeg(cmd: list):
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await proc.communicate()


@Client.on_message(filters.video | filters.document)
async def media_handler(client, message):
    media = message.video or message.document
    if not media:
        return await message.reply("❌ ɴᴏ ᴠᴀʟɪᴅ ᴍᴇᴅɪᴀ ꜰᴏᴜɴᴅ.")

    wait_msg = await message.reply("🔍 ɢᴇᴛᴛɪɴɢ ᴍᴇᴅɪᴀ ɪɴꜰᴏ...")
    duration = await get_duration_from_telegram(client, media.file_id)

    keyboard = []
    for res in RESOLUTIONS:
        bitrate = BITRATE_MAP[res]
        size_bytes = (bitrate * 1000 / 8) * duration
        size_mb = size_bytes / (1024 * 1024)
        size_text = f"{res}p (~{int(size_mb)}MB)"
        sample_text = f"Sample {res}p"
        keyboard.append([
            InlineKeyboardButton(size_text, callback_data=f"res_{res}"),
            InlineKeyboardButton(sample_text, callback_data=f"sample_{res}")
        ])

    keyboard.append([InlineKeyboardButton("Custom Size", callback_data="res_custom")])

    await wait_msg.edit_text(
        f"ᴇꜱᴛɪᴍᴀᴛᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ: `{int(duration)}s`\n\nꜱᴇʟᴇᴄᴛ ʀᴇꜱᴏʟᴜᴛɪᴏɴ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



@Client.on_callback_query(filters.regex("^queue_"))
async def add_to_queue(client, query):
    user_id = query.from_user.id
    data = query.data.split("_", 1)[1]
    queued_users[user_id] = (query, data)
    await query.message.edit("✅ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ. ʏᴏᴜʀ ᴛᴀꜱᴋ ᴡɪʟʟ ʙᴇ ᴘʀᴏᴄᴇꜱꜱᴇᴅ ɴᴇxᴛ.")

@Client.on_callback_query(filters.regex("^(res|sample)_|res_custom$"))
async def handle_conversion(client, query):
    user_id = query.from_user.id
    data = query.data

    if user_id in active_users:
        await query.message.reply(
            "⚠ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀ ᴘʀᴏᴄᴇꜱꜱ ʀᴜɴɴɪɴɢ.\n\nᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ǫᴜᴇᴜᴇ ᴛʜɪꜱ ᴛᴀꜱᴋ?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Yes", callback_data=f"queue_{data}")],
                [InlineKeyboardButton("❌ No", callback_data="cancel_queue")]
            ])
        )
        return

    await process_file(client, query, user_id, data)



async def process_file(client, query, user_id, mode):
    active_users.add(user_id)
    msg = await query.message.edit("⏬ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰɪʟᴇ...")

    try:
        file_msg = query.message.reply_to_message
        if not file_msg or not (file_msg.video or file_msg.document):
            await msg.edit("❌ ɴᴏ ᴠᴀʟɪᴅ ᴍᴇᴅɪᴀ ꜰᴏᴜɴᴅ.")
            return

        start = time.time()
        file_path = await file_msg.download(
            progress=progress_for_pyrogram,
            progress_args=("⬇ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...", msg, start)
        )

        output = f"converted_{user_id}.mp4"

        if mode == "res_custom":
            await msg.edit("ᴇɴᴛᴇʀ ᴛᴀʀɢᴇᴛ ꜱɪᴢᴇ ɪɴ ᴍʙ:")
            user_input = await client.listen(user_id, timeout=60)
            size = int(user_input.text.strip())

            duration = await get_duration(file_path)
            bitrate = (size * 8192) / duration
            cmd = ["ffmpeg", "-i", file_path, "-b:v", f"{int(bitrate)}k", "-preset", "fast", output]
        elif mode.startswith("sample_"):
            res = mode.split("_")[1]
            duration = await get_duration(file_path)
            start_pos = max(1, int(duration) // 2 - 15) if duration > 30 else 0
            cmd = [
                "ffmpeg", "-ss", str(start_pos), "-t", "30",
                "-i", file_path,
                "-vf", f"scale=-2:{res}", "-c:v", "libx264",
                "-preset", "fast", "-c:a", "aac", output
            ]
        else:
            res = mode.split("_")[1]
            cmd = [
                "ffmpeg", "-i", file_path,
                "-vf", f"scale=-2:{res}",
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "copy", output
            ]

        await msg.edit("⚙ ᴄᴏɴᴠᴇʀᴛɪɴɢ ꜰɪʟᴇ...")
        await run_ffmpeg(cmd)

        if not os.path.exists(output):
            await msg.edit("❌ ᴄᴏɴᴠᴇʀꜱɪᴏɴ ꜰᴀɪʟᴇᴅ.")
            return

        await msg.edit("⏫ ᴜᴘʟᴏᴀᴅɪɴɢ ꜰɪʟᴇ...")
        up_start = time.time()
        await query.message.reply_video(
            output,
            caption="✅ ᴄᴏɴᴠᴇʀꜱɪᴏɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.",
            progress=progress_for_pyrogram,
            progress_args=("⬆ ᴜᴘʟᴏᴀᴅɪɴɢ...", msg, up_start)
        )

    except Exception as e:
        await msg.edit(f"❌ ᴇʀʀᴏʀ: `{e}`")
    finally:
        active_users.discard(user_id)
        if user_id in queued_users:
            queued_query, queued_data = queued_users.pop(user_id)
            await process_file(client, queued_query, user_id, queued_data)
        try:
            os.remove(file_path)
            os.remove(output)
        except:
            pass
