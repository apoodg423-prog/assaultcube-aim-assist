"""PySide6 application bootstrap"""

def start_gui():
    try:
        from ui.main_window import start_gui as _start
        _start()
    except Exception as e:
        print("Failed to start GUI:", e)

