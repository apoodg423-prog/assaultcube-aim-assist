"""App runner for Ipro71 Nexus - launches PySide6 UI or CLI compatibility mode"""
import sys
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run():
    # Lazy import to avoid heavy deps at module import
    try:
        from ui.main import start_gui
        start_gui()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        print("Falling back to CLI mode...")
        try:
            import main as legacy_main
            legacy_main.main()
        except Exception as e2:
            print(f"Failed to start CLI mode: {e2}")


if __name__ == '__main__':
    run()
