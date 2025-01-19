import random

import vertexai
from vertexai.generative_models import Content, GenerativeModel, Part

from ..types import Answer, Message, Model, Provider

class VertexProvider(Provider):
    locations = [
        "us-central1",
        "eu-central1",
    ]

    def get_answer(self, model: Model, conversation: list[Message], **kwargs) -> Answer:
        contents = [
            Content(role=message.role, parts=[Part.from_text(message.content)])
            for message in conversation
        ]
        if self.locations and model.locations:
            vertexai.init(location=random.choice(model.locations))
        client = GenerativeModel(model.id)
        response = client.generate_content(contents=contents)
        return Answer(
            content=response.text,  # Adjust according to actual response structure
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
        )