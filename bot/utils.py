# bot/utils.py
from aiogram.utils.exceptions import MessageTextIsEmpty
from formatting import to_telegram_html
from config import MAX_MESSAGE_LENGTH  # ✅ use the shared config value

async def safe_send(chat_id, text, bot):
    if not text:
        return

    try:
        clean_text = to_telegram_html(text)

        # Split into chunks if too long
        for i in range(0, len(clean_text), MAX_MESSAGE_LENGTH):
            chunk = clean_text[i : i + MAX_MESSAGE_LENGTH]
            await bot.send_message(chat_id, chunk, parse_mode="HTML")

    except MessageTextIsEmpty:
        pass
