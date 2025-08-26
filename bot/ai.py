from config import GENAI_API_KEY
import google.genai as genai
from google.genai import types as genai_types
from memory import get_user_profile

client = genai.Client(api_key=GENAI_API_KEY)

grounding_tool = genai_types.Tool(
    google_search=genai_types.GoogleSearch()
)

generation_config = genai_types.GenerateContentConfig(
    tools=[grounding_tool]
)

async def generate_ai_reply(user_text: str, user_id: int = None) -> str:
    """
    Generate personalized AI response.
    Includes user profile if available.
    """
    try:
        prompt = user_text
        if user_id:
            profile = get_user_profile(user_id)
            if profile:
                name = profile.get("name") or "User"
                tone = profile.get("tone", "friendly")
                notes = profile.get("notes", [])
                last_msg = profile.get("last_message", "")
                notes_text = ", ".join(notes) if notes else ""
                
                prompt = (
                    f"You are talking to {name}. "
                    f"Respond in a {tone} tone. "
                    f"User last said: '{last_msg}'. "
                    f"User notes: '{notes_text}'.\n\n"
                    f"Current message: {user_text}"
                )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=generation_config,
        )
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return f"⚠️ Error generating response: {e}"
