import sys
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QHBoxLayout

# app = QApplication(sys.argv)
# window = QWidget()

# window.setWindowTitle("test")
# window.resize(500, 500)
# window.show()

# app.exec()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        self.resize(500, 500)

        self.button = QPushButton("select folder")
        self.label = QLabel("no folder selected")
        self.button.clicked.connect(self.open_folder_dialog)

        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def open_folder_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "select folder")
        self.selected_path = path
        self.label.setText(path)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
