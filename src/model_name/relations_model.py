from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from googletrans import Translator
import deepl
from dotenv import load_dotenv
import textwrap

import logging

from os import getenv

# logging.set_verbosity_error()


load_dotenv("../config.env")
RELATIONS_MODEL_NAME = getenv("RELATIONS_MODEL_NAME")
SUMMARIZATION_MODEL_NAME = getenv("SUMMARIZATION_MODEL_NAME")

translator = Translator()

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


def translate(text: str) -> str:
    language = translator.detect(text).lang
    # if language != "en":
    #     text = translator.translate(text, dest='en').text
    return language


def translate_2(text: str, src_lang: str) -> str:
    translator_2 = deepl.translate(source_language=src_lang, target_language="EN", text=text)
    return translator_2


# for token in special_tokens:
#     if token not in tokenizer.vocab:
#         tokenizer.add_tokens(token)

# num_special_tokens = len(special_tokens)
# special_token_ids = list(range(tokenizer.vocab_size, tokenizer.vocab_size + num_special_tokens))
# special_token_vectors = model.embeddings.word_embeddings(special_token_ids)
# model.embeddings.word_embeddings.weight.data[special_token_ids] = special_token_vectors

# tokenizer.add_tokens(special_tokens)
# model.resize_token_embeddings(len(tokenizer))


def run_model(model, tokenizer, prompt: str, num_generations: int = 3) -> str:
    # prompt_en, language = translate(prompt)
    # language = translate(prompt)
    # prompt_en = translate_2(prompt, language)
    prompt_en = prompt
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

    # if language != "en":
        # output_local = [translator.translate(i, dest=language).text for i in output]
        # output_local = [translate_2(i) for i in output]
        # output_local = "\n".join(output_local)
        # output_wrap = textwrap.wrap(output, 3999)
        # output_local = ""
        # for wrap in output_wrap:
        #     output_local += translate_2(wrap, language)

        # output_local = translate_2(output, language)
        # logging.info(output_local)
        # return output_local

    return output
