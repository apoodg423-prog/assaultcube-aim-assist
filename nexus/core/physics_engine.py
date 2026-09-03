"""Advanced Physics Engine for Ballistics & Lag Compensation"""

import logging
import math
from typing import Tuple, Optional
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class BallisticsData:
    """Ballistics configuration for weapons"""
    weapon_name: str
    bullet_speed: float
    gravity: float
    air_drag: float
    spread: float
    damage: int


class PhysicsEngine:
    """Advanced physics calculations for perfect aiming"""

    WEAPON_BALLISTICS = {
        "rifle": BallisticsData("rifle", 700, -9.81, 0.001, 0.5, 35),
        "sniper": BallisticsData("sniper", 900, -9.81, 0.0005, 0.1, 100),
        "shotgun": BallisticsData("shotgun", 400, -9.81, 0.01, 8.0, 25),
        "pistol": BallisticsData("pistol", 350, -9.81, 0.005, 2.0, 15),
        "smg": BallisticsData("smg", 500, -9.81, 0.003, 1.5, 12),
    }

    def __init__(self, player_ping_ms: int = 50):
        self.player_ping_ms = player_ping_ms
        self.server_tick_rate = 33

    def predict_target_position(
        self,
        current_pos: np.ndarray,
        velocity: np.ndarray,
        time_ahead: float = 0.1,
        acceleration: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Predict where a moving target will be in the future"""
        if acceleration is None:
            acceleration = np.zeros(3)

        predicted = current_pos + (velocity * time_ahead) + (0.5 * acceleration * time_ahead**2)
        return predicted

    def compensate_lag(
        self,
        target_pos: np.ndarray,
        target_vel: np.ndarray,
        ping_ms: int
    ) -> np.ndarray:
        """Compensate for network lag by predicting actual position"""
        lag_seconds = (ping_ms / 1000.0) / 2.0
        return self.predict_target_position(target_pos, target_vel, lag_seconds)

    def calculate_bullet_trajectory(
        self,
        origin: np.ndarray,
        target: np.ndarray,
        weapon_type: str = "rifle"
    ) -> Tuple[np.ndarray, float, bool]:
        """Calculate bullet trajectory with ballistics"""
        if weapon_type not in self.WEAPON_BALLISTICS:
            weapon_type = "rifle"

        ballistics = self.WEAPON_BALLISTICS[weapon_type]
        delta = target - origin
        distance = np.linalg.norm(delta)

        if distance == 0:
            return delta, 0, False

        travel_time = distance / ballistics.bullet_speed
        gravity_drop = 0.5 * ballistics.gravity * (travel_time ** 2)

        adjusted_target = target.copy()
        adjusted_target[2] += gravity_drop

        aim_direction = adjusted_target - origin
        aim_direction = aim_direction / (np.linalg.norm(aim_direction) + 1e-6)

        return aim_direction, travel_time, True

    def leading_calculation(
        self,
        my_pos: np.ndarray,
        target_pos: np.ndarray,
        target_vel: np.ndarray,
        bullet_speed: float
    ) -> Optional[np.ndarray]:
        """Calculate where to aim to hit a moving target (leading)"""
        delta = target_pos - my_pos
        dx = delta[0]
        dy = delta[1]
        dz = delta[2]
        vx = target_vel[0]
        vy = target_vel[1]
        vz = target_vel[2]

        a = vx**2 + vy**2 + vz**2 - bullet_speed**2
        b = 2 * (dx*vx + dy*vy + dz*vz)
        c = dx**2 + dy**2 + dz**2

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return None

        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b + sqrt_disc) / (2*a) if a != 0 else -c/b
        t2 = (-b - sqrt_disc) / (2*a) if a != 0 else -c/b

        t = None
        if t1 > 0:
            t = t1 if t2 <= 0 else min(t1, t2)
        elif t2 > 0:
            t = t2

        if t is None or t < 0:
            return None

        intercept = target_pos + target_vel * t
        return intercept

    def interpolate_smooth_aim(
        self,
        current_aim: np.ndarray,
        target_aim: np.ndarray,
        smoothing: float = 0.7,
        time_delta: float = 0.016
    ) -> np.ndarray:
        """Smoothly interpolate aim direction"""
        t = time_delta * (1 - smoothing)
        t = max(0, min(1, t))

        if t < 0.5:
            t_smooth = 2 * t * t
        else:
            t_smooth = 1 - (2 * (1 - t) ** 2)

        interpolated = current_aim + (target_aim - current_aim) * t_smooth
        interpolated = interpolated / (np.linalg.norm(interpolated) + 1e-6)

        return interpolated

    def add_human_like_jitter(
        self,
        aim: np.ndarray,
        intensity: float = 0.05
    ) -> np.ndarray:
        """Add realistic human tremor/jitter to aim"""
        jitter = np.random.normal(0, intensity * 0.5, 3)
        aim_jittered = aim + jitter
        return aim_jittered / (np.linalg.norm(aim_jittered) + 1e-6)

    def calculate_distance_variance(
        self,
        distance: float,
        base_accuracy: float = 0.95
    ) -> float:
        """Calculate accuracy falloff based on distance"""
        falloff = math.exp(-distance / 10000.0)
        return base_accuracy * falloff

    def set_player_ping(self, ping_ms: int):
        """Update player ping"""
        self.player_ping_ms = max(1, ping_ms)
