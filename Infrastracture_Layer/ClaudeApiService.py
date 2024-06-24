from ILLMApiService import ILLMApiService
import anthropic

class ClaudeApiService(ILLMApiService):
    def SendRequest(self):
        

        client = anthropic.Client(api_key="")

        response = client.messages.create(
            model="claude-2.1",
            system="Respond only in Spanish.", # <-- system prompt
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Hello, world"}
            ]
        )

        print(response)