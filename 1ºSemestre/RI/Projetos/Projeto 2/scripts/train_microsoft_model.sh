#!/bin/bash

cd ../

activate_venv() {
    # Check if the virtual environment is already active
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "Virtual environment is already active."
    else
        echo "Activating the virtual environment..."
        source venv/bin/activate
    fi
}

if [[ -d "venv" ]]; then
    echo "Virtual environment already exists."
    activate_venv
else
    echo "Creating a new virtual environment..."
    python3 -m venv venv
    activate_venv
fi

pip install -r requirements.txt

cd src/

python3 main.py --mode train --train_data_path ../data/training_data.jsonl --bm25_data_path ../data/training_data_bm25_ranked.jsonl --documents_path ../../Assignment1/data/MEDLINE_2024_Baseline.jsonl 