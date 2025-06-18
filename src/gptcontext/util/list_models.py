import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def list_my_models():
    resp = openai.models.list()  # returns a SyncPage[Model]
    for m in resp.data:  # .data is a list of Model objects
        print(m.id)


if __name__ == "__main__":
    if not openai.api_key:
        print("ERROR: OPENAI_API_KEY not set")
    else:
        list_my_models()
