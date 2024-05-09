from abc import abstractmethod

class ILLMApiService:

    def __init__(self):
        pass
    
    @abstractmethod
    def SendRequest(self):
        pass