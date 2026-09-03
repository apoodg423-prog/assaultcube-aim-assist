from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer

class Notifier:
    """Simple in-app notification manager (non-blocking)"""
    def __init__(self, parent):
        self.parent = parent
        self.label = QLabel(parent)
        self.label.setStyleSheet('background: rgba(0,0,0,0.7); color: white; padding: 6px; border-radius: 4px;')
        self.label.hide()
        self.timer = QTimer()
        self.timer.timeout.connect(self._hide)

    def notify(self, text: str, duration_ms: int = 3000):
        self.label.setText(text)
        self.label.adjustSize()
        self.label.move(20, 20)
        self.label.show()
        self.timer.start(duration_ms)

    def _hide(self):
        self.timer.stop()
        self.label.hide()
