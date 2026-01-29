import os
import random
import shutil

def split_indices(n_total, val_split, test_split):
    n_val = round(val_split * n_total)
    n_test = round(test_split * n_total)

    train = [i for i in range(n_total)]
    val = []
    test = []

    for _ in range(n_val):
        ind = random.randint(0, len(train) - 1)
        val.append(train.pop(ind))
    
    for _ in range(n_test):
        ind = random.randint(0, len(train) - 1)
        test.append(train.pop(ind))

    train.sort()
    val.sort()
    test.sort()
    return train, val, test

def split_cmp(in_dir, out_dir):
    n_b = 424
    n_x = 265

    train_b, val_b, test_b = split_indices(n_b, 0.1, 0.1)
    train_x, val_x, test_x = split_indices(n_x, 0.1, 0.1)

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    set_types = ["train", "val", "test"]
    data_types = ["images", "labels"]

    for set_type in set_types:
        for data_type in data_types:
            os.makedirs(f"{out_dir}/{set_type}/{data_type}")

    for dataset, dataset_indices in zip(["b", "x"], [[train_b, val_b, test_b], [train_x, val_x, test_x]]):
        for set_type, indices in zip(set_types, dataset_indices):
            ind = 0
            for filename in sorted(os.listdir(f"{in_dir}/{dataset}_crop")):
                if os.path.splitext(filename)[1] != ".xml":
                    continue
                if ind in indices:
                    filename_base = os.path.splitext(filename)[0]
                    for data_type, extension in zip(data_types, ["jpg", "txt"]):
                        shutil.copyfile(f"{in_dir}/{dataset}_crop/{filename_base}.{extension}",
                                        f"{out_dir}/{set_type}/{data_type}/{filename_base}.{extension}")
                ind += 1

if __name__ == "__main__":
    random.seed(0)
    split_cmp(".", "yolo")
