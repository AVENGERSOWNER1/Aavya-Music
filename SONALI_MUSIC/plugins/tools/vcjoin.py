from SONALI_MUSIC import app
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges

# पहले से जॉइन किए गए यूज़र्स को स्टोर करने के लिए एक सेट
video_chat_users = {}

async def check_video_chat(chat_id):
    while True:
        try:
            participants = await app.get_participants(chat_id)
            
            # अगर वीडियो चैट के लिए यूज़र्स सेट में पहले से हैं
            if chat_id not in video_chat_users:
                video_chat_users[chat_id] = set()

            # सभी पार्टिसिपेंट्स चेक करें
            for user in participants:
                if user.id not in video_chat_users[chat_id]:
                    video_chat_users[chat_id].add(user.id)

                    mention = f"[{user.first_name}](tg://user?id={user.id})"
                    username = f"@{user.username}" if user.username else "No Username"
                    user_id = user.id

                    message = f"**⚘ ᴊσɪηєᴅ ᴠɪᴅєᴏ ᴄʜᴧᴛ**\n\n**:⧽ ηᴧϻє :** {mention}\n**:⧽ ᴜsєʀ ɪᴅ :** `{user_id}`\n**:⧽ ᴜsєʀηᴧϻє :** {username}"
                    
                    msg = await app.send_message(chat_id, message)
                    await asyncio.sleep(60)  # 1 मिनट बाद मैसेज डिलीट करें
                    await app.delete_messages(chat_id, msg.message_id)  # मैसेज डिलीट करें

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(10)  # हर 10 सेकंड में चेक करें

# जब बॉट किसी ग्रुप में ऐड हो तो ऑटो स्टार्ट हो
@app.on_message(filters.command("start") & filters.group)
async def start_video_check(client, message):
    chat_id = message.chat.id
    if chat_id not in video_chat_users:
        video_chat_users[chat_id] = set()
        asyncio.create_task(check_video_chat(chat_id))  # बैकग्राउंड में चेक करना शुरू करें
        await message.reply("✅ **Video Chat Detection Started for this group!**")
