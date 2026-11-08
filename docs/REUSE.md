# Reuse guide — Tactile_Database

[README](../README.md) · [Dandan Zhang’s fork](https://github.com/dianzdd123/Tactile_Database) · [MSEI Lab](https://zhangrobotics.com/msei_website/)

## Get this copy

```bash
git clone https://github.com/dianzdd123/Tactile_Database.git
cd Tactile_Database
```

## Purpose and environment

TacVerse supplies force regression, shape classification and grating classification benchmarks with shared training utilities. See the README for the dataset download and model/protocol overview. Install a mutually compatible PyTorch/torchvision build for CUDA or Apple MPS, plus `timm`, NumPy, pandas and Pillow in a Python 3.10+ environment. Training currently excludes CPU. No exact runtime lockfile was supplied by upstream; record resolved versions with results.

## Point the scripts at your dataset

The default root remains the **parent of the code directory**, preserving the original layout. Set `TACVERSE_DATA_ROOT` to use an explicit dataset location; the variable also selects the default `results` directory:

```bash
export TACVERSE_DATA_ROOT=/absolute/path/to/tacverse
python force_regression.py --metadata-only
python shape_classification.py --metadata-only
python grating_classification.py --metadata-only
```

The data root must contain `Force_Regression/`, `Shape_Classification/` and `Grating_Classification/`. Keep the dataset's internal sensor/label structure. Metadata-only mode still imports the ML utilities, so runtime dependencies must be installed; it does not train models.

## Run order and configuration

Start with one task and a small trial after checking the generated metadata:

```bash
python force_regression.py --device cuda --models resnet18 --epochs 1 --batch-size 16 --num-workers 0
```

Use `--help` on the selected script for protocol, seed, checkpoint and model options. `run_all.py` launches all three downstream scripts and can be substantially more expensive. MAE initialisation needs an appropriate pretrained MAE checkpoint or its pretraining stage; ImageNet modes can download weights. Use explicit local checkpoint paths offline and keep initialisation modes distinct when reporting results. `--allow-random-fallback` changes the initialisation condition if weights are unavailable.

## Splits and outputs

`common.assign_ordered_split` assigns ordered capture units within each sensor/group, keeping all rows of a unit in one split. It now rejects invalid ratios, missing group/order values, duplicate row indices and groups with fewer than three units. With three or more units, boundaries are clamped to keep train/validation/test nonempty. Ordinary 60/20/20 rounding is retained; very small groups may receive different membership than the earlier code, which could leave an empty test set.

Results are CSV files under `results/`, with checkpoints under `results/checkpoints/`. Archive the data version, split metadata, seeds, configuration and environment with each result. A one-epoch trial only establishes execution, not benchmark quality.

## Validation scope

Seven tests cover whole-unit splitting, standard ratios, small/invalid groups and the environment override. They use NumPy/pandas and temporary files; no dataset download, GPU, model training or accuracy measurement is included.

## Local quality checks

Run `python scripts/check_repository.py` from a Git checkout with Python 3.10+ and Git installed. It parses Python, JSON/notebook containers and links in the navigation documents without importing research modules. Notebook cells and remote links are not executed or tested.

## Attribution and reuse terms

This is a fork of [LannWei/Tactile_Database](https://github.com/LannWei/Tactile_Database). Original paper authorship, upstream citations and notices remain authoritative. Cite the associated work and identify this fork’s commit when reporting modifications.

No repository-wide licence file is present in this snapshot. Obtain the authors’ reuse terms before assuming permission to redistribute code, datasets or checkpoints. This documentation update does not relicense the work.
