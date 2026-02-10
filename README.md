## Environment

In order to run scripts included in this project, create a Python environment and install required packages, e.g.:

```bash
python -m venv env
. env/bin/activate
pip install -r requirements.txt
```

## Data Acquisition and Preprocessing

Model is trained on CMP dataset with images cropped to individual facades. Navigate to the "data" directory and run:

```bash
./prepare_dataset.sh
```

The script will download CMP dataset, preprocess it and split into training, validation and test set.

## Model Preparation

The base for this project is YOLOv8 detection model created by Ultralytics. The project modifies its loss function. In order to use the modified model, navigate to the "model" directory and run:

```bash
./prepare_model.sh
```

The script will clone the YOLOv8 repository and apply changes defined in a patch file.

## Training

Navigate to the "model" directory. Set the desired number of epochs in train.py script. Then run:

```bash
python train.py
```

Results will be saved in model/ultralytics/runs/detect/train* directory (subsequent trainings will save results in "train", "train2", etc).

## Inference

For inference on a test set, navigate to model directory. Set the "model_dir" variable in infer.py to the training results directory name (e.g. "train"). Then run:

```bash
python infer.py
```

Results will be saved in model/ultralytics/runs/detect/infer_* (where * denotes the value of the model_dir variable). In order to specify a different set of images for inference, modify the "in_dir" variable in infer.py.

## Evaluation Metrics

### Standard Metrics

Original YOLO repository provides a method for standard metrics evaluation. Navigate to the model directory and run:

```
python val.py
```

### SVD-based metric
