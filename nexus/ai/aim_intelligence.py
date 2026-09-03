"""Advanced Aim Intelligence with Behavioral Randomization"""

import logging
import time
import random
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class AimBehavior(Enum):
    """Different aiming behaviors"""
    AGGRESSIVE = 1
    CAREFUL = 2
    TRACKING = 3
    SPRAY = 4
    PANIC = 5


@dataclass
class HumanAimProfile:
    """Profile mimicking human aiming characteristics"""
    avg_reaction_time_ms: float
    aim_smoothing: float
    tremor_intensity: float
    focus_accuracy: float
    distraction_factor: float
    preferred_aim_bone: str
    spray_compensation: float
    leading_skill: float


class BehavioralRandomizer:
    """Add human-like randomness to aim"""

    def __init__(self):
        self.frame_count = 0
        self.behavior_history = []
        self.behavior_timeout = 0
        self.current_behavior = AimBehavior.TRACKING
        self.behavior_confidence = 0.5

    def generate_human_profile(self) -> HumanAimProfile:
        """Generate realistic human profile"""
        return HumanAimProfile(
            avg_reaction_time_ms=random.uniform(80, 350),
            aim_smoothing=random.uniform(0.4, 0.9),
            tremor_intensity=random.uniform(0.02, 0.15),
            focus_accuracy=random.uniform(0.70, 0.98),
            distraction_factor=random.uniform(0.01, 0.10),
            preferred_aim_bone=random.choice(["head", "neck", "chest"]),
            spray_compensation=random.uniform(0.3, 0.95),
            leading_skill=random.uniform(0.5, 0.95)
        )

    def select_behavior(
        self,
        target_distance: float,
        target_velocity: float,
        player_health: int,
        enemies_nearby: int
    ) -> AimBehavior:
        """Select behavior based on game state"""
        if self.behavior_timeout > 0:
            self.behavior_timeout -= 1
            return self.current_behavior

        if player_health < 30:
            behavior = AimBehavior.PANIC
        elif target_velocity > 200:
            behavior = AimBehavior.TRACKING
        elif target_distance < 500:
            behavior = AimBehavior.AGGRESSIVE
        elif enemies_nearby > 2:
            behavior = AimBehavior.SPRAY
        else:
            behavior = AimBehavior.CAREFUL

        self.current_behavior = behavior
        self.behavior_timeout = random.randint(60, 200)
        return behavior

    def add_reaction_delay(
        self,
        target_spotted_time: float,
        profile: HumanAimProfile
    ) -> bool:
        """Check if enough time has passed for reaction"""
        elapsed = (time.time() - target_spotted_time) * 1000
        reaction_time = profile.avg_reaction_time_ms * random.uniform(0.8, 1.2)
        return elapsed > reaction_time

    def should_miss(
        self,
        profile: HumanAimProfile,
        behavior: AimBehavior,
        shots_fired: int = 0
    ) -> bool:
        """Decide whether to intentionally miss"""
        base_miss_chance = profile.distraction_factor

        if behavior == AimBehavior.PANIC:
            base_miss_chance *= 3

        if shots_fired > 5:
            base_miss_chance += (shots_fired - 5) * 0.05

        return random.random() < base_miss_chance


class IntentionalMissGenerator:
    """Generate realistic misses"""

    def __init__(self):
        self.miss_positions = []
        self.last_miss_frame = 0

    def generate_miss_offset(
        self,
        shot_number: int,
        distance: float,
        behavior: AimBehavior = AimBehavior.TRACKING
    ) -> Tuple[float, float]:
        """Generate realistic miss offset"""
        distance_scale = 1.0 + (distance / 10000.0)

        if behavior == AimBehavior.PANIC:
            base_offset = random.uniform(20, 80)
        elif behavior == AimBehavior.AGGRESSIVE:
            base_offset = random.uniform(5, 20)
        elif behavior == AimBehavior.TRACKING:
            base_offset = random.uniform(2, 8)
        else:
            base_offset = random.uniform(1, 5)

        angle = random.uniform(0, 2 * math.pi)
        offset_x = base_offset * distance_scale * math.cos(angle)
        offset_y = base_offset * distance_scale * math.sin(angle)

        return offset_x, offset_y


class AimIntelligence:
    """Main aim intelligence system"""

    def __init__(self):
        self.randomizer = BehavioralRandomizer()
        self.miss_generator = IntentionalMissGenerator()
        self.profiles: Dict[str, HumanAimProfile] = {}
        self.target_history = {}
        self.aim_trajectory = []
        self.last_aimed_time = time.time()

    def get_or_create_profile(self, player_id: str) -> HumanAimProfile:
        """Get or create profile for player"""
        if player_id not in self.profiles:
            self.profiles[player_id] = self.randomizer.generate_human_profile()
        return self.profiles[player_id]

    def calculate_intelligent_aim(
        self,
        current_pos: np.ndarray,
        target_pos: np.ndarray,
        target_velocity: np.ndarray,
        profile: HumanAimProfile,
        game_state: Dict,
        intended_hit: bool = True
    ) -> np.ndarray:
        """Calculate aim with human-like characteristics"""
        distance = np.linalg.norm(target_pos - current_pos)
        velocity_mag = np.linalg.norm(target_velocity)
        behavior = self.randomizer.select_behavior(
            distance,
            velocity_mag,
            game_state.get("player_health", 100),
            game_state.get("nearby_enemies", 1)
        )

        delta = target_pos - current_pos
        ideal_aim = delta / (np.linalg.norm(delta) + 1e-6)

        if velocity_mag > 50:
            predicted_offset = target_velocity * (profile.leading_skill / 60.0)
            predicted_pos = target_pos + predicted_offset
            delta = predicted_pos - current_pos
            ideal_aim = delta / (np.linalg.norm(delta) + 1e-6)

        if not intended_hit and self.randomizer.should_miss(profile, behavior):
            miss_x, miss_y = self.miss_generator.generate_miss_offset(
                game_state.get("shots_fired", 0),
                distance,
                behavior
            )
            ideal_aim[0] += miss_x / 1000.0
            ideal_aim[1] += miss_y / 1000.0

        if len(self.aim_trajectory) > 0:
            last_aim = self.aim_trajectory[-1]
            smoothed = last_aim + (ideal_aim - last_aim) * (1 - profile.aim_smoothing)
        else:
            smoothed = ideal_aim

        self.aim_trajectory.append(smoothed)
        if len(self.aim_trajectory) > 100:
            self.aim_trajectory.pop(0)

        return smoothed / (np.linalg.norm(smoothed) + 1e-6)

    def should_shoot(
        self,
        aim_accuracy: float,
        distance: float,
        profile: HumanAimProfile
    ) -> bool:
        """Decide whether aim is good enough to shoot"""
        threshold = profile.focus_accuracy * (1.0 - distance / 10000.0)
        threshold = max(0.3, min(0.95, threshold))
        return aim_accuracy > threshold
