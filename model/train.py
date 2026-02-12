import os
import sys
import config
import shutil

ultralytics_path = os.path.abspath(os.path.join(os.getcwd(), "ultralytics"))
sys.path.insert(0, ultralytics_path)
shutil.copyfile(f"ultralytics/ultralytics/utils/loss_{config.model}.py", "ultralytics/ultralytics/utils/loss.py")
shutil.copyfile("config.py", "ultralytics/ultralytics/utils/config.py")

from ultralytics.models.yolo import YOLO

model = YOLO("yolov8s.pt")

model.train(data="data.yaml", epochs=config.epochs, imgsz=640, mosaic=0.0, patience=0, workers=8, project="runs", name="train")
