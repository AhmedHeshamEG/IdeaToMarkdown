import os
from pathlib import Path
from dotenv import load_dotenv


class AppConfig:
    """
    Manages application configuration, including paths and API keys.
    """

    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        self.base_dir = Path(__file__).resolve(
        ).parent.parent.parent  # Root of the project
        self.notes_dir_name = "my_markdown_notes"
        self.notes_dir = self.base_dir / self.notes_dir_name
        self.scratchpad_file_name = "_GLOBAL_SCRATCHPAD.md"
        # Can be overridden by user preference later
        self.default_project_name = "General_Ideas"

        # API Keys - to be loaded from environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        # Add other API keys as needed (e.g., for specific STT/TTS services)

        # Voice interaction settings
        self.wake_word = "Hey Agent"  # Example, can be made configurable

    def ensure_directories(self):
        """Ensures that the base notes directory exists."""
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        print(f"Notes will be saved in: {self.notes_dir}")

    def get_project_file_path(self, project_name: str) -> Path:
        """Returns the full path to a project's markdown file."""
        return self.notes_dir / f"{project_name}.md"

    def get_scratchpad_file_path(self) -> Path:
        """Returns the full path to the global scratchpad file."""
        return self.notes_dir / self.scratchpad_file_name

# Example of how to use:
# config = AppConfig()
# print(f"OpenAI Key Loaded: {'Yes' if config.openai_api_key else 'No'}")
# print(f"Notes directory: {config.notes_dir}")
