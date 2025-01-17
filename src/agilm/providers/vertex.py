import random

import vertexai
from vertexai.generative_models import Content, GenerativeModel, Part

from ..types import Answer, Message, Model


def get_answer(model: Model, conversation: list[Message], **kwargs) -> Answer:
    contents = [
        Content(role=message.role, parts=[Part.from_text(message.content)])
        for message in conversation
    ]
    if model.locations:
        vertexai.init(location=random.choice(model.locations))
    client = GenerativeModel(model.id)
    response = client.generate_content(contents=contents)
    return response