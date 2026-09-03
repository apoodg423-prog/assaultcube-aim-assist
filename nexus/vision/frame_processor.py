"""Advanced Frame Capture and Preprocessing"""

import logging
import time
from typing import Tuple, Optional
import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from mss import mss
except ImportError:
    mss = None

logger = logging.getLogger(__name__)


class FrameProcessor:
    """Capture and preprocess frames for detection"""

    def __init__(
        self,
        target_width: int = 1920,
        target_height: int = 1080,
        target_fps: int = 60
    ):
        self.target_width = target_width
        self.target_height = target_height
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.sct = mss() if mss else None
        self.frame_count = 0
        self.fps_counter = {"frames": 0, "start": time.time()}
        self.last_frame = None
        self.frame_timestamps = []

    def capture_frame(self, monitor_idx: int = 1) -> Optional[np.ndarray]:
        """Capture frame from screen"""
        if not self.sct or not cv2:
            logger.warning("Screen capture not available")
            return None

        try:
            monitor = self.sct.monitors[monitor_idx]
            screenshot = self.sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            self.frame_count += 1
            self.frame_timestamps.append(time.time())
            return frame
        except Exception as e:
            logger.debug(f"Frame capture error: {e}")
            return None

    def preprocess_frame(
        self,
        frame: np.ndarray,
        resize: bool = True,
        normalize: bool = True
    ) -> np.ndarray:
        """Preprocess frame for inference"""
        if frame is None:
            return None

        if resize and cv2 and frame.shape != (self.target_height, self.target_width, 3):
            frame = cv2.resize(frame, (self.target_width, self.target_height))

        if normalize:
            frame = frame.astype(np.float32) / 255.0

        return frame

    def get_fps(self) -> float:
        """Calculate actual FPS"""
        if len(self.frame_timestamps) < 2:
            return 0

        recent = self.frame_timestamps[-60:]
        if len(recent) < 2:
            return 0

        time_diff = recent[-1] - recent[0]
        return len(recent) / time_diff if time_diff > 0 else 0

    def wait_frame_time(self):
        """Wait to maintain target FPS"""
        if len(self.frame_timestamps) < 2:
            return

        elapsed = time.time() - self.frame_timestamps[-1]
        wait_time = max(0, self.frame_time - elapsed)
        if wait_time > 0:
            time.sleep(wait_time)
