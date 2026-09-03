"""Nexus Main Package"""

__version__ = "1.0.0"
__author__ = "apoodg423-prog"
__description__ = "Advanced multi-game AI aim-assist with physics, ensemble detection, and behavioral intelligence"

from nexus.core import AssaultCubeMemoryReader, PlayerData, Vector3, PhysicsEngine
from nexus.ai import EnsembleDetector, Detection, AimIntelligence, HumanAimProfile
from nexus.vision import FrameProcessor, OverlayRenderer
from nexus.utils import ConfigManager, setup_logger
from nexus.aim_assistant import AimAssistant
from nexus.input_controller import InputController

__all__ = [
    "AssaultCubeMemoryReader",
    "PlayerData",
    "Vector3",
    "PhysicsEngine",
    "EnsembleDetector",
    "Detection",
    "AimIntelligence",
    "HumanAimProfile",
    "FrameProcessor",
    "OverlayRenderer",
    "ConfigManager",
    "setup_logger",
    "AimAssistant",
    "InputController",
]
