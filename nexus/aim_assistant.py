"""Main Aim Assistant Orchestrator - Production Ready"""

import logging
import time
import threading
from typing import Optional, Dict, List
import numpy as np
from pathlib import Path

try:
    import cv2
except ImportError:
    cv2 = None

from nexus.core.memory_reader import AssaultCubeMemoryReader
from nexus.core.physics_engine import PhysicsEngine
from nexus.ai.detection_engine import EnsembleDetector
from nexus.ai.aim_intelligence import AimIntelligence
from nexus.vision.frame_processor import FrameProcessor
from nexus.vision.overlay_renderer import OverlayRenderer
from nexus.input_controller import InputController
from nexus.utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class AimAssistant:
    """Main aim-assist orchestrator - production ready"""

    def __init__(self, config: Dict):
        self.config = config
        self.is_running = False
        self.is_aiming = False
        self.pause_requested = False

        logger.info("Initializing Nexus components...")

        # Initialize components with error handling
        try:
            self.memory_reader = AssaultCubeMemoryReader()
            logger.info("✓ Memory reader initialized")
        except Exception as e:
            logger.warning(f"Memory reader init failed: {e}")
            self.memory_reader = None

        try:
            self.physics_engine = PhysicsEngine()
            logger.info("✓ Physics engine initialized")
        except Exception as e:
            logger.error(f"Physics engine init failed: {e}")
            self.physics_engine = None

        try:
            self.detector = EnsembleDetector(
                confidence_threshold=config.get("target_detection", {}).get("confidence_threshold", 0.45)
            )
            logger.info("✓ Detection engine initialized")
        except Exception as e:
            logger.error(f"Detection engine init failed: {e}")
            self.detector = None

        try:
            self.aim_intelligence = AimIntelligence()
            logger.info("✓ Aim intelligence initialized")
        except Exception as e:
            logger.error(f"Aim intelligence init failed: {e}")
            self.aim_intelligence = None

        try:
            self.frame_processor = FrameProcessor()
            logger.info("✓ Frame processor initialized")
        except Exception as e:
            logger.error(f"Frame processor init failed: {e}")
            self.frame_processor = None

        try:
            self.overlay_renderer = OverlayRenderer()
            logger.info("✓ Overlay renderer initialized")
        except Exception as e:
            logger.error(f"Overlay renderer init failed: {e}")
            self.overlay_renderer = None

        try:
            self.input_controller = InputController()
            logger.info("✓ Input controller initialized")
        except Exception as e:
            logger.error(f"Input controller init failed: {e}")
            self.input_controller = None

        # Stats
        self.stats = {
            "fps": 0.0,
            "detections": 0,
            "inference_time": 0.0,
            "aim_active": False,
            "targets": 0,
            "memory_mode": False
        }

    def start(self):
        """Start aim-assist system"""
        logger.info("="*60)
        logger.info("Starting Nexus Aim-Assist System")
        logger.info("="*60)

        self.is_running = True

        # Try to connect to game memory
        if self.memory_reader:
            try:
                if self.memory_reader.connect():
                    self.stats["memory_mode"] = True
                    logger.info("✓ Connected to game memory (enhanced mode)")
                else:
                    logger.info("Running in vision-only mode")
            except Exception as e:
                logger.warning(f"Memory connection failed: {e}")

        # Start main loop in thread
        main_thread = threading.Thread(target=self._main_loop, daemon=True)
        main_thread.start()

        logger.info("")
        logger.info("Nexus started successfully!")
        logger.info("")
        logger.info("Controls:")
        logger.info("  SPACE - Toggle aim assist on/off")
        logger.info("  Q     - Quit")
        logger.info("="*60)

    def _main_loop(self):
        """Main aim-assist loop"""
        while self.is_running:
            try:
                # Capture frame
                if not self.frame_processor:
                    time.sleep(0.01)
                    continue

                frame = self.frame_processor.capture_frame()
                if frame is None:
                    time.sleep(0.01)
                    continue

                # Run detection
                detections = []
                if self.detector:
                    try:
                        detections = self.detector.detect(frame)
                    except Exception as e:
                        logger.debug(f"Detection error: {e}")

                # Get game state
                game_state = self._get_game_state()

                # Process detections
                if detections and self.is_aiming:
                    try:
                        best_target = self._select_best_target(detections, game_state)
                        if best_target:
                            self._aim_at_target(best_target, frame, game_state)
                    except Exception as e:
                        logger.debug(f"Aiming error: {e}")

                # Update stats
                if self.frame_processor:
                    self.stats["fps"] = self.frame_processor.get_fps()
                if self.detector:
                    self.stats["inference_time"] = self.detector.get_average_inference_time()
                self.stats["detections"] = len(detections)
                self.stats["targets"] = len(detections)
                self.stats["aim_active"] = self.is_aiming

                # Render overlay
                try:
                    if self.overlay_renderer and self.detector:
                        head_positions = self.detector.detect_heads(frame, detections)
                        overlay_frame = self.overlay_renderer.render(
                            frame,
                            detections,
                            head_positions,
                            self.stats,
                            show_boxes=True,
                            show_heads=True,
                            show_stats=True
                        )

                        if cv2 and overlay_frame is not None:
                            cv2.imshow("Nexus Aim-Assist", overlay_frame)
                except Exception as e:
                    logger.debug(f"Overlay error: {e}")

                # Handle input
                if cv2:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q') or key == 27:  # Q or ESC
                        self.stop()
                    elif key == ord(' '):  # Space
                        self.is_aiming = not self.is_aiming
                        status = "ON" if self.is_aiming else "OFF"
                        logger.info(f"Aim assist turned {status}")

                # Check keyboard for space (alternative input method)
                if self.input_controller:
                    if self.input_controller.is_key_pressed('space'):
                        if not self.pause_requested:
                            self.is_aiming = not self.is_aiming
                            self.pause_requested = True
                            time.sleep(0.2)  # Debounce
                    else:
                        self.pause_requested = False

                # Maintain target FPS
                if self.frame_processor:
                    self.frame_processor.wait_frame_time()

            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                logger.debug(f"Loop error: {e}")
                time.sleep(0.01)

    def _get_game_state(self) -> Dict:
        """Get current game state from memory"""
        state = {
            "player_health": 100,
            "nearby_enemies": 1,
            "shots_fired": 0
        }

        if self.memory_reader and self.memory_reader.is_connected:
            try:
                local_player = self.memory_reader.get_local_player()
                if local_player:
                    state["player_health"] = local_player.health
                    state["player_pos"] = local_player.position
            except Exception as e:
                logger.debug(f"Memory read error: {e}")

        return state

    def _select_best_target(self, detections: List, game_state: Dict) -> Optional:
        """Select best target from detections"""
        if not detections:
            return None

        # Prefer head detections
        head_dets = [d for d in detections if "head" in d.class_name.lower()]
        candidates = head_dets if head_dets else detections

        if not candidates:
            return None

        # Sort by confidence
        candidates.sort(key=lambda d: d.confidence, reverse=True)
        return candidates[0]

    def _aim_at_target(self, detection, frame, game_state):
        """Aim at target with smoothing"""
        try:
            if not self.input_controller:
                return

            frame_h, frame_w = frame.shape[:2]
            frame_center = np.array([frame_w / 2, frame_h / 2])

            # Calculate delta
            target_pos = np.array([detection.x, detection.y])
            delta = target_pos - frame_center
            distance = np.linalg.norm(delta)

            if distance < 1:
                return

            # Apply smoothing
            smoothing = self.config.get("aiming", {}).get("smoothing", 0.7)
            sensitivity = self.config.get("aim_assist", {}).get("sensitivity", 1.2)

            # Scale movement
            movement = delta * sensitivity * (1 - smoothing) * 0.01

            # Move mouse with smooth easing
            if np.linalg.norm(movement) > 0.1:
                self.input_controller.move_mouse_smooth(
                    movement[0],
                    movement[1],
                    duration=0.01,
                    easing="cubic"
                )
        except Exception as e:
            logger.debug(f"Aim error: {e}")

    def stop(self):
        """Stop aim-assist system"""
        logger.info("")
        logger.info("Stopping Nexus Aim-Assist...")
        self.is_running = False

        if self.memory_reader:
            try:
                self.memory_reader.disconnect()
            except:
                pass

        if cv2:
            try:
                cv2.destroyAllWindows()
            except:
                pass

        logger.info("Nexus stopped")
        logger.info("="*60)
