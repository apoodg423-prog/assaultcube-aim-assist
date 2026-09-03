"""Real-time Overlay Rendering"""

import logging
import numpy as np
from typing import List, Dict, Tuple, Optional

try:
    import cv2
except ImportError:
    cv2 = None

logger = logging.getLogger(__name__)


class OverlayRenderer:
    """Render detection overlays and statistics"""

    def __init__(
        self,
        width: int = 1920,
        height: int = 1080,
        alpha: float = 0.7
    ):
        self.width = width
        self.height = height
        self.alpha = alpha
        self.font = cv2.FONT_HERSHEY_SIMPLEX if cv2 else None

    def render(
        self,
        frame: np.ndarray,
        detections: List,
        head_positions: Dict[int, Tuple[float, float]],
        stats: Dict,
        show_boxes: bool = True,
        show_heads: bool = True,
        show_stats: bool = True
    ) -> Optional[np.ndarray]:
        """Render overlay on frame"""
        if frame is None or not cv2:
            return frame

        try:
            overlay = frame.copy()

            if show_boxes:
                for i, det in enumerate(detections):
                    self._draw_player_box(overlay, det, i in head_positions)

            if show_heads:
                for det_idx, (head_x, head_y) in head_positions.items():
                    cv2.circle(overlay, (int(head_x), int(head_y)), 8, (0, 255, 0), -1)
                    cv2.circle(overlay, (int(head_x), int(head_y)), 10, (0, 255, 0), 2)

            if show_stats:
                self._draw_stats(overlay, stats)

            result = cv2.addWeighted(frame, 1 - self.alpha, overlay, self.alpha, 0)
            return result
        except Exception as e:
            logger.debug(f"Render error: {e}")
            return frame

    def _draw_player_box(
        self,
        frame: np.ndarray,
        det,
        has_head: bool = False
    ):
        """Draw player bounding box"""
        if not cv2:
            return

        x1 = int(det.x - det.w / 2)
        y1 = int(det.y - det.h / 2)
        x2 = int(det.x + det.w / 2)
        y2 = int(det.y + det.h / 2)

        if det.confidence > 0.8:
            color = (0, 255, 0)
        elif det.confidence > 0.6:
            color = (0, 255, 255)
        else:
            color = (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{det.class_name} {det.confidence:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), self.font, 0.5, color, 1)

    def _draw_stats(
        self,
        frame: np.ndarray,
        stats: Dict
    ):
        """Draw statistics overlay"""
        if not cv2:
            return

        y_offset = 30
        line_height = 25

        for key, value in stats.items():
            if isinstance(value, float):
                text = f"{key}: {value:.1f}"
            else:
                text = f"{key}: {value}"
            cv2.putText(
                frame,
                text,
                (10, y_offset),
                self.font,
                0.6,
                (0, 255, 0),
                1
            )
            y_offset += line_height
