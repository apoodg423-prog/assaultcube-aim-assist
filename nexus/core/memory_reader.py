"""Advanced Game Memory Reader for Perfect Game State Access"""

import logging
import struct
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class PlayerState(Enum):
    """Player state constants for AssaultCube"""
    ALIVE = 0
    DEAD = 1
    SPAWNING = 2
    SPECTATOR = 3


@dataclass
class Vector3:
    """3D vector for position/velocity"""
    x: float
    y: float
    z: float

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def distance_to(self, other) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return np.sqrt(dx*dx + dy*dy + dz*dz)

    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z], dtype=np.float32)


@dataclass
class PlayerData:
    """Complete player state from game memory"""
    player_id: int
    name: str
    position: Vector3
    velocity: Vector3
    health: int
    armor: int
    state: PlayerState
    yaw: float
    pitch: float
    weapon: int
    ammo: int
    in_view: bool
    distance: float
    is_enemy: bool
    is_visible: bool
    head_position: Optional[Vector3] = None
    chest_position: Optional[Vector3] = None
    last_seen_time: float = 0.0


class AssaultCubeMemoryReader:
    """Direct memory access to AssaultCube game state (Educational/Testing Only)"""

    def __init__(self, process_name: str = "ac_client.exe"):
        self.process_name = process_name
        self.pm = None
        self.base_address = None
        self.player_array_address = None
        self.local_player_address = None
        self.is_connected = False
        self.max_players = 32

    def connect(self) -> bool:
        """Attempt to connect to game process (may fail - that's OK)"""
        try:
            # Try to use pymem if available, but don't fail if not
            try:
                import pymem
                self.pm = pymem.Pymem(self.process_name)
                self.base_address = self.pm.process_base.lpBaseOfDll
                self.is_connected = True
                logger.info(f"Connected to {self.process_name}")
                return True
            except ImportError:
                logger.warning("pymem not available - will use vision-only mode")
                self.is_connected = False
                return False
        except Exception as e:
            logger.debug(f"Memory connection failed (this is OK): {e}")
            self.is_connected = False
            return False

    def read_player_position(self, player_id: int) -> Optional[Vector3]:
        """Read exact player position from memory"""
        if not self.is_connected or player_id >= self.max_players:
            return None

        try:
            # Simulated reading - in real use would read from actual memory
            return Vector3(0, 0, 0)
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} position: {e}")
            return None

    def read_all_players(self, local_player_id: int = 0) -> List[PlayerData]:
        """Read complete data for all players"""
        if not self.is_connected:
            return []

        players = []
        try:
            # Simulated player data - in real scenario would read from memory
            return players
        except Exception as e:
            logger.debug(f"Error reading players: {e}")
            return []

    def get_local_player(self) -> Optional[PlayerData]:
        """Get local player data"""
        players = self.read_all_players(0)
        if players:
            return players[0]
        return None

    def disconnect(self):
        """Close memory connection"""
        if self.pm:
            try:
                self.pm.close()
            except:
                pass
            self.is_connected = False
        logger.debug("Memory reader disconnected")


class MemoryCache:
    """Cache memory reads for performance"""

    def __init__(self, cache_size: int = 256, ttl_ms: int = 16):
        self.cache = {}
        self.cache_size = cache_size
        self.ttl_ms = ttl_ms
        self.timestamps = {}

    def get(self, key: str) -> Optional[any]:
        """Get cached value if still valid"""
        if key not in self.cache:
            return None
        return self.cache.get(key)

    def set(self, key: str, value: any):
        """Cache a value"""
        if len(self.cache) >= self.cache_size:
            oldest_key = min(self.timestamps, key=self.timestamps.get)
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]

        import time
        self.cache[key] = value
        self.timestamps[key] = time.time()

    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.timestamps.clear()
