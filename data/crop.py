import copy
import os
from PIL import Image
import xml.etree.ElementTree as ET

def crop(in_dir, out_dir, idx, dataset):
    tree = ET.parse(f"{in_dir}/cmp_{dataset}{idx:0{4}d}.xml")
    root = tree.getroot()

    image = Image.open(f"{in_dir}/cmp_{dataset}{idx:0{4}d}.jpg")
    mask = Image.open(f"{in_dir}/cmp_{dataset}{idx:0{4}d}.png")

    facade_idx = 0
    for obj_facade in root.findall("object"):
        label = obj_facade.find("labelname").text.strip('\n')
        if label == "facade":
            points_facade = obj_facade.find("points")
            
            x1_facade, x2_facade = (float(x.text.strip()) for x in points_facade.findall("y"))
            y1_facade, y2_facade = (float(y.text.strip()) for y in points_facade.findall("x"))
            
            width, height = image.size
            left = int(x1_facade * width)
            top = int(y1_facade * height)
            right = int(x2_facade * width)
            bottom = int(y2_facade * height)
            
            cropped_image = image.crop((left, top, right, bottom))
            cropped_mask = mask.crop((left, top, right, bottom))
            
            cropped_image.save(f"{out_dir}/cmp_{dataset}{idx:0{4}d}_{facade_idx}.jpg")
            cropped_mask.save(f"{out_dir}/cmp_{dataset}{idx:0{4}d}_{facade_idx}.png")

            rescaled_objects = []
            for obj in root.findall("object"):
                obj_copy = copy.deepcopy(obj)
                points = obj_copy.find('points')
                x1, x2 = (float(x.text.strip()) for x in points.findall("y"))
                y1, y2 = (float(y.text.strip()) for y in points.findall("x"))

                x1_new, x2_new = ((x - x1_facade) / (x2_facade - x1_facade) for x in (x1, x2))
                y1_new, y2_new = ((y - y1_facade) / (y2_facade - y1_facade) for y in (y1, y2))

                eps = 1e-6
                if x2_new < -eps or x1_new > 1 + eps or y2_new < -eps or y1_new > 1 + eps:
                    continue
                coors = [x1_new, x2_new, y1_new, y2_new]
                for i in range(len(coors)):
                    coors[i] = max(0, min(1, coors[i]))
                x1_new, x2_new, y1_new, y2_new = coors

                points.clear()
                for x in (x1_new, x2_new):
                    ET.SubElement(points, "y").text = str(x)
                for y in (y1_new, y2_new):
                    ET.SubElement(points, "x").text = str(y)
                rescaled_objects.append(obj_copy)

            out_root = ET.Element("root")
            for obj in rescaled_objects:
                out_root.append(obj)
            out_tree = ET.ElementTree(out_root)
            out_tree.write(f"{out_dir}/cmp_{dataset}{idx:0{4}d}_{facade_idx}.xml")

            facade_idx += 1

if __name__ == "__main__":
    if not os.path.exists("b_crop"):
        os.mkdir("b_crop")
    for i in range(1, 379):
        crop("b", "b_crop", i, "b")
    
    if not os.path.exists("x_crop"):
        os.mkdir("x_crop")
    for i in range(1, 229):
        crop("x", "x_crop", i, "x")
