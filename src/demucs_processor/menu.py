import sys
import termios
import tty
from pathlib import Path
from typing import List, Optional

def get_key() -> str:
    """Get a single keypress"""
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            if key == '\x1b':  # ESC sequence
                key += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    except:
        # Fallback for non-TTY environments
        return input()

def display_menu(options: List[str], selected_index: int) -> None:
    """Display the menu with arrow selection"""
    print("\033[2J\033[H")  # Clear screen and move cursor to top
    print("=== Demucs Audio Processor ===")
    print("Use ↑/↓ arrows to select, Enter to confirm, 'q' to quit\n")
    
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"→ {option}")
        else:
            print(f"  {option}")

def select_files(input_dir: Path) -> Optional[List[Path]]:
    """Interactive menu to select files to process"""
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.opus'}
    
    audio_files = sorted([f for f in input_dir.iterdir() if f.suffix.lower() in audio_extensions])
    
    if not audio_files:
        print("No audio files found in input directory")
        return None
    
    options = ["Process all files"] + [f.name for f in audio_files]
    selected_index = 0
    
    while True:
        display_menu(options, selected_index)
        
        key = get_key()
        
        if key == '\x1b[A':  # Up arrow
            selected_index = (selected_index - 1) % len(options)
        elif key == '\x1b[B':  # Down arrow
            selected_index = (selected_index + 1) % len(options)
        elif key == '\r' or key == '\n':  # Enter
            if selected_index == 0:
                return audio_files  # Return all files
            else:
                return [audio_files[selected_index - 1]]  # Return selected file
        elif key == 'q' or key == '\x03':  # q or Ctrl+C
            print("\nExiting...")
            return None