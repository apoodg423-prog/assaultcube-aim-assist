from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
import psutil

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        # System status cards
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        except Exception:
            gpu_util = None

        layout.addWidget(QLabel(f"CPU Usage: {cpu}%"))
        layout.addWidget(QLabel(f"RAM Usage: {mem}%"))
        layout.addWidget(QLabel(f"GPU Usage: {gpu_util if gpu_util is not None else 'N/A'}"))

        # Placeholders for other stats
        layout.addWidget(QLabel("Selected Game: Not Selected"))
        layout.addWidget(QLabel("Current Profile: None"))
        layout.addWidget(QLabel("FPS: Not Measured"))
        layout.addStretch()
