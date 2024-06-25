from tts_service import OpenAITTSService
from llm_service import OpenAIChatService
from VoiceToTextService import OpenAIVoiceToTextService

import os
from dotenv import load_dotenv

class Task:
    def __init__(self, description):
        self.description = description

class CommandResponse:
    Command = None
    Parameters = []

class ResponseObject:
    def __init__(self, tasks, tts_response):
        self.tasks = tasks  # List of Task objects
        self.tts_response = tts_response  # TTS generated voice response as binary data

class LLMManager:
    def __init__(self, debug=True):

        self.debug = debug
        load_dotenv()
        api_key = os.getenv('API_KEY')
        #self.vtt_service =
        self.tts_service = OpenAITTSService()
        self.chat_service = OpenAIChatService()
        self.tts_service.initialize(api_key)
        self.chat_service.initialize(api_key)

    def Configure(self, debug=True):
        self.debug = debug
        load_dotenv()
        api_key = os.getenv('API_KEY')
        #self.vtt_service =
        self.tts_service = OpenAITTSService()
        self.chat_service = OpenAIChatService()
        self.vtt_service = OpenAIVoiceToTextService()

        self.tts_service.initialize(api_key)
        self.chat_service.initialize(api_key)
        self.vtt_service.initialize(api_key)
        print("initilized")

    def create_prompt(self, message, objects):

        example = f"""

                    {{
                        "commands" : 
                        [
                            {{
                                "command" : "COMMAND_NAME",
                                "parameters" : [PARAMETER0]
                            }},
                            {{
                                "command" : "COMMAND_NAME",
                                "parameters" : [PARAMETER0]
                            }}
                        ],
                        "text" : "Text to be said to the user"
                    }}
        """

        prompt = f"""<definition>The user gives a message describing what is happening in the operational environment.
                    You should analyze the situtaion and find solution to the problem that occurs.
                    You should use given predefined commands to preapre a list of them to accomplish actions to solve the problem defined before.
                    The predifened commands can be passed parameters that are defined in the list below.
                    You should use only provided items to find the correct solution.
                    Find the most stupid and funny solution. </definition>
                    <tasks>
                        LOCATE_OBJECT
                        GRASP_OBJECT(item_object)
                    </tasks>

                    <available_objects>
                    {objects}
                    </available_objects>
                    <output>
                    The output returned should be only a JSON object containing a list of CommandResponse objects 
                    (class CommandResponse:
                        Command = None
                        Parameters = []) and string containing text to be said to the user as a response.
                    </output>
                    Example:
                    <output_example>
                    {example}
                    </output_example>
                    <user_message>" {message} "</user_message>
                    <expected_output>
                    Return only the JSON object without any additional information, so the output can be parsed to JSON format
                    </expected_output>
                    """
        if self.debug:
            print(prompt)
        return prompt
        
    def process_input(self, message, objects):

        prompt = self.create_prompt(message, objects)
        messages = [
            {"role": "system", "content": "You are a funny assistant, that should be able to find solution to a given situation and provide the user withlist of commands to perform in case to solve that. You should return only JSON object"},
            {"role": "user", "content": prompt}
        ]
        chat_response = self.chat_service.chat_completion(messages)
        if self.debug:
            print(chat_response)
        if not chat_response:
            print("Failed to generate chat response.")
            return None
        return(chat_response)
        #self.tts_service.text_to_speech(chat_response['text'])

    def handle_voice_input(self, objects):
        response = self.vtt_service.capture_audio()
        return self.process_input(response, objects)

# Assuming you have instances of VTTService, TTSService, and ChatService initialized elsewhere:
# vtt_service = VTTService()
# tts_service = TTSService()
# chat_service = ChatService()

# Initialize LLMManager with these services
# llm_manager = LLMManager(vtt_service, tts_service, chat_service)

# Now, you can handle voice input like this:
# response_object = llm_manager.handle_voice_input(voice_data)
# if response_object:
#     # Process the tasks and play back the tts_response

if __name__ == '__main__':

    message = input()
    response = LLMManager().process_input(message, ["apple", "cola"])