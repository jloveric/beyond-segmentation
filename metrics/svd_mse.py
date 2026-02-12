import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

cls = 0

max_components = 25
count = 0
mse_cumulative_1 = np.zeros((max_components,))
mse_cumulative_2 = np.zeros((max_components,))

mse_sum_1 = 0
mse_sum_2 = 0

for filename in os.listdir("../data/yolo/test/images"):
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

    # For each number of components, reconstruct images and compute MSE
    for x in range(1, max_components + 1):
        # Reconstruct image from first x components
        S_1_x = np.diag(S_1[:x])
        S_2_x = np.diag(S_2[:x])

        # Reconstructed images
        reconstructed_1 = U_1[:, :x] @ S_1_x @ Vt_1[:x, :]
        reconstructed_2 = U_2[:, :x] @ S_2_x @ Vt_2[:x, :]

        # Compute MSE between original and reconstructed images
        mse_1 = np.mean(((img_array_1 - reconstructed_1).astype(np.float32) / 255.0) ** 2)
        mse_2 = np.mean(((img_array_2 - reconstructed_2).astype(np.float32) / 255.0) ** 2)

        # Average MSE of both images
        mse_cumulative_1[x - 1] += mse_1
        mse_cumulative_2[x - 1] += mse_2
        mse_sum_1 += mse_1
        mse_sum_2 += mse_2

    count += 1

mse_avg_1 = mse_cumulative_1 / count
mse_avg_2 = mse_cumulative_2 / count

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(8, 6))
plt.plot(mse_avg_1, marker='o', label="baseline")
plt.plot(mse_avg_2, marker='o', label="alignment")
plt.xlabel('Number of SVD Components (k)')
plt.ylabel('MSE')
plt.legend(loc="upper right")
plt.grid(True)

plot_path = f"svd_mse_{cls}.png"
plt.savefig(plot_path)
plt.close()

print(mse_sum_1 / count)
print(mse_sum_2 / count)
print(mse_sum_2 / mse_sum_1 * 100)
