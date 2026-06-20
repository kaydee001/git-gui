import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout, QMessageBox, QTextEdit


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        self.resize(500, 500)

        self.button = QPushButton("select folder")
        self.label = QLabel("no folder selected")

        self.status_box = QTextEdit()

        self.button.clicked.connect(self.open_folder_dialog)
        self.status_box.setReadOnly(True)

        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.status_box)

        self.setLayout(layout)

    def is_git_repo(self):
        selected_path = os.path.join(self.selected_path, ".git")
        if os.path.exists(selected_path):
            return True
        return False

    def run_git_status(self):
        result = subprocess.run(
            ["git", "status"], cwd=self.selected_path, capture_output=True, text=True)
        self.status_box.setText(result.stdout)

    def open_folder_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "select folder")
        self.selected_path = path
        self.label.setText(path)

        is_repo = self.is_git_repo()
        if not is_repo:
            QMessageBox.warning(self, "error", "not a repo")

        self.run_git_status()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
