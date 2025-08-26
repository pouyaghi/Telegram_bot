# bot/formatting.py
import re

def to_telegram_html(text: str) -> str:
    """
    Convert Gemini-style Markdown (**bold**, *italic*) into Telegram HTML formatting.
    """
    if not text:
        return ""

    # Convert bold (**text** → <b>text</b>)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Convert italic (*text* → <i>text</i>)
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)\*(?<!\*)", r"<i>\1</i>", text)

    # Replace unordered list stars with dashes
    text = re.sub(r"^\s*[\*\-]\s+", "- ", text, flags=re.MULTILINE)

    # (Optional) Clean extra stars left behind
    text = text.replace("*", "")

    return text
