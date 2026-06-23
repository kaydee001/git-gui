import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox, QTextEdit, QLineEdit, QListWidget, QComboBox
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git GUI")
        self.resize(800, 600)

        self.folder_button = QPushButton("select folder")
        self.folder_label = QLabel("no folder selected")
        self.status_box = QTextEdit()
        self.stage_button = QPushButton("stage all")
        self.commit_input = QLineEdit()
        self.commit_button = QPushButton("commit")
        self.push_button = QPushButton("push")
        self.log_button = QPushButton("view commit log")
        self.commit_log = QListWidget()
        self.unstage_button = QPushButton("unstage")
        self.status_label = QLabel("-")
        self.branch_dropdown = QComboBox()

        self.folder_button.clicked.connect(self.open_folder_dialog)
        self.status_box.setReadOnly(True)

        self.status_label.setObjectName("statusLabel")

        self.folder_button.setFixedWidth(180)
        self.stage_button.setFixedWidth(180)
        self.unstage_button.setFixedWidth(180)

        self.commit_button.setFixedWidth(180)
        self.push_button.setFixedWidth(180)

        self.log_button.setFixedWidth(180)

        self.commit_input.setPlaceholderText("enter commit msg")

        self.stage_button.clicked.connect(self.run_git_add)
        self.commit_button.clicked.connect(self.run_git_commit)
        self.push_button.clicked.connect(self.run_git_push)
        self.log_button.clicked.connect(self.run_git_log)
        self.unstage_button.clicked.connect(self.run_git_unstage)
        self.branch_dropdown.currentTextChanged.connect(self.switch_branch)

        row1 = QHBoxLayout()
        row1.addWidget(self.folder_button)
        row1.addSpacing(15)
        row1.addWidget(self.folder_label)
        row1.addStretch()
        row1.addWidget(self.status_label)
        row1.addSpacing(15)
        row1.addWidget(self.branch_dropdown)

        row2 = QHBoxLayout()
        row2.addStretch()
        row2.addWidget(self.stage_button)
        row2.addStretch()
        row2.addWidget(self.unstage_button)
        row2.addStretch()

        row3 = QHBoxLayout()
        row3.addStretch()
        row3.addWidget(self.commit_button)
        row3.addStretch()
        row3.addWidget(self.push_button)
        row3.addStretch()
        row3.addWidget(self.log_button)
        row3.addStretch()

        row4 = QHBoxLayout()
        row4.addWidget(self.commit_log)

        main_layout = QVBoxLayout()
        row1.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(row1)
        main_layout.addWidget(self.status_box)
        main_layout.addLayout(row2)
        main_layout.addWidget(self.commit_input)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Segoe UI;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QLineEdit, QTextEdit, QListWidget, QComboBox {
                background-color: #252526;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px;
            }
            QLabel#statusLabel {
                font-weight: bold;
            }
        """)

    def is_git_repo(self):
        selected_path = os.path.join(self.selected_path, ".git")
        if os.path.exists(selected_path):
            return True
        return False

    def run_git_status(self):
        self.run_git_branch()

        result = subprocess.run(
            ["git", "status"], cwd=self.selected_path, capture_output=True, text=True)
        self.status_label.setText(result.stdout)

        if "nothing to commit, working tree clean" in result.stdout:
            self.status_label.setText("clean")
            self.status_label.setStyleSheet("color: #11b918;")
        elif "Changes to be committed" in result.stdout:
            self.status_label.setText("staged")
            self.status_label.setStyleSheet("color: #efef3c;")
        elif "Changes not staged" in result.stdout:
            self.status_label.setText("unstaged")
            self.status_label.setStyleSheet("color: #ef4624;")

        self.branch_dropdown.currentTextChanged.disconnect(self.switch_branch)
        self.branch_dropdown.clear()
        self.branch_dropdown.addItems(self.branch_names)
        self.branch_dropdown.setCurrentText(self.current_branch)
        self.branch_dropdown.currentTextChanged.connect(self.switch_branch)

        self.status_box.setText(result.stdout)

    def run_git_add(self):
        result = subprocess.run(
            ["git", "add", "."], cwd=self.selected_path, capture_output=True, text=True)
        self.run_git_status()

    def run_git_commit(self):
        msg = self.commit_input.text()
        if not msg:
            QMessageBox.warning(self, "error", "no commit msg found")
        else:
            result = subprocess.run(
                ["git", "commit", "-m", f"{msg}"], cwd=self.selected_path, capture_output=True, text=True)
            self.commit_input.clear()
            self.run_git_status()

    def run_git_push(self):
        result = subprocess.run(
            ["git", "push"], cwd=self.selected_path, capture_output=True, text=True)
        if result.returncode:
            QMessageBox.warning(self, "push failed", result.stderr)
        else:
            self.run_git_status()

    def run_git_log(self):
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"], cwd=self.selected_path, capture_output=True, text=True)
        self.commit_log.clear()
        lines = result.stdout.splitlines()
        for line in lines:
            self.commit_log.addItem(line)

    def run_git_unstage(self):
        result = subprocess.run(
            ["git", "reset"], cwd=self.selected_path, capture_output=True, text=True)
        self.run_git_status()

    def switch_branch(self, branch_name):
        result = subprocess.run(
            ["git", "checkout", f"{branch_name}"], cwd=self.selected_path, capture_output=True, text=True)
        if result.returncode:
            QMessageBox.warning(self, "branching failed", result.stderr)
        else:
            self.run_git_status()

    def run_git_branch(self):
        result = subprocess.run(
            ["git", "branch"], cwd=self.selected_path, capture_output=True, text=True)
        self.branch_names = []
        lines = result.stdout.splitlines()
        self.current_branch = ""
        for line in lines:
            if line.startswith("*"):
                line = line.replace("*", "").strip()
                self.current_branch = line
                self.branch_names.append(line)
            else:
                line = line.strip()
                self.branch_names.append(line)

    def open_folder_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "select folder")
        if not path:
            return
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
