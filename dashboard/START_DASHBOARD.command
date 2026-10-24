#!/bin/bash
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then echo 'Python 3 is required. Install Python 3 and run this again.'; read -r; exit 1; fi
if [ ! -d .venv ]; then python3 -m venv .venv || exit 1; fi
source .venv/bin/activate
python -m pip install -r requirements.txt || { echo 'Dependency installation failed. Internet is needed for the first install.'; read -r; exit 1; }
python -m streamlit run app.py
