import openai

class OpenAITTSService:
    def __init__(self):
        """
        Constructor with minimal setup. Use `initialize` to set up the service.
        """
        self.api_key = None
        self.voice = None

    def initialize(self, api_key, voice="default_voice"):
        """
        Initializes the service with an API key and a voice.
        :param api_key: API key for authenticating with the OpenAI service.
        :param voice: The voice to use for text-to-speech generation.
        """
        openai.api_key = api_key
        self.api_key = api_key
        self.voice = voice

    def text_to_speech(self, text):
        """
        Converts text to speech using the configured voice.
        Ensure `initialize` has been called before using this method.
        :param text: The text to convert to speech.
        :return: Speech data as bytes, or None if an error occurs.
        """
        if not self.api_key or not self.voice:
            raise ValueError("The service has not been initialized. Please call 'initialize' first.")

        try:
            # Assuming OpenAI provides a text-to-speech API endpoint and method
            # This is a placeholder for the actual API call, which would look something like this:
            response = openai.TextToSpeech.create(
                voice=self.voice,
                text=text
            )
            # Assuming the API returns the speech data directly
            return response.audio  # This would be the audio data in bytes
        except Exception as e:
            print(f"Request failed: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    tts_service = OpenAITTSService()
    
    # Explicitly initialize the service before using it
    tts_service.initialize("your_openai_api_key_here", "voice_of_choice")

    text = "Hello, world! This is an example of text-to-speech conversion."
    
    # Get speech from text
    speech_data = tts_service.text_to_speech(text)
    
    if speech_data:
        # Assuming the speech data is in bytes, save it to a file
        with open("output.mp3", "wb") as audio_file:
            audio_file.write(speech_data)
        print("Speech conversion completed and saved to output.mp3.")
    else:
        print("Failed to convert text to speech.")
