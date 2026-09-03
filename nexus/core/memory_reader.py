"""Advanced Game Memory Reader for Perfect Game State Access"""

import logging
import struct
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class PlayerState(Enum):
    """Player state constants"""
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

    def __truediv__(self, scalar):
        if scalar == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def magnitude(self) -> float:
        """Calculate vector magnitude"""
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> 'Vector3':
        """Return normalized vector"""
        mag = self.magnitude()
        if mag == 0:
            return Vector3(0, 0, 0)
        return self / mag

    def distance_to(self, other) -> float:
        """Calculate distance to another vector"""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return np.sqrt(dx*dx + dy*dy + dz*dz)

    def to_array(self) -> np.ndarray:
        """Convert to numpy array"""
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


class MemoryLayout:
    """Generic memory layout configuration for games
    
    Subclass this for specific games and provide offset constants
    """
    
    # Override these in subclasses
    PLAYER_ARRAY_BASE = None  # Offset from base or signature
    PLAYER_SIZE = 0x200  # Default, override per game
    MAX_PLAYERS = 32
    
    # Player struct offsets (relative to player base) - must be overridden
    OFFSET_POSITION = None
    OFFSET_VELOCITY = None
    OFFSET_HEALTH = None
    OFFSET_ARMOR = None
    OFFSET_STATE = None
    OFFSET_YAW = None
    OFFSET_PITCH = None
    OFFSET_WEAPON = None
    OFFSET_AMMO = None
    OFFSET_NAME = None
    OFFSET_NAME_SIZE = 32  # Max name length
    
    # Head position offset from feet (game-specific)
    HEAD_HEIGHT_OFFSET = 60.0
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required offsets are set"""
        required = [
            'PLAYER_ARRAY_BASE', 'OFFSET_POSITION', 'OFFSET_VELOCITY',
            'OFFSET_HEALTH', 'OFFSET_STATE', 'OFFSET_YAW', 'OFFSET_PITCH'
        ]
        for attr in required:
            if getattr(cls, attr, None) is None:
                return False
        return True


class AssaultCubeMemoryReader:
    """Direct memory access to game state (Educational/Testing Only)
    
    This is a generic implementation that can be subclassed for specific games.
    Memory reading is optional and gracefully degrades to vision-only mode.
    """

    def __init__(
        self,
        process_name: str = "ac_client.exe",
        memory_layout: type = MemoryLayout
    ):
        self.process_name = process_name
        self.memory_layout = memory_layout
        self.pm = None
        self.base_address = None
        self.player_array_address = None
        self.local_player_address = None
        self.is_connected = False
        self.max_players = memory_layout.MAX_PLAYERS
        self.pymem_available = False
        self._check_pymem()

    def _check_pymem(self) -> None:
        """Check if pymem is available"""
        try:
            import pymem
            self.pymem_available = True
        except ImportError:
            self.pymem_available = False
            logger.debug("pymem not available - memory reading disabled")

    def connect(self) -> bool:
        """Attempt to connect to game process
        
        Returns:
            True if connected, False if pymem unavailable (graceful degradation)
        """
        if not self.pymem_available:
            logger.debug("Memory reading not available - using vision-only mode")
            return False

        try:
            import pymem
            self.pm = pymem.Pymem(self.process_name)
            
            if self.pm is None or self.pm.process_handle is None:
                logger.warning(f"Could not attach to {self.process_name}")
                self.is_connected = False
                return False
            
            # Get base address of main module
            try:
                self.base_address = self.pm.process_base.lpBaseOfDll
                if self.base_address == 0 or self.base_address is None:
                    logger.warning("Invalid base address")
                    self.is_connected = False
                    return False
            except Exception as e:
                logger.debug(f"Could not get base address: {e}")
                self.is_connected = False
                return False
            
            # Attempt to find player array (game-specific)
            if self.memory_layout.PLAYER_ARRAY_BASE is not None:
                if isinstance(self.memory_layout.PLAYER_ARRAY_BASE, int):
                    self.player_array_address = self.base_address + self.memory_layout.PLAYER_ARRAY_BASE
                else:
                    # Would be signature scan in real implementation
                    self.player_array_address = self.base_address + 0x10A8860
                logger.debug(f"Player array at: 0x{self.player_array_address:X}")
            
            self.is_connected = True
            logger.info(f"Connected to {self.process_name} at 0x{self.base_address:X}")
            return True
            
        except FileNotFoundError:
            logger.debug(f"Process {self.process_name} not found")
            self.is_connected = False
            return False
        except PermissionError:
            logger.debug(f"Permission denied accessing {self.process_name}")
            self.is_connected = False
            return False
        except Exception as e:
            logger.debug(f"Memory connection failed: {e}")
            self.is_connected = False
            return False

    def read_bytes(self, address: int, size: int) -> Optional[bytes]:
        """Read bytes from memory
        
        Args:
            address: Memory address to read from
            size: Number of bytes to read
            
        Returns:
            Bytes read or None on error
        """
        if not self.is_connected or not self.pm:
            return None
        
        try:
            if address == 0 or address is None:
                return None
            return self.pm.read_bytes(address, size)
        except Exception as e:
            logger.debug(f"Failed to read {size} bytes at 0x{address:X}: {e}")
            return None

    def read_float(self, address: int) -> Optional[float]:
        """Read single float from memory"""
        data = self.read_bytes(address, 4)
        if data is None:
            return None
        try:
            return struct.unpack('f', data)[0]
        except:
            return None

    def read_int32(self, address: int) -> Optional[int]:
        """Read 32-bit integer from memory"""
        data = self.read_bytes(address, 4)
        if data is None:
            return None
        try:
            return struct.unpack('i', data)[0]
        except:
            return None

    def read_uint32(self, address: int) -> Optional[int]:
        """Read unsigned 32-bit integer from memory"""
        data = self.read_bytes(address, 4)
        if data is None:
            return None
        try:
            return struct.unpack('I', data)[0]
        except:
            return None

    def read_string(self, address: int, max_length: int = 32) -> Optional[str]:
        """Read null-terminated string from memory"""
        data = self.read_bytes(address, max_length)
        if data is None:
            return None
        try:
            # Find null terminator
            null_idx = data.find(b'\x00')
            if null_idx != -1:
                data = data[:null_idx]
            return data.decode('utf-8', errors='ignore').strip()
        except:
            return "Unknown"

    def read_player_position(self, player_id: int) -> Optional[Vector3]:
        """Read exact player position from memory
        
        Returns None if:
        - Not connected to game memory
        - Player ID is invalid
        - Memory read fails
        """
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return None

        if self.memory_layout.OFFSET_POSITION is None:
            return None

        try:
            # Calculate player address
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            pos_addr = player_addr + self.memory_layout.OFFSET_POSITION
            
            # Read 3 floats (x, y, z)
            data = self.read_bytes(pos_addr, 12)
            if data is None or len(data) < 12:
                return None
            
            x, y, z = struct.unpack('fff', data)
            
            # Basic sanity check (positions shouldn't be extremely far from origin)
            if abs(x) > 100000 or abs(y) > 100000 or abs(z) > 100000:
                logger.debug(f"Suspicious player position: ({x}, {y}, {z})")
                return None
            
            return Vector3(x, y, z)
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} position: {e}")
            return None

    def read_player_velocity(self, player_id: int) -> Optional[Vector3]:
        """Read player velocity from memory"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return None

        if self.memory_layout.OFFSET_VELOCITY is None:
            return Vector3(0, 0, 0)

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            vel_addr = player_addr + self.memory_layout.OFFSET_VELOCITY
            
            data = self.read_bytes(vel_addr, 12)
            if data is None or len(data) < 12:
                return Vector3(0, 0, 0)
            
            x, y, z = struct.unpack('fff', data)
            return Vector3(x, y, z)
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} velocity: {e}")
            return Vector3(0, 0, 0)

    def read_player_health(self, player_id: int) -> int:
        """Read player health from memory"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return 0

        if self.memory_layout.OFFSET_HEALTH is None:
            return 0

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            health_addr = player_addr + self.memory_layout.OFFSET_HEALTH
            health = self.read_int32(health_addr)
            return max(0, health) if health is not None else 0
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} health: {e}")
            return 0

    def read_player_armor(self, player_id: int) -> int:
        """Read player armor from memory"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return 0

        if self.memory_layout.OFFSET_ARMOR is None:
            return 0

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            armor_addr = player_addr + self.memory_layout.OFFSET_ARMOR
            armor = self.read_int32(armor_addr)
            return max(0, armor) if armor is not None else 0
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} armor: {e}")
            return 0

    def read_player_state(self, player_id: int) -> PlayerState:
        """Read player alive/dead state"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return PlayerState.DEAD

        if self.memory_layout.OFFSET_STATE is None:
            return PlayerState.ALIVE

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            state_addr = player_addr + self.memory_layout.OFFSET_STATE
            state_val = self.read_int32(state_addr)
            
            if state_val is None:
                return PlayerState.DEAD
            
            # Try to match enum
            try:
                return PlayerState(state_val)
            except ValueError:
                # Unknown state, assume alive if positive
                return PlayerState.ALIVE if state_val >= 0 else PlayerState.DEAD
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} state: {e}")
            return PlayerState.DEAD

    def read_player_rotation(self, player_id: int) -> Tuple[float, float]:
        """Read player yaw and pitch angles"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return (0.0, 0.0)

        if self.memory_layout.OFFSET_YAW is None or self.memory_layout.OFFSET_PITCH is None:
            return (0.0, 0.0)

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            
            yaw_addr = player_addr + self.memory_layout.OFFSET_YAW
            pitch_addr = player_addr + self.memory_layout.OFFSET_PITCH
            
            yaw = self.read_float(yaw_addr)
            pitch = self.read_float(pitch_addr)
            
            return (yaw or 0.0, pitch or 0.0)
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} rotation: {e}")
            return (0.0, 0.0)

    def read_player_weapon(self, player_id: int) -> int:
        """Read current weapon ID"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return 0

        if self.memory_layout.OFFSET_WEAPON is None:
            return 0

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            weapon_addr = player_addr + self.memory_layout.OFFSET_WEAPON
            weapon = self.read_int32(weapon_addr)
            return weapon if weapon is not None else 0
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} weapon: {e}")
            return 0

    def read_player_ammo(self, player_id: int) -> int:
        """Read current ammo count"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return 0

        if self.memory_layout.OFFSET_AMMO is None:
            return 0

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            ammo_addr = player_addr + self.memory_layout.OFFSET_AMMO
            ammo = self.read_int32(ammo_addr)
            return max(0, ammo) if ammo is not None else 0
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} ammo: {e}")
            return 0

    def read_player_name(self, player_id: int) -> str:
        """Read player name"""
        if not self.is_connected or player_id >= self.max_players or player_id < 0:
            return f"Player_{player_id}"

        if self.memory_layout.OFFSET_NAME is None:
            return f"Player_{player_id}"

        try:
            player_addr = self.player_array_address + (player_id * self.memory_layout.PLAYER_SIZE)
            name_addr = player_addr + self.memory_layout.OFFSET_NAME
            name = self.read_string(name_addr, self.memory_layout.OFFSET_NAME_SIZE)
            return name or f"Player_{player_id}"
        except Exception as e:
            logger.debug(f"Failed to read player {player_id} name: {e}")
            return f"Player_{player_id}"

    def read_all_players(self, local_player_id: int = 0) -> List[PlayerData]:
        """Read complete data for all players
        
        Returns empty list if not connected to memory
        """
        if not self.is_connected:
            return []

        players = []
        local_pos = self.read_player_position(local_player_id)
        
        try:
            for i in range(self.max_players):
                pos = self.read_player_position(i)
                if pos is None:
                    continue
                
                state = self.read_player_state(i)
                if state == PlayerState.DEAD:
                    continue
                
                # Read all player attributes
                vel = self.read_player_velocity(i) or Vector3(0, 0, 0)
                health = self.read_player_health(i)
                armor = self.read_player_armor(i)
                yaw, pitch = self.read_player_rotation(i)
                weapon = self.read_player_weapon(i)
                ammo = self.read_player_ammo(i)
                name = self.read_player_name(i)
                
                # Calculate derived values
                distance = pos.distance_to(local_pos) if local_pos else 0
                head_pos = Vector3(
                    pos.x,
                    pos.y,
                    pos.z + self.memory_layout.HEAD_HEIGHT_OFFSET
                )
                
                player = PlayerData(
                    player_id=i,
                    name=name,
                    position=pos,
                    velocity=vel,
                    health=health,
                    armor=armor,
                    state=state,
                    yaw=yaw,
                    pitch=pitch,
                    weapon=weapon,
                    ammo=ammo,
                    in_view=distance < 5000,
                    distance=distance,
                    is_enemy=(i != local_player_id),
                    is_visible=True,  # Would need wall raycasting to determine
                    head_position=head_pos,
                    last_seen_time=time.time()
                )
                players.append(player)
            
            return players
        except Exception as e:
            logger.debug(f"Error reading players: {e}")
            return []

    def get_local_player(self) -> Optional[PlayerData]:
        """Get local player data
        
        Returns None if:
        - Not connected to memory
        - Local player not found
        """
        if not self.is_connected:
            return None
        
        try:
            players = self.read_all_players(0)
            if players:
                return players[0]
            return None
        except Exception as e:
            logger.debug(f"Failed to get local player: {e}")
            return None

    def disconnect(self):
        """Close memory connection"""
        if self.pm:
            try:
                self.pm.close()
            except Exception as e:
                logger.debug(f"Error closing pymem: {e}")
        self.is_connected = False
        logger.debug("Memory reader disconnected")


