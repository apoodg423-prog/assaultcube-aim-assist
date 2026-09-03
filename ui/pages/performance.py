from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PerformancePage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Performance Monitor")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        layout.addWidget(QLabel("FPS: Not Implemented"))
        layout.addWidget(QLabel("CPU: Not Implemented"))
        layout.addWidget(QLabel("GPU: Not Implemented"))
        layout.addWidget(QLabel("RAM: Not Implemented"))
        layout.addWidget(QLabel("Detection Time: Not Implemented"))
        layout.addStretch()
