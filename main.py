import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import BotCommand
import google.genai as genai
from google.genai import types as genai_types
import asyncio

# ---------------- CONFIG ----------------
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ---------------- GEMINI ----------------
client = genai.Client(api_key=GENAI_API_KEY)

# Grounding tool (Google Search)
grounding_tool = genai_types.Tool(
    google_search=genai_types.GoogleSearch()
)

# Config with grounding enabled
generation_config = genai_types.GenerateContentConfig(
    tools=[grounding_tool]
)

# ---------------- TELEGRAM ----------------
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

MAX_HISTORY = 400  # Number of messages to keep for summary
MAX_MESSAGE_LENGTH = 4096
chat_history = {}

# ---------------- SAFE SEND ----------------
async def safe_send(chat_id: int, text: str, bot):
    """Send text safely by splitting into chunks if too long."""
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        await bot.send_message(chat_id, text[i:i+MAX_MESSAGE_LENGTH])

# ---------------- COMMANDS ----------------
commands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="Show help message"),
    BotCommand(command="about", description="About this bot"),
    BotCommand(command="ask", description="Ask Gemini AI a question"),
    BotCommand(command="summarize", description="Summarize last 400 messages")
]

async def on_startup(dp):
    await bot.set_my_commands(commands)
    print("Bot started and commands set!")

# ---------------- GEMINI RESPONSE ----------------
async def generate_ai_reply(user_text: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
            config=generation_config,
        )
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return f"⚠️ Error generating response: {e}"

# ---------------- COMMAND HANDLERS ----------------
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I'm your Gemini-powered bot 🤖")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("Send me a message, and I'll respond using Gemini AI!")

@dp.message_handler(commands=["about"])
async def about(message: types.Message):
    await message.answer("I am Pouya's little digital spark. Here to chat and have fun!")

# ---------------- ASK HANDLER (GROUPS/CHANNELS) ----------------
@dp.message_handler(commands=["ask"])
async def ask_handler(message: types.Message):
    if message.chat.type in ["group", "supergroup", "channel"]:
        user_text = message.get_args()
        if not user_text:
            await message.reply("Please provide a question after /ask.")
            return
        answer = await generate_ai_reply(user_text)
        await safe_send(message.chat.id, answer, bot)

# ---------------- SUMMARIZE HANDLER ----------------
@dp.message_handler(commands=["summarize"])
async def summarize_handler(message: types.Message):
    chat_id = message.chat.id

    if chat_id not in chat_history or not chat_history[chat_id]:
        await message.reply("No messages to summarize yet.")
        return

    history_text = "\n".join(chat_history[chat_id])
    prompt = f"Summarize the following conversation clearly and concisely:\n\n{history_text}"
    summary = await generate_ai_reply(prompt)
    await safe_send(chat_id, summary, bot)

# ---------------- STORE GROUP MESSAGES ----------------
@dp.message_handler(lambda m: m.chat.type in ["group", "supergroup", "channel"])
async def store_group_messages(message: types.Message):
    # Ignore commands and bot messages
    if message.text is None or message.text.startswith("/") or message.from_user.is_bot:
        return

    chat_id = message.chat.id
    text = f"{message.from_user.first_name}: {message.text}"

    if chat_id not in chat_history:
        chat_history[chat_id] = []

    chat_history[chat_id].append(text)

    # Keep only the last MAX_HISTORY messages
    if len(chat_history[chat_id]) > MAX_HISTORY:
        chat_history[chat_id] = chat_history[chat_id][-MAX_HISTORY:]

# ---------------- HANDLE PRIVATE MESSAGES ----------------
@dp.message_handler(lambda m: m.chat.type == "private")
async def private_message_handler(message: types.Message):
    # Forward to admin
    try:
        await message.forward(ADMIN_ID)
    except Exception as e:
        print(f"Forward failed: {e}")

    # Reply with AI
    answer = await generate_ai_reply(message.text)
    await safe_send(message.chat.id, answer, bot)

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
