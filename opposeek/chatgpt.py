import os
import openai
import tiktoken

openai.api_key = os.environ.get("OPENAI_API_KEY")


def send(
    prompt=None,
    text_data=None,
    chat_model="gpt-3.5-turbo",
    model_token_limit=4097,
    max_msg_tokens=2500,
):
    if not prompt:
        return "Error: Prompt is missing. Please provide a prompt."

    encoding = tiktoken.encoding_for_model(chat_model)
    if text_data:
        token_integers = encoding.encode(text_data)

        content_chunks = [
            token_integers[i : i + max_msg_tokens]
            for i in range(0, len(token_integers), max_msg_tokens)
        ]

        content_chunks = [
            encoding.decode(content_chunk) for content_chunk in content_chunks
        ]
    else:
        content_chunks = []

    messages = [{"role": "user", "content": prompt}]

    for content_chunk in content_chunks:
        messages.insert(0, {"role": "user", "content": content_chunk})

    while (
        sum(len(encoding.encode(msg["content"])) for msg in messages)
        > model_token_limit
    ):
        messages.pop(0)

    response = openai.ChatCompletion.create(model=chat_model, messages=messages)
    response = response.choices[0].message["content"].strip()

    return response
