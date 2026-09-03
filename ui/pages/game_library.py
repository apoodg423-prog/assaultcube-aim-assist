from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QFileDialog, QInputDialog, QMessageBox
from PySide6.QtCore import Qt
from core.app_controller import get_controller
from app.services.game_service import GameService

class GameLibraryPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.reload_games()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Game Library")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        hl = QHBoxLayout()
        self.add_btn = QPushButton("Add Game")
        self.edit_btn = QPushButton("Edit Selected")
        self.delete_btn = QPushButton("Delete Selected")
        self.add_btn.clicked.connect(self.add_game)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.edit_btn.clicked.connect(self.edit_selected)

        hl.addWidget(self.add_btn)
        hl.addWidget(self.edit_btn)
        hl.addWidget(self.delete_btn)
        layout.addLayout(hl)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        layout.addStretch()

    def reload_games(self):
        self.list_widget.clear()
        games = GameService.list_games()
        for g in games:
            item = f"{g.id}: {g.name} [{g.exe_path or 'no exe'}]"
            self.list_widget.addItem(item)

    def add_game(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Game Executable")
        if not path:
            return
        name, ok = QInputDialog.getText(self, "Game Name", "Enter game name:")
        if not ok or not name:
            QMessageBox.warning(self, "Missing name", "Game name is required")
            return
        GameService.add_game(name=name, exe_path=path)
        self.reload_games()

    def delete_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        game_id = int(item.text().split(":")[0])
        if QMessageBox.question(self, "Delete", "Delete selected game?") == QMessageBox.Yes:
            GameService.delete_game(game_id)
            self.reload_games()

    def edit_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        game_id = int(item.text().split(":")[0])
        # Very simple edit: change name
        name, ok = QInputDialog.getText(self, "Edit Name", "New name:")
        if not ok or not name:
            return
        # Direct DB update
        from database.db import SessionLocal
        db = SessionLocal()
        try:
            g = db.query(__import__('database.models', fromlist=['Game']).Game).filter_by(id=game_id).first()
            if g:
                g.name = name
                db.add(g)
                db.commit()
        finally:
            db.close()
        self.reload_games()
