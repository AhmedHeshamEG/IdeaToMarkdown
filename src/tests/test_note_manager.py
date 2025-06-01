import pytest
from pathlib import Path
import shutil  # For cleaning up test directories

from idea_to_markdown.note_manager import NoteManager
from idea_to_markdown.config import AppConfig

# Fixture to create a temporary notes directory for testing


@pytest.fixture
def temp_notes_dir(tmp_path: Path) -> Path:
    notes_dir = tmp_path / "test_markdown_notes"
    notes_dir.mkdir()
    return notes_dir


@pytest.fixture
def test_config(temp_notes_dir: Path) -> AppConfig:
    config = AppConfig()
    # Override the notes_dir to use the temporary one
    original_base_dir = config.base_dir
    config.notes_dir = temp_notes_dir
    # Adjust base_dir if other paths depend on it relative to notes_dir, though not strictly needed for these tests
    # config.base_dir = temp_notes_dir.parent
    return config


@pytest.fixture
def note_manager(test_config: AppConfig) -> NoteManager:
    # Ensure the directory from config is used
    # Make sure the test_notes_dir is created by config
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
        # Assert that no new project files were created unexpectedly (tricky without knowing all files)
        # For simplicity, check if notes_dir is empty or only contains scratchpad if it was made
        # This depends on the test execution order or better isolation.
        # For now, the error message check is the primary assertion.

    # Clean up the temporary directory after all tests in this class if needed,
    # though pytest's tmp_path fixture handles this automatically.
    # def teardown_class(cls):
    #     # Example: if test_config.notes_dir was manually created and not part of tmp_path
    #     # if Path("path_to_temp_notes_during_test").exists():
    #     #     shutil.rmtree("path_to_temp_notes_during_test")
    #     pass
