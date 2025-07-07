from dotenv import load_dotenv
load_dotenv()

import os
import requests
import google.generativeai as genai
import re
import json

# ✅ Load Gemini API key from .env
genai.configure(api_key=os.getenv("OPENAI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")


# ✅ Helper: Extract name, email, date, time from LLM response
def extract_booking_details(text):
    name = re.search(r"name\s*is\s*(\w+)", text, re.IGNORECASE)
    email = re.search(r"email\s*is\s*([\w\.-]+@[\w\.-]+)", text, re.IGNORECASE)
    date = re.search(r"(\d{4}-\d{2}-\d{2})", text)  # YYYY-MM-DD
    time = re.search(r"(\d{1,2}:\d{2})", text)      # HH:MM

    return {
        "name": name.group(1) if name else None,
        "email": email.group(1) if email else None,
        "date": date.group(1) if date else None,
        "time": time.group(1) if time else None
    }


# ✅ Main function to run Gemini and book
def ask_agent(prompt: str) -> str:
    try:
        instruction = (
            "Extract user's name, email, date (in YYYY-MM-DD format), and time (in HH:MM 24-hour format) from the following message. "
            "If user says 'tomorrow' or 'next Monday', convert that to the actual date. "
            "Respond ONLY in valid JSON format like this:\n"
            '{ "name": "Name", "email": "email@example.com", "date": "2025-07-06", "time": "14:00" }\n\n'
            f"Message: {prompt}"
        )

        response = model.generate_content(instruction)
        raw_reply = response.text.strip()

        # Extract the first valid JSON block using regex
        json_block = re.search(r"\{.*\}", raw_reply, re.DOTALL)
        if not json_block:
            return "❌ Gemini didn't return structured data. Please try again clearly."

        # Load it as JSON
        data = json.loads(json_block.group())

        # Validate extracted data
        required_fields = ["name", "email", "date", "time"]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return f"❌ Missing fields: {', '.join(missing)}. Please include them in your message."

        # Call your FastAPI booking backend
        backend_url = "http://127.0.0.1:8000/book"
        res = requests.post(backend_url, json=data)

        if res.status_code == 200:
            return res.json().get("message", "✅ Booked successfully.")
        else:
            return "❌ Booking API failed. Please try again."

    except Exception as e:
        return f"❌ Agent error: {str(e)}"

# for m in genai.list_models():
#     print(m.name)
