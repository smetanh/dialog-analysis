import googletrans
import deepl
from collections import deque
from dotenv import load_dotenv
from os import getenv


load_dotenv("../config.env")
DEEPL_TOKEN = getenv("DEEPL_TOKEN")

google_translator = googletrans.Translator()
deepl_translator = deepl.Translator(DEEPL_TOKEN)


def detect_language(text: str | deque) -> str:
    if isinstance(text, deque):
        text = "\n".join(text)

    language = google_translator.detect(text).lang

    if language == "en":
        language = "en-us"

    return language


def translate(text: str | deque, target_language: str) -> str:
    if isinstance(text, deque):
        text = "\n".join(text)

    result = deepl_translator.translate_text(text, target_lang=target_language).text

    return result
