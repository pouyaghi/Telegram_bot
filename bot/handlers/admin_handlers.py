# bot/handlers/admin_handlers.py
from aiogram import types
from config import ADMIN_ID

def register(dp):
    @dp.message_handler(lambda m: m.from_user.id == ADMIN_ID, commands=["broadcast"])
    async def broadcast(message: types.Message):
        # Example: broadcast message to all stored chat_ids
        from memory import chat_history
        text = message.get_args()
        if not text:
            await message.reply("Please provide a message to broadcast.")
            return
        for chat_id in chat_history.keys():
            try:
                await dp.bot.send_message(chat_id, f"[Admin broadcast]: {text}")
            except Exception as e:
                print(f"Failed to send to {chat_id}: {e}")
        await message.reply("Broadcast sent!")
