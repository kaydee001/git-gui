from PySide6.QtCore import QThread, Signal
import subprocess

NO_WINDOW = subprocess.CREATE_NO_WINDOW


class GitWorker(QThread):
    finished = Signal(int, str, str)

    def __init__(self, command, cwd):
        super().__init__()
        self.command = command
        self.cwd = cwd

    def run(self):
        result = subprocess.run(
            self.command, cwd=self.cwd, capture_output=True, text=True, creationflags=NO_WINDOW)
        self.finished.emit(result.returncode, result.stdout, result.stderr)
