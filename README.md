## Environment

In order to run scripts included in this project, create a Python environment using requirements.txt file, e.g.

```bash
python -m venv env
. env/bin/activate
pip install -r requirements.txt
```

## Data Acquisition and Preprocessing

Model is trained on CMP dataset with images cropped to individual facades. Navigate to data directory and run

```bash
./prepare_dataset.sh
```

The script will download CMP dataset, preprocess it and split into training, validation and test set.

## Training

## Inference

## Metrics evaluation
