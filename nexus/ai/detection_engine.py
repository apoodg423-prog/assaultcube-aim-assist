"""Advanced Multi-Model Detection Engine with Ensemble Learning"""

import logging
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from ultralytics import YOLO
    import torch
except ImportError:
    YOLO = None
    torch = None

logger = logging.getLogger(__name__)


@dataclass
class Detection:
    """Single detection result"""
    x: float
    y: float
    w: float
    h: float
    confidence: float
    class_id: int
    class_name: str
    model_id: int
    keypoints: Optional[np.ndarray] = None


class EnsembleDetector:
    """Ensemble of multiple YOLO models for robust detection"""

    def __init__(
        self,
        model_configs: List[Dict] = None,
        confidence_threshold: float = 0.45,
        nms_threshold: float = 0.45,
        device: str = "cuda" if torch and torch.cuda.is_available() else "cpu"
    ):
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.device = device
        self.models = []
        self.model_weights = []
        self.detection_history = {}
        self.inference_times = []
        self.yolo_available = YOLO is not None

        if not self.yolo_available:
            logger.warning("YOLOv8 not available - detection will be limited")

        if model_configs is None:
            model_configs = [
                {"name": "yolov8n", "weight": 1.0},
            ]

        self._load_models(model_configs)

    def _load_models(self, model_configs: List[Dict]):
        """Load multiple YOLO models"""
        if not self.yolo_available:
            logger.warning("Skipping model loading - YOLO not available")
            return

        for config in model_configs:
            try:
                model_name = config.get("name", "yolov8n")
                weight = config.get("weight", 1.0)

                logger.info(f"Loading model: {model_name}")
                model = YOLO(f"{model_name}.pt")
                model.to(self.device)

                self.models.append(model)
                self.model_weights.append(weight)
                logger.info(f"Successfully loaded {model_name}")
            except Exception as e:
                logger.warning(f"Failed to load model {config}: {e}")

        if not self.models:
            logger.warning("No detection models loaded")

    def detect(
        self,
        frame: np.ndarray,
        confidence_threshold: Optional[float] = None
    ) -> List[Detection]:
        """Run ensemble detection on frame"""
        threshold = confidence_threshold or self.confidence_threshold
        all_detections = []
        inference_start = time.time()

        if not self.models:
            self.inference_times.append(time.time() - inference_start)
            return []

        for model_idx, model in enumerate(self.models):
            try:
                results = model(frame, conf=threshold, verbose=False)

                for result in results:
                    if hasattr(result, 'boxes') and result.boxes is not None:
                        boxes = result.boxes
                        for i, box in enumerate(boxes):
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            conf = box.conf[0].cpu().item()
                            cls_id = int(box.cls[0].cpu().item())

                            w = x2 - x1
                            h = y2 - y1
                            x = x1 + w / 2
                            y = y1 + h / 2

                            keypoints = None
                            if hasattr(result, 'keypoints') and result.keypoints is not None:
                                try:
                                    keypoints = result.keypoints[i].cpu().numpy()
                                except:
                                    pass

                            detection = Detection(
                                x=x,
                                y=y,
                                w=w,
                                h=h,
                                confidence=conf,
                                class_id=cls_id,
                                class_name=result.names.get(cls_id, "unknown") if hasattr(result, 'names') else "person",
                                model_id=model_idx,
                                keypoints=keypoints
                            )
                            all_detections.append(detection)
            except Exception as e:
                logger.debug(f"Error in model {model_idx}: {e}")

        inference_time = time.time() - inference_start
        self.inference_times.append(inference_time)
        if len(self.inference_times) > 100:
            self.inference_times.pop(0)

        merged_detections = self._ensemble_merge(all_detections)
        return merged_detections

    def _ensemble_merge(self, detections: List[Detection]) -> List[Detection]:
        """Merge detections from multiple models"""
        if not detections:
            return []

        clusters = self._cluster_detections(detections, iou_threshold=0.3)
        merged = []

        for cluster in clusters:
            if not cluster:
                continue

            weights = [self.model_weights[d.model_id] for d in cluster]
            confidences = [d.confidence * w for d, w in zip(cluster, weights)]
            avg_confidence = sum(confidences) / sum(weights) if sum(weights) > 0 else 0

            avg_x = sum(d.x * w for d, w in zip(cluster, weights)) / sum(weights)
            avg_y = sum(d.y * w for d, w in zip(cluster, weights)) / sum(weights)
            avg_w = sum(d.w * w for d, w in zip(cluster, weights)) / sum(weights)
            avg_h = sum(d.h * w for d, w in zip(cluster, weights)) / sum(weights)

            merged_detection = Detection(
                x=avg_x,
                y=avg_y,
                w=avg_w,
                h=avg_h,
                confidence=avg_confidence,
                class_id=cluster[0].class_id,
                class_name=cluster[0].class_name,
                model_id=-1,
                keypoints=cluster[0].keypoints
            )
            merged.append(merged_detection)

        return merged

    def _cluster_detections(
        self,
        detections: List[Detection],
        iou_threshold: float = 0.3
    ) -> List[List[Detection]]:
        """Cluster detections using IoU"""
        if not detections:
            return []

        clusters = []
        used = set()

        for i, det in enumerate(detections):
            if i in used:
                continue

            cluster = [det]
            used.add(i)

            for j, other_det in enumerate(detections[i+1:], start=i+1):
                if j in used:
                    continue

                iou = self._calculate_iou(det, other_det)
                if iou > iou_threshold:
                    cluster.append(other_det)
                    used.add(j)

            clusters.append(cluster)

        return clusters

    def _calculate_iou(self, det1: Detection, det2: Detection) -> float:
        """Calculate Intersection over Union"""
        x1_min, y1_min = det1.x - det1.w/2, det1.y - det1.h/2
        x1_max, y1_max = det1.x + det1.w/2, det1.y + det1.h/2
        x2_min, y2_min = det2.x - det2.w/2, det2.y - det2.h/2
        x2_max, y2_max = det2.x + det2.w/2, det2.y + det2.h/2

        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)
        area1 = det1.w * det1.h
        area2 = det2.w * det2.h
        union_area = area1 + area2 - inter_area

        return inter_area / (union_area + 1e-6)

    def get_average_inference_time(self) -> float:
        """Get average inference time in milliseconds"""
        if not self.inference_times:
            return 0
        return np.mean(self.inference_times) * 1000

    def detect_heads(
        self,
        frame: np.ndarray,
        detections: List[Detection]
    ) -> Dict[int, Tuple[float, float]]:
        """Extract head positions from detections"""
        head_positions = {}

        for i, det in enumerate(detections):
            if det.keypoints is not None:
                try:
                    head_kp = det.keypoints[0]
                    if len(head_kp) >= 2:
                        head_positions[i] = (float(head_kp[0]), float(head_kp[1]))
                    else:
                        head_y = det.y - det.h / 3
                        head_positions[i] = (det.x, head_y)
                except:
                    head_y = det.y - det.h / 3
                    head_positions[i] = (det.x, head_y)
            else:
                head_y = det.y - det.h / 3
                head_positions[i] = (det.x, head_y)

        return head_positions
