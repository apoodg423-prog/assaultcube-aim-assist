from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QFileDialog, QLineEdit
from PySide6.QtCore import Qt

class GameLibraryPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Game Library")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        hl = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search games...")
        self.add_btn = QPushButton("Add Game")
        self.add_btn.clicked.connect(self.add_game)
        hl.addWidget(self.search)
        hl.addWidget(self.add_btn)

        layout.addLayout(hl)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Initially empty - Game adapters will populate
        layout.addStretch()

    def add_game(self):
        name, _ = QFileDialog.getOpenFileName(self, "Select Game Executable")
        if name:
            # For now, add entry to list - actual DB save implemented later
            self.list_widget.addItem(name)
