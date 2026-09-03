"""Base Game Adapter for multi-game support"""
from abc import ABC, abstractmethod

class GameAdapter(ABC):
    def __init__(self, name: str, exe_path: str = None):
        self.name = name
        self.exe_path = exe_path
        self.supported_features = []

    @abstractmethod
    def detect_process(self) -> bool:
        """Return True if the game process is found/runnable"""
        raise NotImplementedError

    @abstractmethod
    def read_game_state(self):
        """Read game-specific state (optional)"""
        raise NotImplementedError

    def get_supported_features(self):
        return self.supported_features
