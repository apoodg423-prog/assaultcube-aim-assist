from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Settings")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        layout.addWidget(QLabel("General / Appearance / Performance / Detection / Input / Notifications / Advanced"))
        layout.addWidget(QPushButton("Save"))
        layout.addWidget(QPushButton("Reset to Defaults"))
        layout.addStretch()
