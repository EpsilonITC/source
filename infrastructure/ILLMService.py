from abc import ABC, abstractmethod

class ILLMService(ABC):
    @abstractmethod
    def initialize(self, api_key, model="gpt-3.5-turbo"):
        """
        Initializes the instance with an API key and model.
        :param api_key: API key for authenticating with the service.
        :param model: The model to use for generating text completions.
        """
        pass

    @abstractmethod
    def chat_completion(self, messages):
        """
        Sends a chat completion request to the API and returns the response.
        Make sure to call `initialize` before using this method.
        :param messages: A list of message dictionaries for the chat. Each message should be
                         a dict with "role" (either "user" or "system") and "content".
        :return: Response from the API.
        """
        pass
