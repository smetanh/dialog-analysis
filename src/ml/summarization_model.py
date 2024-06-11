from src.translator.translate import translate

from collections import deque
from os import getenv
import requests
import logging

from dotenv import load_dotenv
import emoji


load_dotenv("../config.env")
API_URL = getenv("SUMMARIZATION_MODEL_API_URL")
MODEL_TOKEN = getenv("SUMMARIZATION_MODEL_TOKEN")

headers = {"Authorization": f"Bearer {MODEL_TOKEN}"}


def message_pre_processing(text: deque) -> str:
    message = "\n".join(text)
    message = translate(message, "en-us")
    message = emoji.demojize(message, delimiters=(" ", " ")).replace("_", " ")
    return message


def message_post_processing(text: list) -> str:
    message = text[0]["summary_text"]
    message = message.strip()
    return message


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_summary(text: deque) -> str:
    message = message_pre_processing(text)
    output = query({
        "inputs": message
    })

    result = message_post_processing(output)
    return result
