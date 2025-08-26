from aiogram import types, Dispatcher
from aiogram.types import BotCommand
from ai import generate_ai_reply
from memory import store_message, get_history
from utils import safe_send
from config import ADMIN_ID

def register_handlers(dp: Dispatcher):

    # /start and /help
    @dp.message_handler(commands=["start", "help"])
    async def send_welcome(message: types.Message):
        await message.reply("Hello! I'm your Gemini-powered bot 🤖")

    # /about
    @dp.message_handler(commands=["about"])
    async def about(message: types.Message):
        await message.reply(
            "I am Pouya's little digital spark. Here to chat and have fun!"
        )

    # /ask
    @dp.message_handler(commands=["ask"])
    async def ask_handler(message: types.Message):
        if message.chat.type in ["group", "supergroup", "channel", "private"]:
            user_text = message.get_args()
            if not user_text:
                await message.reply("Please provide a question after /ask.")
                return
            answer = await generate_ai_reply(user_text)
            await safe_send(message.chat.id, answer, dp.bot)

    # /summarize
    @dp.message_handler(commands=["summarize"])
    async def summarize_handler(message: types.Message):
        chat_id = message.chat.id
        history = get_history(chat_id)
        if not history:
            await message.reply("No messages to summarize yet.")
            return
        history_text = "\n".join(history)
        prompt = f"Summarize the following conversation clearly and concisely:\n\n{history_text}"
        summary = await generate_ai_reply(prompt)
        await safe_send(chat_id, summary, dp.bot)

    # Store all messages for history
    @dp.message_handler(lambda m: m.chat.type in ["group", "supergroup", "channel", "private"])
    async def store_messages(message: types.Message):
        if message.text is None or message.text.startswith("/") or message.from_user.is_bot:
            return
        text = f"{message.from_user.first_name}: {message.text}"
        store_message(message.chat.id, message.from_user.id, text)

        # For private messages, forward to admin
        if message.chat.type == "private":
            try:
                await message.forward(ADMIN_ID)
            except Exception as e:
                print(f"Forward failed: {e}")
            # Optional: reply with AI
            answer = await generate_ai_reply(message.text)
            await safe_send(message.chat.id, answer, dp.bot)
    
    @dp.message_handler(commands=["set_tone"])
    async def set_tone(message: types.Message):
        tone = message.get_args()
        if not tone:
            await message.reply("Please provide a tone: friendly, formal, funny, etc.")
            return
        from memory import set_user_tone
        set_user_tone(message.from_user.id, tone)
        await message.reply(f"Your tone is now set to '{tone}'!")
