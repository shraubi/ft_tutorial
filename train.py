import openai
import logging
import time
import sqlalchemy

from openai.error import RateLimitError, InvalidRequestError

from db import create_table, get_engine, get_session, samples, Base

logging.basicConfig(level=logging.INFO)

openai.api_key = "API_KEY"

engine = get_engine()
create_table(engine)
session = get_session(engine)
query = session.query(samples.text, samples.prompt, samples.answers).all()


def answer(row):
    prompt = f"Write a text, using the topic and context.\nContext: {row.text}.\nTopic: {row.prompt}\nText:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=350,
        frequency_penalty=0.5,
        presence_penalty=0,
        best_of=3,
        stop=["\n\n", "END"],
    )

    sample = session.query(samples).filter(samples.text == row.text)
    sample.update({"answers": response["choices"][0]["text"]})
    session.commit()


def main():
    for row in query:
        if row.answers:
            continue
        else:
            try:
                answer(row)
            except RateLimitError:
                time.sleep(30)
                answer(row)
            except InvalidRequestError:
                continue


main()
