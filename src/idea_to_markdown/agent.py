from .config import AppConfig
from .note_manager import NoteManager
from .speech_interface import SpeechInterface
import time
import sys


class Agent:
    """
    The main agent that orchestrates voice interaction,
    LLM processing (via SpeechInterface), and note management.
    """

    def __init__(self, config: AppConfig):
        self.config = config
        self.note_manager = NoteManager(config)
        self.speech_interface = SpeechInterface(config)
        self.current_project: str | None = None
        self.running = False

        # Validate critical dependencies
        if not self.speech_interface.client:
            print("WARNING: OpenAI client not available. Voice features will be limited.")
            print("Check your API key in the .env file.")

    def _handle_initial_project_setup(self):
        """Asks user for project context or to use scratchpad via voice."""
        # Prepare the initial prompt with existing projects
        existing_projects = self.note_manager.list_projects()

        project_options = ""
        if existing_projects:
            project_options = f" Existing projects are: {', '.join(existing_projects)}."

        full_initial_prompt = (
            "Welcome! Which project are you working on today? "
            "Or shall we use the general scratchpad?" +
            project_options +
            f" You can say 'new project [name]', 'use [project name]', or 'scratchpad'. Default is '{self.config.default_project_name}'."
        )

        # Show the prompt and get user's response
        print(f"📢 Agent says: {full_initial_prompt}")
        response_text = self.speech_interface.conduct_realtime_conversation_turn(
            "Project name, 'new project [name]', 'use [project name]', or 'scratchpad': "
        )

        if response_text:
            response_lower = response_text.lower()

            # Handle "new project" command
            if "new project" in response_lower:
                name_part = response_lower.replace("new project", "").strip()
                if name_part:
                    self.current_project = name_part
                    self.note_manager.add_note_to_project(
                        self.current_project, f"Project '{self.current_project}' initiated.")
                    print(
                        f"📢 Agent: Okay, working on new project: {self.current_project}.")
                else:
                    print(
                        "📢 Agent: Project name not clearly specified. Using scratchpad for now.")
                    self.current_project = None

            # Handle "use [project]" command
            elif "use " in response_lower and "scratchpad" not in response_lower:
                name_part = response_lower.replace("use", "").strip()
                if name_part and name_part in existing_projects:
                    self.current_project = name_part
                    self.note_manager.add_note_to_project(
                        self.current_project, f"Continuing project '{self.current_project}'.")
                    print(
                        f"📢 Agent: Okay, working on project: {self.current_project}.")
                elif name_part:  # New project implied by "use"
                    self.current_project = name_part
                    self.note_manager.add_note_to_project(
                        self.current_project, f"Starting new project from 'use' command: '{self.current_project}'.")
                    print(
                        f"📢 Agent: Okay, starting new project: {self.current_project}.")
                else:
                    print("📢 Agent: Project name not clear. Using scratchpad.")
                    self.current_project = None

            # Handle "scratchpad" command
            elif "scratchpad" in response_lower:
                self.current_project = None
                print("📢 Agent: Okay, using the global scratchpad.")

            # Handle existing project name
            elif response_text.strip() and response_text.strip() in existing_projects:
                self.current_project = response_text.strip()
                self.note_manager.add_note_to_project(
                    self.current_project, f"Continuing project '{self.current_project}'.")
                print(
                    f"📢 Agent: Okay, working on project: {self.current_project}.")

            # Default handling
            else:
                self.current_project = response_text.strip(
                ) if response_text.strip() else self.config.default_project_name
                self.note_manager.add_note_to_project(
                    self.current_project, f"Project '{self.current_project}' selected/initiated.")
                print(
                    f"📢 Agent: Okay, working on project: {self.current_project}.")
        else:
            # Fallback to default project
            self.current_project = self.config.default_project_name
            self.note_manager.add_note_to_project(
                self.current_project, f"Continuing default project '{self.current_project}'.")
            print(
                f"📢 Agent: No project specified or error. Using default project: {self.current_project}.")

    def start_session(self):
        """Starts the interactive voice session."""
        try:
            self._handle_initial_project_setup()
            self.running = True

            ready_message = f"Ready to capture ideas for '{self.current_project if self.current_project else 'the scratchpad'}'. Say 'exit agent' or 'quit agent' to end."
            print(f"📢 Agent says: {ready_message}")

            while self.running:
                # Listen for user input
                user_final_utterance = self.speech_interface.conduct_realtime_conversation_turn(
                    f"Listening for '{self.current_project or 'scratchpad'}' (or say 'switch project', 'exit agent')..."
                )

                if not user_final_utterance:
                    print(
                        "Agent: No input received or error in voice turn. Retrying...")
                    time.sleep(1)
                    continue

                # Process commands
                if user_final_utterance.lower() in ["exit agent", "quit agent", "stop agent please"]:
                    print("📢 Agent says: Ending session. Goodbye!")
                    self.running = False
                    continue

                if "switch project" in user_final_utterance.lower() or "change project" in user_final_utterance.lower():
                    self._handle_initial_project_setup()
                    continue

                # Save the note
                note_content = user_final_utterance

                if self.current_project:
                    self.note_manager.add_note_to_project(
                        self.current_project, note_content)
                else:
                    self.note_manager.add_note_to_scratchpad(note_content)

                # Confirm note was saved
                preview = note_content[:50] + \
                    "..." if len(note_content) > 50 else note_content
                print(f"📢 Agent: Note saved: '{preview}'")

        except KeyboardInterrupt:
            print("\n\nSession interrupted by user. Exiting gracefully...")
        except Exception as e:
            print(f"Error in agent session: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.running = False
            print("Session ended.")
