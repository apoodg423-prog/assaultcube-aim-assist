"""Advanced Input Control System with Smoothing"""

import logging
import time
from typing import Tuple
import numpy as np
from pynput.mouse import Controller, Button
import keyboard

logger = logging.getLogger(__name__)


class InputController:
    """Control mouse and keyboard input with advanced smoothing"""

    def __init__(self):
        self.mouse = Controller()
        self.is_active = False
        self.last_move_time = time.time()

    def move_mouse_smooth(
        self,
        delta_x: float,
        delta_y: float,
        duration: float = 0.01,
        easing: str = "cubic"
    ):
        """
        Move mouse with smooth interpolation.
        
        Args:
            delta_x, delta_y: Relative movement in pixels
            duration: Time to complete movement (seconds)
            easing: Easing function (linear, cubic, exponential)
        """
        try:
            if abs(delta_x) < 0.1 and abs(delta_y) < 0.1:
                return  # Too small to move

            if easing == "cubic":
                # Cubic easing for smooth acceleration/deceleration
                steps = max(1, int(duration * 1000))  # Convert to steps
                for i in range(1, steps + 1):
                    t = i / steps
                    # Smoothstep function: t^2 * (3 - 2t)
                    t_smooth = t * t * (3 - 2 * t)
                    
                    move_x = delta_x * t_smooth
                    move_y = delta_y * t_smooth
                    
                    self.mouse.move(move_x, move_y)
                    time.sleep(duration / max(steps, 1))
            elif easing == "exponential":
                # Exponential easing
                steps = max(1, int(duration * 1000))
                for i in range(1, steps + 1):
                    t = i / steps
                    t_smooth = t * t * t  # Cubic acceleration
                    
                    move_x = delta_x * t_smooth
                    move_y = delta_y * t_smooth
                    
                    self.mouse.move(move_x, move_y)
                    time.sleep(duration / max(steps, 1))
            else:
                # Linear - instant move
                self.mouse.move(delta_x, delta_y)
                time.sleep(duration)
        except Exception as e:
            logger.debug(f"Mouse move error (may be expected): {e}")

    def click(self, button: str = "left", count: int = 1):
        """Click mouse button"""
        try:
            btn = Button.left if button.lower() == "left" else Button.right
            for _ in range(count):
                self.mouse.click(btn)
                time.sleep(0.05)
        except Exception as e:
            logger.error(f"Failed to click: {e}")

    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        try:
            return self.mouse.position
        except:
            return (0, 0)

    def set_mouse_position(self, x: int, y: int):
        """Set mouse position absolutely"""
        try:
            self.mouse.position = (x, y)
        except Exception as e:
            logger.error(f"Failed to set mouse position: {e}")

    def is_key_pressed(self, key: str) -> bool:
        """Check if key is currently pressed"""
        try:
            return keyboard.is_pressed(key)
        except:
            return False
