import sys
import os

folder_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(folder_path)
from infrastructure.RobotService import main

main()