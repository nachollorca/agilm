import random

import vertexai as vertexai_source
from vertexai.generative_models import Content, GenerativeModel, Part

from ..datatypes import Answer, Message, Model
from . import Provider


class Vertex(Provider):
    model_ids = ["gemini-1.5-flash-002", "gemini-1.5-pro-002", "gemini-2.0-flash"]
    locations = [
        "europe-central2",
        "europe-north1",
        "europe-southwest1",
        "europe-west1",
        "europe-west12",
        "europe-west2",
        "europe-west3",
        "europe-west4",
        "europe-west6",
        "europe-west8",
        "europe-west9",
        "us-central1",
    ]
    env_vars = ["GOOGLE_APPLICATION_CREDENTIALS"]

    def get_answer(self, model: Model, conversation: list[Message], **kwargs) -> Answer:
        contents = [Content(role=message.role, parts=[Part.from_text(message.content)]) for message in conversation]
        if model.locations:
            location = random.choice(model.locations)
            vertexai_source.init(location=location)
            print(f"Querying 'vertex' server in location '{location}'")
        client = GenerativeModel(model.id)
        response = client.generate_content(contents=contents)
        return Answer(
            content=response.candidates[0].content.parts[0].text,
            tokens_in=response.usage_metadata.prompt_token_count,
            tokens_out=response.usage_metadata.candidates_token_count,
            source=response,
        )
