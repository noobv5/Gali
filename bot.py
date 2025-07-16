from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import config

bot = Client("mybot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# message.txt ফাইল থেকে মেসেজগুলো লোড করে
def load_messages():
    with open("message.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# ১টি session দিয়ে যত মেসেজ পাঠানো যায় ১ মিনিটের মধ্যে
async def send_from_session(session_str, username, messages, index):
    results = []
    try:
        async with Client(session_str, config.API_ID, config.API_HASH) as app:
            user = await app.get_users(username)
            for i, msg in enumerate(messages, 1):
                await app.send_message(chat_id=user.id, text=msg)
                results.append(f"✅ Session {index}: Sent message {i}")
                await asyncio.sleep(1)  # optionally delay
    except Exception as e:
        results.append(f"❌ Session {index} Error: {e}")
    return results

# একসাথে সব session চালাবে, কিন্তু ৬০ সেকেন্ড পার হলে বন্ধ করবে
async def send_all_with_timeout(username: str, messages: list):
    tasks = []
    for idx, session in enumerate(config.SESSIONS, 1):
        task = asyncio.create_task(send_from_session(session, username, messages, idx))
        tasks.append(task)

    try:
        done, pending = await asyncio.wait(tasks, timeout=60)
        results = []
        for d in done:
            results.extend(d.result())

        for p in pending:
            p.cancel()
            results.append("⏰ Time limit reached. Cancelled remaining tasks.")

        return results
    except Exception as e:
        return [f"❌ Global Error: {e}"]

# /send command handler
@bot.on_message(filters.command("send") & filters.private)
async def send_handler(client: Client, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("⚠️ ব্যবহার: /send @username")
            return

        username = parts[1].replace("@", "")
        messages = load_messages()

        await message.reply(f"🚀 @{username} কে ৩টি session দিয়ে মেসেজ পাঠানো শুরু হয়েছে... (সর্বোচ্চ ১ মিনিট)")

        result = await send_all_with_timeout(username, messages)

        await message.reply("\n".join(result))
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

bot.run()