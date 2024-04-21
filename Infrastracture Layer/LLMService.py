import openai

class OpenAIChatService:
    def __init__(self):
        """
        Constructor that does minimal work. Actual initialization is deferred to the `initialize` method.
        """
        self.api_key = None
        self.model = None

    def initialize(self, api_key, model="gpt-3.5-turbo"):
        """
        Fully initializes the instance with an API key and model.
        :param api_key: API key for authenticating with the OpenAI service.
        :param model: The model to use for generating text completions.
        """
        openai.api_key = api_key
        self.api_key = api_key
        self.model = model

    def chat_completion(self, messages):
        """
        Sends a chat completion request to OpenAI's API and returns the response.
        Make sure to call `initialize` before using this method.
        :param messages: A list of message dictionaries for the chat. Each message should be
                         a dict with "role" (either "user" or "system") and "content".
        :return: Response from the OpenAI API.
        """
        if not self.api_key or not self.model:
            raise ValueError("The service has not been initialized. Please call 'initialize' first.")

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message['content'] if response.choices else None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    chat_service = OpenAIChatService()
    
    # Explicitly initialize the service before using it
    chat_service.initialize("your_openai_api_key_here")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    
    response = chat_service.chat_completion(messages)
    print(response)