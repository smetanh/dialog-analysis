import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "Hello",
    "parameters": {"src_lang": "en_XX", "tgt_lang": "ru_RU"}
})

print(output)
