import requests
from googletrans import Translator
import deepl
from dotenv import load_dotenv

import logging

from os import getenv

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

load_dotenv("../config.env")
SUMMARIZATION_MODEL_NAME = getenv("SUMMARIZATION_MODEL_NAME")

translator = Translator()


# def load_summarization_model(model_name=SUMMARIZATION_MODEL_NAME):
#     return AutoModelForSeq2SeqLM.from_pretrained(model_name)

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def translate(text: str) -> str:
    language = translator.detect(text).lang
    # if language != "en":
    #     text = translator.translate(text, dest='en').text
    return language


def translate_2(text: str, src_lang: str) -> str:
    translator_2 = deepl.translate(source_language=src_lang, target_language="EN", text=text)
    return translator_2


def run(text: str) -> str:
    output = query({
        "inputs": text,
    })
    return output[0]["summary_text"]
