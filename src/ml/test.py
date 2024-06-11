import requests
import logging
from os import getenv

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from dotenv import load_dotenv


# logging.set_verbosity_error()
load_dotenv("../config.env")
logging.info("test !!!!!!!!!!!!!!!!!!!!!!!!!!!")
RELATIONS_MODEL_NAME = getenv("RELATIONS_MODEL_NAME")

API_URL = "https://api-inference.huggingface.co/models/smetan/comet-bart-aaai"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


special_tokens = [
    "AtLocation",
    "CapableOf",
    "Causes",
    "CausesDesire",
    "CreatedBy",
    "DefinedAs",
    "DesireOf",
    "Desires",
    "HasA",
    "HasFirstSubevent",
    "HasLastSubevent",
    "HasPainCharacter",
    "HasPainIntensity",
    "HasPrerequisite",
    "HasProperty",
    "HasSubEvent",
    "HasSubevent",
    "HinderedBy",
    "InheritsFrom",
    "InstanceOf",
    "IsA",
    "LocatedNear",
    "LocationOfAction",
    "MadeOf",
    "MadeUpOf",
    "MotivatedByGoal",
    "NotCapableOf",
    "NotDesires",
    "NotHasA",
    "NotHasProperty",
    "NotIsA",
    "NotMadeOf",
    "ObjectUse",
    "PartOf",
    "ReceivesAction",
    "RelatedTo",
    "SymbolOf",
    "UsedFor",
    "isAfter",
    "isBefore",
    "isFilledBy",
    "oEffect",
    "oReact",
    "oWant",
    "xAttr",
    "xEffect",
    "xIntent",
    "xNeed",
    "xReact",
    "xReason",
    "xWant",
]


prompt1 = "The answer to the universe is"

t = []
for i in special_tokens:
    t.append(f"[{i}] {prompt1}")

prompt = t

def test1(prompt):
    for i in prompt:
        output = query({
            "inputs": i,
            "parameters": {
                "num_return_sequences": 3,
                "num_beams": 3
            }
        })
        print(output)


def test2(prompt):
    model = AutoModelForSeq2SeqLM.from_pretrained(RELATIONS_MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(RELATIONS_MODEL_NAME)
    print("------------------")
    for i in prompt:
        tokens = tokenizer(
            i,
            return_tensors="pt",
            truncation=True,
            max_length=100
        )
        generated_output = model.generate(
            **tokens,
            num_beams=3,
            num_return_sequences=3,
            max_length=100
        )
        # print(tokenizer.decode(generated_output, skip_special_tokens=True))
        items = [tokenizer.decode(i, skip_special_tokens=True) for i in generated_output]
        print(items)


# test1(prompt)
test2(prompt)