# Demucs Stem Splitter CLI

Little CLI menu wrapper around demucs.
All credit to https://github.com/adefossez/demucs

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
./run.sh
```

## Usage

1. Place audio files in `tracks_in/`
2. Run the app and select files with arrow keys
3. Find stems in `tracks_out/<songname>/`
4. Processed files move to `tracks_done/`