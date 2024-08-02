#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Activate the conda environment
source /opt/conda/etc/profile.d/conda.sh
conda activate myenv

cd /pointillism/lib/utils/iou3d/
python3 setup.py install

cd ../roipool3d/
python3 setup.py install

cd /pointillism
$@
