from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ProfilesPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Profiles")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Profile management: Not Implemented (DB-backed profiles will appear here)"))
        layout.addStretch()
