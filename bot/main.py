from aiogram import Bot, Dispatcher, executor
from config import API_TOKEN
from commands import register_handlers
from aiogram.types import BotCommand

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Register handlers
register_handlers(dp)

# Set bot commands on startup
async def on_startup(dp):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help message"),
        BotCommand(command="about", description="About this bot"),
        BotCommand(command="ask", description="Ask Gemini AI a question"),
        BotCommand(command="summarize", description="Summarize last 400 messages")
    ]
    await bot.set_my_commands(commands)
    print("Bot started and commands set!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
