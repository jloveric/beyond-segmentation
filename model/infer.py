import os
from pathlib import Path
from ultralytics.models.yolo import YOLO

training_dir = "train"

model = YOLO(f"runs/detect/{training_dir}/weights/best.pt")

indir = "../../data/yolo/test/images"
images = [filename for filename in os.listdir(indir)]
results = model.predict([indir + "/" + filename for filename in images])

outdir = f"runs/detect/infer_{training_dir}"
if not os.path.exists(outdir):
    os.makedirs(outdir)
for i in range(len(results)):
    results[i].save(filename=outdir + "/" + os.path.splitext(images[i])[0] + "_labels.jpg", line_width=1, font_size=3)
    results[i].save(filename=outdir + "/" + images[i], labels=False, conf=False)
    results[i].save_txt(txt_file=outdir + "/" + os.path.splitext(images[i])[0] + ".txt", save_conf=True)
