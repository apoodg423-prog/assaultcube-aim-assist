from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QApplication, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QSize

from ui.pages.dashboard import DashboardPage
from ui.pages.game_library import GameLibraryPage
from ui.pages.features import FeaturesPage
from ui.pages.profiles import ProfilesPage
from ui.pages.settings import SettingsPage
from ui.pages.performance import PerformancePage
from ui.pages.logs import LogsPage
from ui.pages.license_page import LicensePage
from ui.pages.about import AboutPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ipro71 Nexus")
        self.resize(1200, 800)
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        h = QHBoxLayout(central)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        for name in ["Dashboard","Game Library","Profiles","Features","Settings","Performance","Logs","License","About"]:
            item = QListWidgetItem(name)
            item.setSizeHint(QSize(200, 40))
            self.sidebar.addItem(item)

        # Stack
        self.stack = QStackedWidget()
        self.pages = {
            0: DashboardPage(),
            1: GameLibraryPage(),
            2: ProfilesPage(),
            3: FeaturesPage(),
            4: SettingsPage(),
            5: PerformancePage(),
            6: LogsPage(),
            7: LicensePage(),
            8: AboutPage(),
        }

        for i in range(len(self.pages)):
            self.stack.addWidget(self.pages[i])

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        h.addWidget(self.sidebar)
        h.addWidget(self.stack, 1)

        self.setCentralWidget(central)


def start_gui():
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
