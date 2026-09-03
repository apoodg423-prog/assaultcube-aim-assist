from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("About Ipro71 Nexus")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Version: 1.0.0"))
        layout.addWidget(QLabel("Built on top of existing assaultcube-aim-assist project"))
        layout.addStretch()
