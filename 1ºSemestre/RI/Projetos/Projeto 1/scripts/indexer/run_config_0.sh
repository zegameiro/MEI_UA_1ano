#!/bin/bash

cd ../../

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

python3 main.py --mode index --input_dir ../data/MEDLINE_2024_Baseline.jsonl --output_dir ../data/ --normalize_case