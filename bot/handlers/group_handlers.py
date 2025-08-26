# bot/handlers/group_handlers.py
from aiogram import types
from memory import store_message, get_conversation_history
from ai import generate_ai_reply
from utils import safe_send


def register(dp):
    @dp.message_handler(lambda m: m.chat.type in ["group", "supergroup"])
    async def handle_group_messages(message: types.Message):
        # 1. Ignore commands and bot messages
        if (
            message.text is None
            or message.text.startswith("/")
            or message.from_user.is_bot
        ):
            return

        # 2. Save message to memory
        store_message(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message_text=message.text
        )

        # 3. Get conversation history (optional, only if you want AI to use memory in groups too)
        history = get_conversation_history(message.chat.id, message.from_user.id)

        # 4. Simple condition: bot replies only if mentioned
        if f"@{(await dp.bot.me).username}" in message.text:
            user_message = message.text.replace(f"@{(await dp.bot.me).username}", "").strip()

            # Generate AI reply with history
            answer = await generate_ai_reply(
                user_message=user_message,
                user_id=message.from_user.id,
                history=history
            )

            # Save bot reply to memory
            store_message(message.chat.id, "bot", answer)

            # Send reply
            await safe_send(message.chat.id, f"@{message.from_user.username} {answer}", dp.bot)
