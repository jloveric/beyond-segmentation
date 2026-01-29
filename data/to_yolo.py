from dataclasses import dataclass
import os
import re
import xml.etree.ElementTree as ET

@dataclass
class Rectangle:
    label: str
    xs: list[int]
    ys: list[int]

def to_yolo(in_path, out_path):
    with open(in_path) as f:
        xml = f.read()
    tree = ET.fromstring(xml)

    rectangles = []

    for object in tree:
        xs = []
        for y in object.iter("y"):
            xs.append(float(y.text.replace('\n', '')))
        ys = []
        for x in object.iter("x"):
            ys.append(float(x.text.replace('\n', '')))
        for l in object.iter("label"):
            label = int(l.text.replace('\n', '')) - 3
        if label >= 0:
            rectangles.append(Rectangle(str(label), xs, ys))

    with open(out_path, "a") as f:
        for rectangle in rectangles:
            f.write(f"{rectangle.label} {(rectangle.xs[0] + rectangle.xs[1]) / 2} {(rectangle.ys[0] + rectangle.ys[1]) / 2} {abs(rectangle.xs[0] - rectangle.xs[1])} {abs(rectangle.ys[0] - rectangle.ys[1])}\n")

if __name__ == "__main__":
    for dataset, n in zip(["b", "x"], [378, 228]):
        for i in range(1, n + 1):
            filename_base = f"cmp_{dataset}{i:0{4}d}"
            for filename in os.listdir(f"{dataset}_crop"):
                if re.match("^" + filename_base + r"_[0-9]+\.xml$", filename):
                    filename_txt = re.sub("xml$", "txt", filename)
                    to_yolo(f"{dataset}_crop/{filename}", f"{dataset}_crop/{filename_txt}")
