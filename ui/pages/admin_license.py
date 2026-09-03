from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QComboBox, QFileDialog, QMessageBox
from licensing.license_manager import AdminLicenseManager

class AdminLicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin License Manager")
        self.resize(600, 400)
        self._init_ui()
        self.reload()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        hl = QHBoxLayout()
        self.license_type = QComboBox()
        self.license_type.addItems(['1 Month', '6 Months', 'Lifetime'])
        self.gen_btn = QPushButton('Generate')
        self.gen_btn.clicked.connect(self.generate)
        hl.addWidget(self.license_type)
        hl.addWidget(self.gen_btn)
        layout.addLayout(hl)

        self.list_widget = QListWidget()
        layout.addWidget(QLabel('Recently Generated'))
        layout.addWidget(self.list_widget)

        hl2 = QHBoxLayout()
        self.copy_btn = QPushButton('Copy Key')
        self.export_btn = QPushButton('Export Keys')
        self.revoke_btn = QPushButton('Revoke')
        self.copy_btn.clicked.connect(self.copy_key)
        self.export_btn.clicked.connect(self.export_keys)
        self.revoke_btn.clicked.connect(self.revoke_key)
        hl2.addWidget(self.copy_btn)
        hl2.addWidget(self.export_btn)
        hl2.addWidget(self.revoke_btn)
        layout.addLayout(hl2)

    def reload(self):
        self.list_widget.clear()
        licenses = AdminLicenseManager.list_licenses()
        for l in licenses[:50]:
            self.list_widget.addItem(f"{l.id}: {l.key} ({l.license_type}) {l.status}")

    def generate(self):
        lt = self.license_type.currentText()
        lic = AdminLicenseManager.create_license(lt)
        QMessageBox.information(self, 'Generated', f'Key: {lic.key}')
        self.reload()

    def copy_key(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        key = item.text().split(':')[1].strip().split(' ')[0]
        QApplication = __import__('PySide6.QtWidgets', fromlist=['QApplication']).QApplication
        QApplication.clipboard().setText(key)

    def export_keys(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Export Keys', filter='CSV Files (*.csv)')
        if not path:
            return
        licenses = AdminLicenseManager.list_licenses()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('id,key,license_type,status,created_at,expires_at\n')
                for l in licenses:
                    f.write(f"{l.id},{l.key},{l.license_type},{l.status},{l.created_at},{l.expires_at}\n")
            QMessageBox.information(self, 'Exported', f'Exported {len(licenses)} keys')
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

    def revoke_key(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        lid = int(item.text().split(':')[0])
        db = __import__('database.db', fromlist=['SessionLocal']).SessionLocal()
        try:
            lic = db.query(__import__('database.models', fromlist=['License']).License).filter_by(id=lid).first()
            if lic:
                lic.status = 'REVOKED'
                db.add(lic)
                db.commit()
        finally:
            db.close()
        self.reload()
