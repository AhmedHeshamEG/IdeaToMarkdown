import pytest
from pathlib import Path
import shutil  # For cleaning up test directories

from idea_to_markdown.note_manager import NoteManager
from idea_to_markdown.config import AppConfig


@pytest.fixture
def temp_notes_dir(tmp_path: Path) -> Path:
    notes_dir = tmp_path / "test_markdown_notes"
    notes_dir.mkdir()
    return notes_dir


@pytest.fixture
def test_config(temp_notes_dir: Path) -> AppConfig:
    config = AppConfig()
    # Override the notes_dir to use the temporary one
    config.notes_dir = temp_notes_dir
    return config


@pytest.fixture
def note_manager(test_config: AppConfig) -> NoteManager:
    # Ensure the directory from config is used
    test_config.ensure_directories()
    return NoteManager(test_config)


class TestNoteManager:
    def test_create_new_project_file(self, note_manager: NoteManager, test_config: AppConfig):
        project_name = "TestProject1"
        note_manager.add_note_to_project(
            project_name, "Initial note for TestProject1")

        project_file = test_config.notes_dir / f"{project_name}.md"
        assert project_file.exists()
        with open(project_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert f"# Project: {project_name}" in content
            assert "Initial note for TestProject1" in content

    def test_add_note_to_existing_project(self, note_manager: NoteManager, test_config: AppConfig):
        project_name = "TestProject2"
        note_manager.add_note_to_project(project_name, "First note")
        note_manager.add_note_to_project(project_name, "Second note")

        project_file = test_config.notes_dir / f"{project_name}.md"
        with open(project_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "First note" in content
            assert "Second note" in content
            assert content.count("## Entry:") == 2

    def test_create_scratchpad_file(self, note_manager: NoteManager, test_config: AppConfig):
        note_manager.add_note_to_scratchpad("A quick thought")

        scratchpad_file = test_config.notes_dir / test_config.scratchpad_file_name
        assert scratchpad_file.exists()
        with open(scratchpad_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "# Global Scratchpad" in content
            assert "A quick thought" in content

    def test_list_projects(self, note_manager: NoteManager, test_config: AppConfig):
        # Should be empty initially in test dir
        assert note_manager.list_projects() == []

        note_manager.add_note_to_project("ProjectAlpha", "note a")
        note_manager.add_note_to_project("ProjectBeta", "note b")
        note_manager.add_note_to_scratchpad(
            "scratch note")  # Scratchpad shouldn't be listed

        projects = sorted(note_manager.list_projects())
        assert projects == sorted(["ProjectAlpha", "ProjectBeta"])

    def test_add_note_empty_project_name(self, note_manager: NoteManager, capsys):
        note_manager.add_note_to_project("", "This note should not be saved")
        captured = capsys.readouterr()
        assert "Error: Project name cannot be empty." in captured.out

    def test_timestamp_format(self, note_manager: NoteManager):
        """Test the timestamp format used in notes"""
        timestamp = note_manager._get_timestamp_prefix()
        # Check that the timestamp matches the expected format (YYYY-MM-DD HH:MM:SS)
        assert len(timestamp) == 19  # Length of "YYYY-MM-DD HH:MM:SS"
        assert timestamp[4] == "-" and timestamp[7] == "-"  # Date format
        assert timestamp[10] == " "  # Space between date and time
        assert timestamp[13] == ":" and timestamp[16] == ":"  # Time format

    def test_multiple_notes_formatting(self, note_manager: NoteManager, test_config: AppConfig):
        """Test the formatting of multiple notes in a single project file"""
        project_name = "FormattingTest"

        # Add several notes
        note_manager.add_note_to_project(project_name, "First note")
        note_manager.add_note_to_project(
            project_name, "Second note\nWith multiple lines")
        note_manager.add_note_to_project(
            project_name, "- Third note\n- With bullets")

        project_file = test_config.notes_dir / f"{project_name}.md"
        with open(project_file, "r", encoding="utf-8") as f:
            content = f.read()

            # Check that the project header appears once
            assert content.count(f"# Project: {project_name}") == 1

            # Check that each note has its own entry header
            assert content.count("## Entry:") == 3

            # Check multiline content is preserved
            assert "Second note\nWith multiple lines" in content

            # Check bullet formatting is preserved
            assert "- Third note\n- With bullets" in content