class MemoryCache:
    """Cache memory reads for performance
    
    Implements LRU (Least Recently Used) eviction with TTL (Time-To-Live)
    """

    def __init__(self, cache_size: int = 256, ttl_ms: int = 16):
        """Initialize cache
        
        Args:
            cache_size: Maximum number of entries
            ttl_ms: Time-to-live for cached entries in milliseconds
        """
        self.cache = {}
        self.cache_size = cache_size
        self.ttl_ms = ttl_ms
        self.timestamps = {}

    def get(self, key: str) -> Optional[any]:
        """Get cached value if still valid
        
        Returns None if:
        - Key not in cache
        - Entry has expired (TTL exceeded)
        """
        if key not in self.cache:
            return None
        
        # Check if data expired
        age_ms = (time.time() - self.timestamps[key]) * 1000
        
        if age_ms > self.ttl_ms:
            # Remove expired entry
            del self.cache[key]
            del self.timestamps[key]
            logger.debug(f"Cache entry {key} expired after {age_ms:.1f}ms")
            return None
        
        return self.cache[key]

    def set(self, key: str, value: any):
        """Cache a value
        
        Evicts oldest entry if cache is full
        """
        if len(self.cache) >= self.cache_size:
            # Simple LRU - remove oldest
            if self.timestamps:
                oldest_key = min(self.timestamps, key=self.timestamps.get)
                del self.cache[oldest_key]
                del self.timestamps[oldest_key]
                logger.debug(f"Evicted cache entry {oldest_key}")

        self.cache[key] = value
        self.timestamps[key] = time.time()

    def clear(self):
        """Clear all cached entries"""
        self.cache.clear()
        self.timestamps.clear()
        logger.debug("Cache cleared")

    def get_stats(self) -> Dict[str, any]:
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'capacity': self.cache_size,
            'utilization': len(self.cache) / self.cache_size if self.cache_size > 0 else 0,
            'ttl_ms': self.ttl_ms
        }
