from collections import deque
from os import getenv
import logging

from dotenv import load_dotenv
import googletrans
import deepl


load_dotenv("../config.env")
DEEPL_TOKEN = getenv("DEEPL_TOKEN")

google_translator = googletrans.Translator()
deepl_translator = deepl.Translator(DEEPL_TOKEN)


def detect_language(text: str | deque | list) -> str:
    if isinstance(text, list):
        logging.info("===LIST")
        # for i in range(len(text)):
        #     text[i] = ", ".join(text[i])
        text = "\n".join(text)
    elif isinstance(text, deque):
        logging.info("===DEQUE")
        text = "\n".join(text)

    logging.info("===TEXT DETECTED LANG")
    logging.info(text)

    language = google_translator.detect(text).lang
    if language.lower() == "en":
        language = "en-us"

    return language


def translate(text: str | deque | list, target_language: str) -> str:
    if isinstance(text, list):
        # for i in range(len(text)):
        #     text[i] = ", ".join(text[i])
        text = "\n".join(text)
    elif isinstance(text, deque):
        text = "\n".join(text)

    result = deepl_translator.translate_text(text, target_lang=target_language).text
    return result
