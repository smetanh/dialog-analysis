from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from dotenv import load_dotenv
import deepl
import logging

from os import getenv

# logging.set_verbosity_error()


load_dotenv("../config.env")
RELATIONS_MODEL_NAME = getenv("RELATIONS_MODEL_NAME")
DEEPL_TOKEN = getenv("DEEPL_TOKEN")

translator = deepl.Translator(DEEPL_TOKEN)

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


def load_model(model_name=RELATIONS_MODEL_NAME):
    return AutoModelForSeq2SeqLM.from_pretrained(model_name)


def load_tokenizer(model_name=RELATIONS_MODEL_NAME):
    return AutoTokenizer.from_pretrained(model_name)


def translate(text: str, target_language: str) -> str:
    if target_language.lower() == "en":
        target_language = "en-us"
    result = translator.translate_text(text, target_lang=target_language).text
    return result


def translate0(text: str, source_language: str = "ru_RU", target_language: str = "en_XX") -> str:

    import requests

    API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": text,
        "parameters": {"src_lang": source_language, "tgt_lang": target_language}
    })

    # print(output)

    return output[0]["translation_text"]


def run_model(model, tokenizer, prompt_en: str, source_language: str, num_generations: int = 3) -> str:
    # prompt_en = translate(prompt, "en")
    # prompt_en = prompt
    # logging.info(prompt_en)
    output = []
    t = [
        "AtLocation",
        "oEffect",
        "oReact",
        "oWant",
        "xAttr",
        "xEffect",
        "xIntent",
        "xNeed",
        "xReact",
        "xReason",
        "xWant"
    ]

    special_tokens2 = t
    for relation in special_tokens2:
        prompt_en_relation = f"{prompt_en} [{relation}]"

        tokens = tokenizer(
            prompt_en_relation,
            return_tensors="pt",
            truncation=True,
            max_length=4096
        )
        generated_output = model.generate(
            **tokens,
            num_beams=num_generations,
            num_return_sequences=num_generations,
            max_length=4096
        )

        items = [tokenizer.decode(i, skip_special_tokens=True).lstrip().replace(".", "") for i in generated_output]
        try:
            items.remove("none")
        except ValueError:
            pass
        output.append(
            f"[{relation}]: " + ", ".join(items) + "."
        )

    output = "\n".join(output)
    logging.info("OUTPUT: " + output)
    if source_language != "en":
        t = translate(output, source_language)
        logging.info("TRANSLATE: " + t)
        return t

    return output
