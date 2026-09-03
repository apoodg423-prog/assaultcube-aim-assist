from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
from licensing.license_manager import LicenseManager, LicenseValidator, AdminLicenseManager

class LicensePage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("License")
        title.setStyleSheet("font-size:18px;font-weight:600;")
        layout.addWidget(title)

        hl = QHBoxLayout()
        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText("Enter license key...")
        self.activate_btn = QPushButton("Activate")
        self.activate_btn.clicked.connect(self.activate_key)
        self.admin_btn = QPushButton("Admin Manager")
        self.admin_btn.clicked.connect(self.open_admin)
        hl.addWidget(self.input_key)
        hl.addWidget(self.activate_btn)
        hl.addWidget(self.admin_btn)
        layout.addLayout(hl)

        self.status_lbl = QLabel("Status: Not Activated")
        layout.addWidget(self.status_lbl)
        layout.addStretch()

    def activate_key(self):
        key = self.input_key.text().strip()
        if not key:
            QMessageBox.warning(self, "Input required", "Enter a license key")
            return
        res = LicenseManager.activate(key)
        if res.get('status') == 'ACTIVE':
            self.status_lbl.setText(f"Status: ACTIVE (expires: {res.get('expires_at')})")
        else:
            self.status_lbl.setText(f"Status: {res.get('status')}")

    def open_admin(self):
        from ui.pages.admin_license import AdminLicenseDialog
        dlg = AdminLicenseDialog(self)
        dlg.exec()
