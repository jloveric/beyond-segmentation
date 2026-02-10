import os
os.chdir("ultralytics")

from pathlib import Path
from ultralytics.models.yolo import YOLO

training_dir = "train"

model = YOLO(f"runs/detect/{training_dir}/weights/best.pt")

metrics = model.val(data="data.yaml", split="test")

with open(f"runs/detect/test.txt", "w") as f:
    print(metrics, file=f)
