import sys
import os
from pathlib import Path
import configparser

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QListWidget
)

class MimeChanger(QWidget):
    def __init__(self):
        super().__init__()
        self.mimeapps_path = Path.home() / '.config' / 'mimeapps.list'
        self.config = configparser.ConfigParser(strict=False, delimiters=('='))

        self.init_ui()
        self.load_mimeapps()

    def init_ui(self):
        self.setWindowTitle('MIME Type Changer')

        # Left: MIME list
        self.mime_list = QListWidget()
        self.mime_list.itemClicked.connect(self.load_selected_mime)

        # Right: MIME editor
        self.mime_label = QLabel('MIME Type:')
        self.mime_input = QLineEdit()

        self.desktop_label = QLabel('.desktop file:')
        self.desktop_input = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_desktop_file)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.set_default_app)

        editor_layout = QVBoxLayout()
        editor_layout.addWidget(self.mime_label)
        editor_layout.addWidget(self.mime_input)
        editor_layout.addWidget(self.desktop_label)
        editor_layout.addWidget(self.desktop_input)
        editor_layout.addWidget(self.browse_button)
        editor_layout.addWidget(self.save_button)

        # Horizontal split: list on left, editor on right
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.mime_list, 1)
        main_layout.addLayout(editor_layout, 2)

        self.setLayout(main_layout)
        self.resize(600, 400)

    def load_mimeapps(self):
        if self.mimeapps_path.exists():
            self.config.read(self.mimeapps_path)
        if 'Default Applications' not in self.config:
            self.config['Default Applications'] = {}

        self.mime_list.clear()
        for mime, app in self.config['Default Applications'].items():
            self.mime_list.addItem(f"{mime} = {app}")

    def load_selected_mime(self, item):
        line = item.text()
        if '=' in line:
            mime, desktop = map(str.strip, line.split('=', 1))
            self.mime_input.setText(mime)
            self.desktop_input.setText(desktop)

    def browse_desktop_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select .desktop file", "/usr/share/applications", "Desktop files (*.desktop)"
        )
        if file_path:
            self.desktop_input.setText(os.path.basename(file_path))

    def set_default_app(self):
        mime_type = self.mime_input.text().strip()
        desktop_file = self.desktop_input.text().strip()

        if not mime_type or not desktop_file:
            QMessageBox.warning(self, "Missing info", "Please fill both MIME type and .desktop file.")
            return

        self.config['Default Applications'][mime_type] = desktop_file
        with open(self.mimeapps_path, 'w') as f:
            self.config.write(f, space_around_delimiters=False)

        QMessageBox.information(self, "Saved", f"Updated {mime_type} = {desktop_file}")
        self.load_mimeapps()  # Refresh list

def main():
    app = QApplication(sys.argv)
    window = MimeChanger()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
