from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class FeaturesPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Features")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        # Feature cards - show Not Implemented if backend missing
        features = [
            'Aimbot','No Recoil','No Spread','ESP','Wallhack','Triggerbot','FOV','Aim Smoothing','Bone Selection','Target Selection','Prediction','Distance Settings'
        ]

        for f in features:
            lbl = QLabel(f"{f}: Not Implemented")
            layout.addWidget(lbl)

        layout.addStretch()
