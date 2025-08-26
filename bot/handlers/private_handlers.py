# bot/handlers/private_handlers.py
from aiogram import types
from ai import generate_ai_reply
from utils import safe_send
from config import ADMIN_ID
from memory import store_message, get_conversation_history


def register(dp):
    @dp.message_handler(lambda m: m.chat.type == "private")
    async def handle_private_messages(message: types.Message):
        # 1. Forward user message to admin
        try:
            await message.forward(ADMIN_ID)
        except Exception as e:
            print(f"Forward failed: {e}")

        # 2. Save user message to memory
        store_message(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message_text=message.text
        )

        # 3. Get conversation history
        history = get_conversation_history(message.chat.id, message.from_user.id)

        # 4. Generate AI reply (personalized, with history)
        answer = await generate_ai_reply(
            user_message=message.text,
            user_id=message.from_user.id,
            history=history
        )

        # 5. Save bot reply to memory
        store_message(
            chat_id=message.chat.id,
            user_id="bot",
            message_text=answer
        )

        # 6. Send reply safely
        await safe_send(message.chat.id, answer, dp.bot)
