from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from licensing.license_manager import LicenseManager

class LicensePage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("License")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Status: Not Activated"))
        layout.addWidget(QLabel("Type: N/A"))
        layout.addWidget(QLabel("Activation Date: N/A"))
        layout.addWidget(QLabel("Expiration Date: N/A"))
        layout.addWidget(QLabel("Days Remaining: N/A"))
        layout.addWidget(QLabel("License Key: ****-****-****-****"))
        layout.addWidget(QPushButton("Activate (Not Implemented)"))
        layout.addStretch()
