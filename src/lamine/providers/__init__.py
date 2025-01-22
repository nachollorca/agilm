from abc import ABC, abstractmethod
from typing import Optional

from ..datatypes import Answer, Message, _Model


class Provider(ABC):
    """
    Abstract class defining the shared interface for API providers.

    Attributes:
        model_ids (Optional[list[str]]): a list of valid model ids supported by the provider, e.g. "gemini-2-flash".
        locations (Optional[list[str]]): a list of valid locations where the provider is hosts LMs, e.g. "eu-central1".
            This generally applies only to provideders Vertex, Bedrock and Azure.
        env_vars (Optional[list[str]]): a list of environmental variables (API Keys) that should exist to query the provider.
    """

    model_ids: Optional[list[str]] = None
    locations: Optional[list[str]] = None
    env_vars: Optional[list[str]] = None

    def __init__(self):
        self.model_ids = [] if not self.model_ids else self.model_ids
        self.locations = [] if not self.locations else self.locations
        self.env_vars = [] if not self.env_vars else self.env_vars

    @abstractmethod
    def get_answer(self, model: _Model, conversation: list[Message], **kwargs) -> Answer:
        """
        Requests a response from a language model API for a single conversation.

        Args:
            model (Model): The language model to use for generating the response.
            conversation (list[Message]): A list of messages representing the conversation history.
            **kwargs: Additional keyword arguments like `temperature` or `top_p`.

        Returns:
            Answer: The response generated by the language model.
        """
        ...
