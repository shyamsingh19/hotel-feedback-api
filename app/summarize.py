import openai
import os

from dotenv import load_dotenv

load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_comments(theme: str, comments: list[str]) -> str:
    if not comments:
        return "No feedback for this theme."

    prompt = (
        f"Summarize the following hotel guest comments about {theme}:\n"
        + "\n".join(comments)
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
