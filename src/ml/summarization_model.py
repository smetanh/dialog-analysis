from collections import deque
import requests
from os import getenv
import logging

from dotenv import load_dotenv
import emoji
# import deepl
from src.translator.translate import translate


load_dotenv("../config.env")
API_URL = getenv("SUMMARIZATION_MODEL_API_URL")
MODEL_TOKEN = getenv("SUMMARIZATION_MODEL_TOKEN")
# DEEPL_TOKEN = getenv("DEEPL_TOKEN")

headers = {"Authorization": f"Bearer {MODEL_TOKEN}"}

# translator = deepl.Translator(DEEPL_TOKEN)


# def translate(text: str, target_language: str) -> str:
#     if target_language.lower() == "en":
#         target_language = "en-us"
#     result = translator.translate_text(text, target_lang=target_language).text
#     return result


# def translate0(text: str) -> str:
#     import requests
#
#     API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
#     headers = {"Authorization": "Bearer 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"}
#
#     def query(payload):
#         response = requests.post(API_URL, headers=headers, json=payload)
#         return response.json()
#
#     output = query({
#         "inputs": text,
#         "parameters": {"src_lang": "ru_RU", "tgt_lang": "en_XX"}
#     })
#
#     # print(output)
#
#     return output[0]["translation_text"]


def message_preprocess(text: deque) -> str:
    message = "\n".join(text)
    message = translate(message, "en")
    message = emoji.demojize(message, delimiters=(" ", " ")).replace("_", " ")
    return message


def query2(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def run(text: deque) -> str:
    message = message_preprocess(text)
    logging.info("+++")
    logging.info(message)

    output = query2({
        "inputs": message
    })
    logging.info(output)

    return output[0]["summary_text"]
