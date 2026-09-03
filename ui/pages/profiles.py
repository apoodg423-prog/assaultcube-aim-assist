from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QInputDialog, QMessageBox
from app.services.game_service import GameService
import json

class ProfilesPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.reload()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Profiles")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        self.game_list = QListWidget()
        self.profile_list = QListWidget()

        hl = QHBoxLayout()
        self.create_btn = QPushButton("Create Profile")
        self.delete_btn = QPushButton("Delete Profile")
        self.create_btn.clicked.connect(self.create_profile)
        self.delete_btn.clicked.connect(self.delete_profile)

        hl.addWidget(self.create_btn)
        hl.addWidget(self.delete_btn)

        layout.addWidget(QLabel("Games"))
        layout.addWidget(self.game_list)
        layout.addWidget(QLabel("Profiles"))
        layout.addWidget(self.profile_list)
        layout.addLayout(hl)

        self.game_list.currentItemChanged.connect(self.on_game_selected)

    def reload(self):
        self.game_list.clear()
        games = GameService.list_games()
        for g in games:
            self.game_list.addItem(f"{g.id}: {g.name}")

    def on_game_selected(self, current, previous=None):
        self.profile_list.clear()
        if not current:
            return
        game_id = int(current.text().split(":")[0])
        profiles = GameService.list_profiles(game_id)
        for p in profiles:
            self.profile_list.addItem(f"{p.id}: {p.name}")

    def create_profile(self):
        g_item = self.game_list.currentItem()
        if not g_item:
            QMessageBox.warning(self, "No game", "Select a game first")
            return
        game_id = int(g_item.text().split(":")[0])
        name, ok = QInputDialog.getText(self, "Profile Name", "Enter profile name:")
        if not ok or not name:
            return
        # default data placeholder
        data = {"aiming": {"sensitivity": 1.2, "smoothing": 0.7}}
        GameService.add_profile(game_id, name, data)
        self.on_game_selected(g_item)

    def delete_profile(self):
        item = self.profile_list.currentItem()
        if not item:
            return
        pid = int(item.text().split(":")[0])
        if QMessageBox.question(self, "Delete", "Delete profile?") == QMessageBox.Yes:
            GameService.delete_profile(pid)
            # refresh
            g_item = self.game_list.currentItem()
            if g_item:
                self.on_game_selected(g_item)
