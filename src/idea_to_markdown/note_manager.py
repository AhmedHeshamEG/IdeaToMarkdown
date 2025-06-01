from pathlib import Path
from datetime import datetime
from .config import AppConfig


class NoteManager:
    """
    Handles creation, writing, and management of Markdown note files.
    """

    def __init__(self, config: AppConfig):
        self.config = config

    def _get_timestamp_prefix(self) -> str:
        """Generates a timestamp prefix for notes."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _ensure_file_exists(self, file_path: Path):
        """Ensures a file exists, creating it with a header if not."""
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                if file_path.name == self.config.scratchpad_file_name:
                    f.write(
                        f"# Global Scratchpad - {self._get_timestamp_prefix()}\n\n")
                else:
                    project_name = file_path.stem
                    f.write(
                        f"# Project: {project_name} - Created {self._get_timestamp_prefix()}\n\n")
            print(f"Created new note file: {file_path}")

    def add_note_to_project(self, project_name: str, content: str):
        """
        Adds a note to the specified project's Markdown file.
        Each project has its own .md file.
        """
        if not project_name:
            print("Error: Project name cannot be empty.")
            return

        project_file_path = self.config.get_project_file_path(project_name)
        self._ensure_file_exists(project_file_path)

        with open(project_file_path, "a", encoding="utf-8") as f:
            f.write(f"\n## Entry: {self._get_timestamp_prefix()}\n")
            f.write(content.strip() + "\n")
        print(f"Note added to project '{project_name}'.")

    def add_note_to_scratchpad(self, content: str):
        """
        Adds a note to the global scratchpad file.
        """
        scratchpad_path = self.config.get_scratchpad_file_path()
        self._ensure_file_exists(scratchpad_path)

        with open(scratchpad_path, "a", encoding="utf-8") as f:
            f.write(f"\n## Scratchpad Entry: {self._get_timestamp_prefix()}\n")
            f.write(content.strip() + "\n")
        print("Note added to scratchpad.")

    def list_projects(self) -> list[str]:
        """Lists all existing project markdown files."""
        projects = []
        if self.config.notes_dir.exists():
            for item in self.config.notes_dir.iterdir():
                if item.is_file() and item.suffix == ".md" and item.name != self.config.scratchpad_file_name:
                    # .stem gives filename without extension
                    projects.append(item.stem)
        return projects
