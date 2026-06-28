import os
import subprocess
from PySide6.QtWidgets import QFileDialog, QMessageBox
from worker import GitWorker

NO_WINDOW = subprocess.CREATE_NO_WINDOW


class GitOpsMixin():
    def on_git_done(self, returncode, stdout, stderr):
        self.hide_spinner()
        if returncode:
            self.show_message("error", stderr, QMessageBox.Icon.Warning)
        else:
            self.run_git_status()

    def is_git_repo(self):
        selected_path = os.path.join(self.selected_path, ".git")
        if os.path.exists(selected_path):
            return True

        return False

    def run_git_status(self):
        self.run_git_branch()

        result = subprocess.run(
            ["git", "status"], cwd=self.selected_path, capture_output=True, text=True, creationflags=NO_WINDOW)
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
        self.show_spinner()
        command = ["git", "add", "."]
        self.worker = GitWorker(command, self.selected_path)
        self.worker.finished.connect(self.on_git_done)
        self.worker.start()

    def run_git_commit(self):
        msg = self.commit_input.text()
        if not msg:
            self.show_message("error", "no commit msg found",
                              QMessageBox.Icon.Warning)
        else:
            result = subprocess.run(
                ["git", "commit", "-m", f"{msg}"], cwd=self.selected_path, capture_output=True, text=True, creationflags=NO_WINDOW)
            self.commit_input.clear()
            self.run_git_status()

    def run_git_push(self):
        self.show_spinner()
        command = ["git", "push"]
        self.worker = GitWorker(command, self.selected_path)
        self.worker.finished.connect(self.on_git_done)
        self.worker.start()

    def run_git_log(self):
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"], cwd=self.selected_path, capture_output=True, text=True, creationflags=NO_WINDOW)
        self.commit_log.clear()
        lines = result.stdout.splitlines()
        for line in lines:
            self.commit_log.addItem(line)

    def run_git_unstage(self):
        result = subprocess.run(
            ["git", "reset"], cwd=self.selected_path, capture_output=True, text=True, creationflags=NO_WINDOW)
        self.run_git_status()

    def switch_branch(self, branch_name):
        result = subprocess.run(
            ["git", "checkout", f"{branch_name}"], cwd=self.selected_path, capture_output=True, text=True, creationflags=NO_WINDOW)
        if result.returncode:
            self.show_message("error", result.stderr,
                              QMessageBox.Icon.Warning)
        else:
            self.run_git_status()

    def run_git_branch(self):
        result = subprocess.run(
            ["git", "branch"], cwd=self.selected_path, capture_output=True, text=True, creationflags=NO_WINDOW)
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

    def run_git_pull(self):
        self.show_spinner()
        command = ["git", "pull"]
        self.worker = GitWorker(command, self.selected_path)
        self.worker.finished.connect(self.on_git_done)
        self.worker.start()

    def run_git_fetch_all(self):
        self.show_spinner()
        command = ["git", "fetch", "--all"]
        self.worker = GitWorker(command, self.selected_path)
        self.worker.finished.connect(self.on_git_done)
        self.worker.start()

    def open_folder_dialog(self):
        path = QFileDialog.getExistingDirectory(self, "select folder")
        if not path:
            return
        self.selected_path = path
        folder_name = os.path.basename(self.selected_path)
        self.status_section_label.setText(f"repository status : {folder_name}")
        self.folder_label.setText(None)

        is_repo = self.is_git_repo()
        if not is_repo:
            self.show_message("error", "not a repo",
                              QMessageBox.Icon.Warning)
        else:
            self.run_git_status()
            self.enable_UI()
