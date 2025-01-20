import random

import vertexai as vertexai_source
from vertexai.generative_models import Content, GenerativeModel, Part

from ..types import Answer, Message, Model, Provider


class Vertex(Provider):
    model_ids = ["gemini-1.5-flash-002", "gemini-1.5-pro-002", "gemini-2.0-flash"]
    locations = [
        "europe-west6",
        "europe-west2",
        "europe-west8",
        "europe-north1",
        "europe-central2",
        "australia-southeast1",
        "us-west4",
        "us-east5",
        "asia-south1",
        "us-west3",
        "europe-west9",
        "me-central2",
        "us-west1",
        "asia-northeast3",
        "africa-south1",
        "me-west1",
        "asia-northeast1",
        "europe-west3",
        "europe-west12",
        "asia-southeast1",
        "us-east1",
        "asia-southeast2",
        "europe-west1",
        "us-west2",
        "me-central1",
        "northamerica-northeast1",
        "europe-west4",
        "southamerica-west1",
        "us-east4",
        "southamerica-east1",
        "northamerica-northeast2",
        "europe-southwest1",
        "us-south1",
        "asia-northeast2",
        "australia-southeast2",
        "asia-east1",
        "us-central1",
        "asia-east2",
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
