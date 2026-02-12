import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

cls = 0

max_components = 25
count = 0
S_1_all = np.zeros((max_components,))
S_2_all = np.zeros((max_components,))

for filename in os.listdir("../../../CMP/yolo/test/images"):
    base_name, _ = os.path.splitext(filename)
    path_base_1 = f"baseline/{base_name}_{cls}"
    path_base_2 = f"custom/{base_name}_{cls}"

    image_path_1 = path_base_1 + ".png"
    image_path_2 = path_base_2 + ".png"
    if not os.path.exists(image_path_1) or not os.path.exists(image_path_2):
        continue
    image_1 = Image.open(image_path_1)
    image_2 = Image.open(image_path_2)

    gray_image_1 = image_1.convert('L')
    gray_image_2 = image_2.convert('L')

    img_array_1 = np.array(gray_image_1)
    img_array_2 = np.array(gray_image_2)

    U_1, S_1, Vt_1 = np.linalg.svd(img_array_1, full_matrices=False)
    U_2, S_2, Vt_2 = np.linalg.svd(img_array_2, full_matrices=False)

    S_1_all += S_1[0:max_components]
    S_2_all += S_2[0:max_components]
    count += 1

S_1_all /= count
S_2_all /= count

plt.figure(figsize=(8, 6))
plt.plot(S_1_all, marker='o', label="baseline")
plt.plot(S_2_all, marker='o', label="custom")
plt.xlabel('Index of Singular Value')
plt.ylabel('Singular Value')
plt.legend(loc="upper right")
plt.grid(True)

plot_path = f"svd_{cls}.png"
plt.savefig(plot_path)
plt.close()
