# application/containers.py
from dependency_injector import containers, providers
from simulation_service import SimulationService
from llm_manager import LLMManager
from yolo_service import YOLOService
from llm_service import OpenAIChatService
from tts_service import OpenAITTSService
class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    yolo_service = providers.Singleton(YOLOService)
    simulation_service = providers.Singleton(SimulationService)
    llm_manager = providers.Singleton(LLMManager)
    llm_service = providers.Singleton(OpenAIChatService)
    
    robot_service = providers.Factory(
        yolo_service=yolo_service,
        llm_manager=llm_manager,
        simulation_service = simulation_service,
        llm_service=llm_service
    )
