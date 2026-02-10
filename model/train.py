import os
os.chdir("ultralytics")

from ultralytics.models.yolo import YOLO

epochs = 200

model = YOLO("yolov8s.pt")

model.train(data="../data.yaml", epochs=epochs, imgsz=640, mosaic=0.0, patience=0, workers=8)
