import sys
import os
from PySide6.QtWidgets import QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox, QTextEdit, QLineEdit, QListWidget, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie
from git_ops import GitOpsMixin


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path


class MainWindow(QWidget, GitOpsMixin):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git GUI")
        self.resize(800, 600)

        self._init_widgets()
        self._init_connections()
        self._init_layout()

        with open(resource_path("style.qss"), "r") as f:
            self.setStyleSheet(f.read())

    def _init_widgets(self):
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
        self.pull_button = QPushButton("pull")
        self.fetch_all_button = QPushButton("fetch all")
        self.spinner = QLabel()
        self.spinner_movie = QMovie(resource_path("loading_ring.gif"))

        self.status_label.setObjectName("statusLabel")

        self.folder_button.setFixedWidth(180)
        self.stage_button.setFixedWidth(180)
        self.unstage_button.setFixedWidth(180)

        self.status_box.setReadOnly(True)

        self.commit_button.setFixedWidth(180)
        self.push_button.setFixedWidth(180)

        self.log_button.setFixedWidth(180)

        self.commit_input.setPlaceholderText("enter commit msg")
        self.commit_input.setEnabled(False)

        self.pull_button.setFixedWidth(180)
        self.fetch_all_button.setFixedWidth(180)

        self.spinner.setMovie(self.spinner_movie)
        self.spinner.setFixedSize(24, 24)
        self.spinner_movie.setScaledSize(self.spinner.size())
        self.spinner.hide()

        self.stage_button.setEnabled(False)
        self.commit_button.setEnabled(False)
        self.push_button.setEnabled(False)
        self.log_button.setEnabled(False)
        self.unstage_button.setEnabled(False)
        self.pull_button.setEnabled(False)
        self.fetch_all_button.setEnabled(False)

    def _init_connections(self):
        self.stage_button.clicked.connect(self.run_git_add)
        self.commit_button.clicked.connect(self.run_git_commit)
        self.push_button.clicked.connect(self.run_git_push)
        self.log_button.clicked.connect(self.run_git_log)
        self.unstage_button.clicked.connect(self.run_git_unstage)
        self.branch_dropdown.currentTextChanged.connect(self.switch_branch)
        self.pull_button.clicked.connect(self.run_git_pull)
        self.fetch_all_button.clicked.connect(self.run_git_fetch_all)
        self.folder_button.clicked.connect(self.open_folder_dialog)

    def _init_layout(self):
        row1 = QHBoxLayout()
        row1.addWidget(self.folder_button)
        row1.addSpacing(15)
        row1.addWidget(self.folder_label)
        row1.addStretch()
        row1.addWidget(self.spinner)
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

        row5 = QHBoxLayout()
        row5.addWidget(self.pull_button)
        row5.addWidget(self.fetch_all_button)

        main_layout = QVBoxLayout()
        row1.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(row1)
        main_layout.addWidget(self.status_box)
        main_layout.addLayout(row2)
        main_layout.addWidget(self.commit_input)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)
        main_layout.addLayout(row5)

        self.setLayout(main_layout)

    def enable_UI(self):
        self.stage_button.setEnabled(True)
        self.commit_button.setEnabled(True)
        self.commit_input.setEnabled(True)
        self.push_button.setEnabled(True)
        self.log_button.setEnabled(True)
        self.unstage_button.setEnabled(True)
        self.pull_button.setEnabled(True)
        self.fetch_all_button.setEnabled(True)

    def disable_UI(self):
        self.stage_button.setEnabled(False)
        self.commit_button.setEnabled(False)
        self.push_button.setEnabled(False)
        self.log_button.setEnabled(False)
        self.unstage_button.setEnabled(False)
        self.pull_button.setEnabled(False)
        self.fetch_all_button.setEnabled(False)
        self.commit_input.setEnabled(False)

    def show_spinner(self):
        self.spinner_movie.start()
        self.spinner.show()
        self.disable_UI()

    def hide_spinner(self):
        self.spinner_movie.stop()
        self.spinner.hide()
        self.enable_UI()

    def show_message(self, title, text, icon=QMessageBox.Icon.Information):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setFixedWidth(300)
        msg.exec()
