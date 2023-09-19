import asyncio
import os
import random
import tempfile
from base64 import b64decode
from pathlib import Path

import openai
from telegram import Bot

_ANIMALS = [
    "prairie dog",
    "capybara",
    "wallaby",
    "koala",
    "quoka",
    "beaver",
    "marmot",
    "groundhog",
    "chipmunk",
    "dormouse",
    "pika mouse",
]

_PREDICATES = [
    "happy to see me",
    "obsessed with finding the right sleeping position",
    "dreaming of its favorite food",
    "content",
    "excited",
    "extremely relaxed",
    "chilling on a pillow",
    "sleeping on the back of a capybara",
    "being sniffed by a rabbit",
    "spooning its partner",
]


def _prompt_data():
    animal = random.choice(_ANIMALS)
    predicate = random.choice(_PREDICATES)
    return f"A photo of a {animal} who is {predicate}", animal, predicate


def _tmpdir():
    return Path(tempfile.gettempdir())


def _telegram_token():
    return os.getenv("TELEGRAM_TOKEN")


def _openai_api_key():
    return os.getenv("OPENAI_API_KEY")


def _user_ids():
    users = os.getenv("WHITELIST")
    user_ids = users.split(";")
    return [user_id for user_id in user_ids if len(user_id) > 0]


async def a_main():
    img_size = "512x512"

    prompt, animal, predicate = _prompt_data()

    openai.api_key = _openai_api_key()

    print(prompt)
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=img_size,
        response_format="b64_json",
    )

    first_response = response["data"][0]

    b64 = first_response["b64_json"]
    image_data = b64decode(b64)

    file_name = _tmpdir() / f"{animal}_{predicate}.png"

    with open(file_name, mode="wb") as filehandle:
        filehandle.write(image_data)

    bot = Bot(token=_telegram_token())
    async with bot:
        for user_id in _user_ids():
            await bot.send_photo(chat_id=user_id, photo=file_name)

    return 1


def main(request, context):
    return asyncio.run(a_main())


if __name__ == "__main__":
    main()
