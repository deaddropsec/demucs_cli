#!/usr/bin/env python3
"""
Demucs Stem Splitter - Audio source separation tool
"""
import os
import certifi
from pathlib import Path
from demucs_processor.menu import select_files
from demucs_processor.processor import process_audio_files

# Fix SSL certificate issue on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

def main():
    """Main entry point"""
    # Directory paths
    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / "tracks_in"
    output_dir = base_dir / "tracks_out"
    processed_dir = base_dir / "tracks_processed"
    
    # Create directories if they don't exist
    input_dir.mkdir(exist_ok=True)
    
    # Select files
    selected_files = select_files(input_dir)
    
    if selected_files:
        process_audio_files(selected_files, output_dir, processed_dir)

if __name__ == "__main__":
    main()