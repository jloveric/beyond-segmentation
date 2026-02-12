import os
import cv2
import numpy as np

baseline_dir = "train"
infer_dir = "train2"

def load_bboxes(file_path):
    bboxes = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            class_idx = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            bboxes.append({
                'class_idx': class_idx,
                'x': x_center,
                'y': y_center,
                'w': width,
                'h': height
            })
    return bboxes

def draw(input_dir, base_name, output_dir):
    bboxes = load_bboxes(input_dir + "/" + base_name + ".txt")

    orig_img = cv2.imread(input_dir + "/" + base_name + ".jpg")
    if orig_img is None:
        raise FileNotFoundError(f"Original image not found")
    height, width = orig_img.shape[:2]

    class_bboxes = {}
    for bbox in bboxes:
        cls = bbox['class_idx']
        class_bboxes.setdefault(cls, []).append(bbox)

    os.makedirs(output_dir, exist_ok=True)

    for cls_idx, boxes in class_bboxes.items():
        img = np.zeros((height, width, 3), dtype=np.uint8)

        for box in boxes:
            x_center = box['x']
            y_center = box['y']
            w_norm = box['w']
            h_norm = box['h']

            box_width = int(w_norm * width)
            box_height = int(h_norm * height)

            x1 = int((x_center - w_norm / 2) * width)
            y1 = int((y_center - h_norm / 2) * height)

            x1 = max(0, min(x1, width - 1))
            y1 = max(0, min(y1, height - 1))
            x2 = max(0, min(x1 + box_width, width))
            y2 = max(0, min(y1 + box_height, height))

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=-1)

        output_path = os.path.join(output_dir, f"{base_name}_{cls_idx}.png")
        cv2.imwrite(output_path, img)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    for filename in os.listdir("../../../CMP/yolo/test/images"):
        base_name, _ = os.path.splitext(filename)
        output_dir = 'bboxes'

        draw(f"../model/runs/{baseline_dir}", base_name, "baseline")
        draw(f"../model/runs/{infer_dir}", base_name, "inference")
