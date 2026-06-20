import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox, QTextEdit, QLineEdit


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        self.resize(800, 600)

        self.button = QPushButton("select folder")
        self.folder_label = QLabel("no folder selected")
        self.stage_button = QPushButton("stage all")
        self.commit_msg_label = QLabel("commit msg")
        self.commit_input = QLineEdit()
        self.commit_button = QPushButton("commit")
        self.push_button = QPushButton("push")

        self.status_box = QTextEdit()

        self.button.clicked.connect(self.open_folder_dialog)
        self.status_box.setReadOnly(True)

        self.stage_button.clicked.connect(self.run_git_add)
        self.commit_button.clicked.connect(self.run_git_commit)
        self.push_button.clicked.connect(self.run_git_push)

        row1 = QHBoxLayout()
        row1.addWidget(self.button)
        row1.addWidget(self.folder_label)

        row2 = QVBoxLayout()
        row2.addWidget(self.stage_button)

        row3 = QVBoxLayout()
        row3.addWidget(self.commit_msg_label)

        row4 = QVBoxLayout()
        row4.addWidget(self.commit_input)

        row5 = QHBoxLayout()
        row5.addWidget(self.commit_button)
        row5.addWidget(self.push_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(row1)
        main_layout.addWidget(self.status_box)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)
        main_layout.addLayout(row5)

        self.setLayout(main_layout)

    def is_git_repo(self):
        selected_path = os.path.join(self.selected_path, ".git")
        if os.path.exists(selected_path):
            return True
        return False

    def run_git_status(self):
        result = subprocess.run(
            ["git", "status"], cwd=self.selected_path, capture_output=True, text=True)
        self.status_box.setText(result.stdout)

    def run_git_add(self):
        result = subprocess.run(["git", "add", "."], cwd=self.selected_path)
        self.run_git_status()

    def run_git_commit(self):
        msg = self.commit_input.text()
        if not msg:
            QMessageBox.warning(self, "error", "no commit msg found")
        else:
            result = subprocess.run(
                ["git", "commit", "-m", f"{msg}"], cwd=self.selected_path)
            self.commit_input.clear()
            self.run_git_status()

    def run_git_push(self):
        result = subprocess.run(
            ["git", "push"], cwd=self.selected_path, capture_output=True, text=True)
        if result.returncode:
            QMessageBox.warning(self, "push failed", result.stderr)
        else:
            self.run_git_status()

    def open_folder_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "select folder")
        self.selected_path = path
        self.folder_label.setText(path)

        is_repo = self.is_git_repo()
        if not is_repo:
            QMessageBox.warning(self, "error", "not a repo")
        else:
            self.run_git_status()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
