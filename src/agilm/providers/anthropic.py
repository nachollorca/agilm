from anthropic import Anthropic
from ..types import Answer, Message, Model, Provider

class AnthropicProvider(Provider):
    def get_answer(self, model: Model, conversation: list[Message], **kwargs) -> Answer:
        client = Anthropic()
        messages = [message.dict for message in conversation]
        response = client.messages.create(
            model=model.id, messages=messages, max_tokens=4096, **kwargs
        )
        return Answer(
            content=response.content[0].text,
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
        )