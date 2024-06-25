# presentation/main.py
import sys
import os

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from containers import Container

def main():
    container = Container()

    simulation_service = container.simulation_service()
    
    #robot_service.grasp()

if __name__ == "__main__":
    main()
