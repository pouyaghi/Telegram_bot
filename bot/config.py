import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
MAX_HISTORY = 400
MAX_MESSAGE_LENGTH = 4096