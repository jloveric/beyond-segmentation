import os
os.chdir("ultralytics")

from pathlib import Path
from ultralytics.models.yolo import YOLO

model_dir = "train"
in_dir = "../../data/yolo/test/images"

model = YOLO(f"runs/detect/{model_dir}/weights/best.pt")

images = [filename for filename in os.listdir(in_dir)]
results = model.predict([in_dir + "/" + filename for filename in images])

out_dir = f"runs/detect/infer_{model_dir}"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
for i in range(len(results)):
    results[i].save(filename=out_dir + "/" + os.path.splitext(images[i])[0] + "_labels.jpg", line_width=1, font_size=3)
    results[i].save(filename=out_dir + "/" + images[i], labels=False, conf=False)
    results[i].save_txt(txt_file=out_dir + "/" + os.path.splitext(images[i])[0] + ".txt", save_conf=True)
