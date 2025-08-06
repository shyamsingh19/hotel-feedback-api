import openai
import os
import time
import requests

from dotenv import load_dotenv

load_dotenv(override=True)
# openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_content(prompt: str, model="gemini-2.0-flash", max_retries=3) -> str:
    try:
        print(f"Running generate_content for prompt: {prompt}")
        GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": os.getenv("GEMINI_API_KEY"),
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3},
        }

        for attempt in range(max_retries):
            response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]

            elif response.status_code == 429:
                print(" Rate limit hit.")
                try:
                    retry_delay = response.json()["error"]["details"][2]["retryDelay"]
                    seconds = int(retry_delay.replace("s", ""))
                except:
                    seconds = 10  # default fallback
                print(f" Retrying in {seconds} seconds... (attempt {attempt + 1})")
                time.sleep(seconds)
            else:
                raise Exception(f" API error {response.status_code}: {response.text}")

        raise Exception(" All retries failed.")

    except Exception as e:
        raise Exception(f"Error generating content: {e}")


def summarize_comments(theme: str, comments: list[str]) -> str:
    if not comments:
        return "No feedback for this theme."

    prompt = (
        f"Summarize the following hotel guest comments about {theme}:\n\n"
        + "\n".join(f"- {comment}" for comment in comments)
    )

    try:
        return generate_content(prompt).strip()
    except Exception as e:
        return f"Error summarizing comments: {e}"
