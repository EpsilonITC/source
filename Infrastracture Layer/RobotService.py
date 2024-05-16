import json
import os
import numpy as np
import torch
from ultralytics import YOLO
from PIL import Image
from grasp_generator import GraspGenerator
from environment.utilities import Camera
from environment.env import Environment
from utils import YcbObjects
import pybullet as p
import argparse
import sys
from LLMManager import LLMManager

sys.path.append('network')

class RobotService:

    class_names = [
    '003_cracker_box', '004_sugar_box', '005_tomato_soup_can', '006_mustard_bottle', '007_tuna_fish_can', 
    '008_pudding_box', '009_gelatin_box', '010_potted_meat_can', '011_banana', '019_pitcher_base', 
    '021_bleach_cleanser', '024_bowl', '025_mug', '035_power_drill', '036_wood_block', 
    '037_scissors', '040_large_marker', '051_large_clamp', '052_extra_large_clamp', '061_foam_brick'
    ]
    def __init__(self):
        self.args = self.parse_args()
        #self.Configure()

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Grasping demo')
        parser.add_argument('--scenario', type=str, default='pack', help='Grasping scenario (pack)')
        parser.add_argument('--runs', type=int, default=1, help='Number of runs the scenario is executed')
        parser.add_argument('--show-network-output', dest='output', type=bool, default=False, help='Show network output (True/False)')
        return parser.parse_args()

    def load_yolo_model(self, weights_file):
        model = YOLO(weights_file)
        return model

    def Configure(self, vis, debug):
        self.objects = YcbObjects('objects/ycb_objects', mod_orn=['ChipsCan', 'MustardBottle', 'TomatoSoupCan'], mod_stiffness=['Strawberry'])
        center_x, center_y = 0.05, -0.52
        self.network_path = 'network/trained-models/cornell-randsplit-rgbd-grconvnet3-drop1-ch32/epoch_19_iou_0.98'
        self.camera = Camera((center_x, center_y, 1.9), (center_x, center_y, 0.785), 0.2, 2.0, (224, 224), 40)
        self.env = Environment(self.camera, vis=vis, debug=debug, finger_length=0.06)
        self.generator = GraspGenerator(self.network_path, self.camera, 5)
        self.yolo_model = self.load_yolo_model("yolo5.pt")

        # def parse_args():
        # parser = argparse.ArgumentParser(description='Grasping demo')
        # parser.add_argument('--scenario', type=str, default='pack', help='Grasping scenario (pack)')
        # parser.add_argument('--runs', type=int, default=1, help='Number of runs the scenario is executed')
        # parser.add_argument('--show-network-output', dest='output', type=bool, default=False, help='Show network output (True/False)')
        # args = parser.parse_args()
        # return args

        # def load_yolo_model(weights_file):
        # # Load YOLOv8 model with specified weights
        # model = YOLO(weights_file)
        # return model

        # List of class names in order
        # class_names = [
        # '003_cracker_box', '004_sugar_box', '005_tomato_soup_can', '006_mustard_bottle', '007_tuna_fish_can', 
        # '008_pudding_box', '009_gelatin_box', '010_potted_meat_can', '011_banana', '019_pitcher_base', 
        # '021_bleach_cleanser', '024_bowl', '025_mug', '035_power_drill', '036_wood_block', 
        # '037_scissors', '040_large_marker', '051_large_clamp', '052_extra_large_clamp', '061_foam_brick'
        # ]

    def grasp(self, n, vis, output):

        for i in range(n):
            print(f'Trial {i}')
            #self.objects.shuffle_objects()
            info = self.objects.get_n_first_obj_info(5)
            object_names = self.class_names[0:5]   #self.objects.get_n_first_obj_names(5)
            self.env.create_packed(info)

            while len(self.env.obj_ids) != 0:
                self.env.move_away_arm()
                self.env.reset_all_obj()

                rgb, depth, _ = self.camera.get_cam_img()

                # Detect objects with YOLO
                #yolo_results = yolo_model.predict(rgb)
                #boxes = yolo_results[0].boxes.data  # Bounding box information

                # Generate grasps
                grasps, save_name = self.generator.predict_grasp(rgb, depth, n_grasps=3, show_output=output)
                #obj = input('Enter the object u would like to pick up: ')
                prompt = input("How can I help you?")
                response = LLMManager().process_input(prompt, object_names)
                print(response)
                grasping = json.loads(response)['commands']
                print(grasping)

                for item in grasping:
                    if item['command'] == "GRASP_OBJECT":
                        for i, grasp in enumerate(grasps):
                            #rgb, depth, _ = camera.get_cam_img()
                            yolo_results = self.yolo_model.predict(rgb)
                            boxes = yolo_results[0].boxes.data  # Bounding box information
                            x, y, z, roll, opening_len, obj_height = grasp

                            # Find the closest bounding box center
                            min_distance = float('inf')
                            closest_box = None
                            for box in boxes:
                                box_x_center = float((box[0] + box[2]) / 2)
                                box_y_center = float((box[1] + box[3]) / 2)
                                box_x_center, box_y_center = self.generator.bb_to_robot_frame((box_x_center, box_y_center))
                                distance = np.linalg.norm([x - box_x_center, y - box_y_center])

                                if (distance < min_distance):
                                    min_distance = distance
                                    closest_box = box
                                print(min_distance, int(closest_box[5]))
                            if closest_box is not None:
                                class_id = int(closest_box[5])  # Convert class ID to int
                                confidence = closest_box[4]

                                # Map class ID to class name
                                class_name = self.class_names[class_id]
                                #print(f"Grasping object '{class_name}' with Confidence: {confidence:.2f}")
                            if class_name == "011_banana":
                                if vis:
                                    debug_id = p.addUserDebugLine([x, y, z], [x, y, 1.2], [0, 0, 1], lineWidth=3)

                                success_grasp, success_target = self.env.grasp((x, y, z), roll, opening_len, obj_height)

                                if vis:
                                    p.removeUserDebugItem(debug_id)

                                if success_target:
                                    if save_name is not None:
                                        os.rename(save_name + f'_SUCCESS_grasp{i}.png')
                                    break
                                else:
                                    print(f"Failed to grasp at ({x}, {y}, {z}). Trying again...")

                self.env.reset_all_obj()

            self.env.remove_all_obj()

def main():
    robotService = RobotService()
    args = robotService.parse_args()
    output = args.output
    runs = args.runs
    robotService.Configure(vis=True, debug=False)
    robotService.grasp(runs, vis=True, output=output)

if __name__ == '__main__':
    main()
