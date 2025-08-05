import os
import openai
import re
import nltk
from collections import defaultdict
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv(override=True)


nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


def get_negative_theme_ratio(comments: List[str]) -> Dict[str, float]:
    theme_counts = defaultdict(int)
    negative_counts = defaultdict(int)

    for comment in comments:
        theme = group_with_openai(comment)
        sentiment = sia.polarity_scores(comment)

        theme_counts[theme] += 1
        if sentiment["compound"] <= -0.05:
            negative_counts[theme] += 1

    ratios = {}
    for theme, total in theme_counts.items():
        if total > 0:
            ratios[theme] = round(negative_counts[theme] / total, 2)

    return ratios


THEMES = ["Cleanliness", "Staff & Service", "Food & Dining", "Location", "Amenities"]

KEYWORDS = {
    "Cleanliness": ["clean", "dirty", "spotless", "tidy", "hygiene"],
    "Staff & Service": ["staff", "rude", "friendly", "helpful", "service", "check-in"],
    "Food & Dining": ["food", "breakfast", "dinner", "meal", "restaurant"],
    "Location": ["location", "area", "neighborhood", "walk", "near", "convenient"],
    "Amenities": ["pool", "wifi", "spa", "gym", "facility", "parking"],
}


def group_with_openai(comment: str) -> str:
    prompt = f"""
You are an AI that categorizes hotel guest comments into one of these themes:
{", ".join(THEMES)}.

Comment:
\"\"\"{comment}\"\"\"

Which single theme does this comment fit best?
Just reply with the theme name.
"""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        theme = response["choices"][0]["message"]["content"].strip()
        return theme if theme in THEMES else group_with_keywords(comment)
    except Exception:
        return group_with_keywords(comment)


def group_with_keywords(comment: str) -> str:
    comment_lower = comment.lower()
    scores = {theme: 0 for theme in THEMES}
    for theme, keywords in KEYWORDS.items():
        for kw in keywords:
            matches = len(re.findall(rf"\b{re.escape(kw)}\b", comment_lower))
            scores[theme] += matches
    return max(scores, key=scores.get)


def group_feedback_by_theme(comments: list[str]) -> dict[str, list[str]]:
    theme_map = {theme: [] for theme in THEMES}
    for comment in comments:
        theme = group_with_openai(comment)
        theme_map[theme].append(comment)
    return theme_map
