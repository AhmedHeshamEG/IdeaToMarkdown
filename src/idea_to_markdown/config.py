import os
from pathlib import Path
from dotenv import load_dotenv


class AppConfig:
    """
    Manages application configuration, including paths and API keys.
    """

    def __init__(self, custom_base_dir=None):
        # Load environment variables from .env file
        load_dotenv()

        # Root of the project - can be overridden for testing
        self.base_dir = custom_base_dir or Path(
            __file__).resolve().parent.parent.parent

        # Notes directory - relative to base_dir
        self.notes_dir_name = "markdown_notes"
        self.notes_dir = self.base_dir / self.notes_dir_name

        # File naming
        self.scratchpad_file_name = "_GLOBAL_SCRATCHPAD.md"
        self.default_project_name = "General_Ideas"

        # API Keys from environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            print(
                "WARNING: No OpenAI API key found in environment variables or .env file.")
            print("Voice features will not work without a valid API key.")

        # Voice interaction settings from environment or defaults
        self.wake_word = os.getenv("WAKE_WORD", "Hey Agent")
        self.voice_recording_duration = int(
            os.getenv("VOICE_RECORDING_DURATION", "5"))

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
