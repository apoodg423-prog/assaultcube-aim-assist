from threading import Thread
import time
from nexus.aim_assistant import AimAssistant
from nexus.utils.config_manager import ConfigManager

class AppController:
    """Central controller to manage backend components and expose stats to UI"""
    def __init__(self, config_path='config.yaml'):
        self.config = ConfigManager.load(config_path) or {}
        self.assistant = None
        self._thread = None
        self.running = False

    def start_assistant(self):
        if self.assistant and self.assistant.is_running:
            return
        self.assistant = AimAssistant(self.config)
        self._thread = Thread(target=self.assistant.start, daemon=True)
        self._thread.start()
        self.running = True

    def stop_assistant(self):
        if self.assistant:
            self.assistant.stop()
        self.running = False

    def get_stats(self):
        if self.assistant:
            return getattr(self.assistant, 'stats', {})
        return {}

# Simple singleton
_controller = AppController()

def get_controller():
    return _controller
