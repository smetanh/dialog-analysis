import logging
from os import getenv

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from dotenv import load_dotenv


# logging.set_verbosity_error()
load_dotenv("../config.env")
RELATIONS_MODEL_NAME = getenv("RELATIONS_MODEL_NAME")

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

special_tokens_test = [
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


def load_model(model_name=RELATIONS_MODEL_NAME):
    return AutoModelForSeq2SeqLM.from_pretrained(model_name)


def load_tokenizer(model_name=RELATIONS_MODEL_NAME):
    return AutoTokenizer.from_pretrained(model_name)


class Relations:
    def __init__(self, model, tokenizer, prompt):
        self.model = model
        self.tokenizer = tokenizer
        self.prompt = prompt

        self.num_generations = 3
        self.prefixes = special_tokens
        self.output = [[] for _ in range(len(self.prefixes))]
        self.iterator = 0

    def get_relations(self) -> list:
        for relation in self.prefixes:
            for prompt_i in self.prompt:
                prompt_relation = f"{prompt_i} [{relation}]"

                tokens = self.tokenizer(
                    prompt_relation,
                    return_tensors="pt",
                    truncation=True,
                    max_length=4096
                )
                generated_output = self.model.generate(
                    **tokens,
                    num_beams=self.num_generations,
                    num_return_sequences=self.num_generations,
                    max_length=4096
                )

                items = list(
                    set(
                        self.tokenizer.decode(
                            i, skip_special_tokens=True
                        ).lstrip().replace(".", "") for i in generated_output
                    )
                )
                for item in items:
                    self.output[self.iterator].append(item)
            self.output_post_processing()
            self.iterator += 1
        return self.output

    def output_post_processing(self):
        counter = {}
        for item in self.output[self.iterator]:
            if item not in counter:
                counter[item] = 0
            counter[item] += 1

        sorted_counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

        top_k = 3
        top_items = []
        top_percents = 0

        for k, v in sorted_counter.items():
            if top_k > 0:
                top_items.append(f"{int(100 * v / len(self.output[self.iterator]))}% {k}")
                top_percents += int(100 * v / len(self.output[self.iterator]))
                top_k -= 1

        top_items.append(f"{100 - top_percents}% другие")

        self.output[self.iterator] = f"[{self.prefixes[self.iterator]}]: " + ", ".join(top_items)

        # self.remove_duplicates()
        # empty_rows_indices = self.get_empty_rows_indices()

        # self.output = self.remove_empty_rows(self.output, empty_rows_indices)

        # self.prefixes = self.remove_empty_rows(self.prefixes, empty_rows_indices)


    # def remove_duplicates(self):
    #     for i in range(len(self.output)):
    #         for j in range(len(self.output[i])):
    #             for k in range(len(self.output)):
    #                 for m in range(len(self.output[k]) - 1, -1, -1):
    #                     if i == 0 and j == 0 and self.output[k][m] == "none":
    #                         self.output[k].pop(m)
    #                     elif (k != i) and (self.output[i][j] == self.output[k][m]):
    #                         self.output[k].pop(m)
    #
    # @staticmethod
    # def remove_empty_rows(text: list, indices: set):
    #     for i in sorted(indices, reverse=True):
    #         del text[i]
    #     return text
    #
    # def get_empty_rows_indices(self) -> set:
    #     empty_indices = set()
    #     for i in range(len(self.output)):
    #         if len(self.output[i]) == 0:
    #             empty_indices.add(i)
    #     return empty_indices
    #
    # def get_prefixes(self) -> tuple | list:
    #     return self.prefixes
    #
    # def list_to_str(self):
    #     for i in range(len(self.output)):
    #         self.output[i] = ", ".join(self.output[i])
    #     self.output = "\n".join(self.output)
    #     self.output: str



