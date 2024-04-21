from ultralytics import YOLO
import os

model_path = "/Users/dawid/Documents/Coding/Visual Studio/Robotic_Arm/source/Infrastracture Layer/runs/detect/train8/weights/best.pt"
model = YOLO(model_path)


#model = YOLO('yolov8x.pt')  # initialize model
results = model('/Users/dawid/Desktop/yolo_training/image25.jpg')  # perform inference
results[0].show()  # display results for the first image



# Load a model
#model = YOLO("yolov8m.yaml")  # build a new model from scratch

# Use the model
#results = model.train(data="/Users/dawid/Documents/Coding/Visual Studio/Robotic_Arm/source/Application Layer/config.yaml", epochs=150)  # train the model



#training 1-6 do not give good results
#training 7 trained with model S gives promising results with 150 epochs
#traing 8 trained with model M