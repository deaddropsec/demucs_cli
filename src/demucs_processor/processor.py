import shutil
import subprocess
from pathlib import Path
from typing import List

def process_audio_files(selected_files: List[Path], output_dir: Path, processed_dir: Path) -> None:
    """Process selected audio files using demucs"""
    output_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(exist_ok=True)
    
    print(f"\nProcessing {len(selected_files)} file(s)...\n")
    
    for i, audio_file in enumerate(selected_files, 1):
        print(f"[{i}/{len(selected_files)}] Processing: {audio_file.name}")
        
        try:
            cmd = [
                "python", "-m", "demucs",
                "-n", "mdx_extra",
                "-o", str(output_dir),
                "--filename", "{track}/{stem}.{ext}",
                str(audio_file)
            ]
            
            subprocess.run(cmd, check=True)
            
            # Move files from output/mdx_extra/<track>/ to output/<track>/
            track_name = audio_file.stem
            model_output_dir = output_dir / "mdx_extra" / track_name
            final_output_dir = output_dir / track_name
            
            if model_output_dir.exists():
                if final_output_dir.exists():
                    shutil.rmtree(final_output_dir)
                shutil.move(str(model_output_dir), str(final_output_dir))
            
            # Remove empty mdx_extra directory if it exists
            mdx_dir = output_dir / "mdx_extra"
            if mdx_dir.exists() and not any(mdx_dir.iterdir()):
                mdx_dir.rmdir()
            
            print(f"    Successfully processed: {audio_file.name}")
            
            # Move to processed
            dest_path = processed_dir / audio_file.name
            shutil.move(str(audio_file), str(dest_path))
            print(f"    Moved to processed folder")
            
        except subprocess.CalledProcessError as e:
            print(f"    Error processing {audio_file.name}: {e}")
        except Exception as e:
            print(f"    Unexpected error with {audio_file.name}: {e}")
    
    print("\nProcessing complete!")