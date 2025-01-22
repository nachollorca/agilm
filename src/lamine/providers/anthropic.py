from anthropic import Anthropic as Anthropic_source

from ..datatypes import Answer, Message, _Model
from . import Provider


class Anthropic(Provider):
    model_ids = ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-haiku-20240307"]
    env_vars = ["ANTHROPIC_API_KEY"]

    def get_answer(self, model: _Model, conversation: list[Message], **kwargs) -> Answer:
        client = Anthropic_source()
        messages = [message.to_dict for message in conversation]
        response = client.messages.create(model=model.id, messages=messages, max_tokens=4096, **kwargs)  # type: ignore
        return Answer(
            content=response.content[0].text,  # type: ignore
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
            source=response,
        )
