from .config import AppConfig
from .note_manager import NoteManager
from .speech_interface import SpeechInterface
import time  # Added for time.sleep


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

    def _handle_initial_project_setup(self):
        """Asks user for project context or to use scratchpad via voice."""
        # Initial prompt for project setup
        initial_prompt_text = (
            "Welcome! Which project are you working on today? "
            "Or shall we use the general scratchpad?"
        )
        # The speech interface will speak this and listen for a response
        # For this setup, we'll make the agent speak first, then listen.

        # Agent speaks the welcome and project query
        # In a real conversational flow, the speech_interface would handle this turn.
        # For now, let's simulate the agent speaking then listening.

        # Let's construct the full prompt for the user
        full_initial_prompt = initial_prompt_text
        existing_projects = self.note_manager.list_projects()
        if existing_projects:
            full_initial_prompt += f" Existing projects are: {', '.join(existing_projects)}."
        full_initial_prompt += f" You can say 'new project [name]', 'use [project name]', or 'scratchpad'. Default is '{self.config.default_project_name}'."

        # The speech_interface will handle speaking this and getting the user's spoken response
        # For this conceptual step, we'll assume the agent "speaks" then "listens"
        # A more integrated SpeechInterface would handle this as one conversational turn.

        # Simulate agent speaking the prompt (actual TTS is in SpeechInterface)
        # This line is for console feedback
        # FUTURE: Agent should speak this
        print(f"📢 Agent says: {full_initial_prompt}")
        # The actual speaking and listening is now part of conduct_realtime_conversation_turn

        response_text = self.speech_interface.conduct_realtime_conversation_turn(
            "Project name, 'new project [name]', 'use [project name]', or 'scratchpad': "
        )

        if response_text:
            response_lower = response_text.lower()
            if "new project" in response_lower:
                # Attempt to extract project name (simple parsing)
                name_part = response_lower.replace("new project", "").strip()
                if name_part:
                    self.current_project = name_part  # Consider more robust name extraction
                    self.note_manager.add_note_to_project(
                        self.current_project, f"Project '{self.current_project}' initiated.")
                    # Agent confirms action (text for now, SpeechInterface would speak it)
                    print(
                        # FUTURE: Agent should speak this
                        f"📢 Agent: Okay, working on new project: {self.current_project}.")
                else:
                    print(
                        # FUTURE: Agent should speak this
                        "📢 Agent: Project name not clearly specified. Using scratchpad for now.")
                    self.current_project = None
            elif "use " in response_lower and not "scratchpad" in response_lower:  # e.g. "use my novel"
                name_part = response_lower.replace("use", "").strip()
                if name_part and name_part in existing_projects:
                    self.current_project = name_part
                    self.note_manager.add_note_to_project(
                        self.current_project, f"Continuing project '{self.current_project}'.")
                    print(
                        # FUTURE: Agent should speak this
                        f"📢 Agent: Okay, working on project: {self.current_project}.")
                elif name_part:  # New project implied by "use"
                    self.current_project = name_part
                    self.note_manager.add_note_to_project(
                        self.current_project, f"Starting new project from 'use' command: '{self.current_project}'.")
                    print(
                        # FUTURE: Agent should speak this
                        f"📢 Agent: Okay, starting new project: {self.current_project}.")
                else:
                    # FUTURE: Agent should speak this
                    print("📢 Agent: Project name not clear. Using scratchpad.")
                    self.current_project = None

            elif "scratchpad" in response_lower:
                self.current_project = None
                # FUTURE: Agent should speak this
                print("📢 Agent: Okay, using the global scratchpad.")
            # User just said an existing project name
            elif response_text.strip() and response_text.strip() in existing_projects:
                self.current_project = response_text.strip()
                self.note_manager.add_note_to_project(
                    self.current_project, f"Continuing project '{self.current_project}'.")
                print(
                    # FUTURE: Agent should speak this
                    f"📢 Agent: Okay, working on project: {self.current_project}.")
            else:  # Default or unrecognized, could be a new project name directly
                self.current_project = response_text.strip(
                ) if response_text.strip() else self.config.default_project_name
                self.note_manager.add_note_to_project(
                    self.current_project, f"Project '{self.current_project}' selected/initiated.")
                print(
                    # FUTURE: Agent should speak this
                    f"📢 Agent: Okay, working on project: {self.current_project}.")
        else:  # No response or error in speech interface
            self.current_project = self.config.default_project_name
            self.note_manager.add_note_to_project(
                self.current_project, f"Continuing default project '{self.current_project}'.")
            print(
                # FUTURE: Agent should speak this
                f"📢 Agent: No project specified or error. Using default project: {self.current_project}.")

        # The speech interface would ideally speak the confirmation.
        # For now, agent prints to console.

    def start_session(self):
        """Starts the interactive voice session."""
        self._handle_initial_project_setup()
        self.running = True

        ready_message = f"Ready to capture ideas for '{self.current_project if self.current_project else 'the scratchpad'}'. Say 'exit agent' or 'quit agent' to end."
        # FUTURE: Agent should speak this
        print(f"📢 Agent says: {ready_message}")
        # In a full loop, the speech interface would play this.

        while self.running:
            # The speech_interface now handles listening, sending to LLM, and speaking response.
            # It returns the user's transcribed input.
            user_final_utterance = self.speech_interface.conduct_realtime_conversation_turn(
                f"Listening for '{self.current_project or 'scratchpad'}' (or say 'switch project', 'exit agent')..."
            )

            if not user_final_utterance:
                # Error or no input, speech_interface should have handled user feedback.
                # Agent can decide to reprompt or wait. For now, continue.
                # FUTURE: Agent might speak a reprompt
                print("Agent: No input received or error in voice turn. Retrying...")
                time.sleep(1)  # Brief pause
                continue

            # Process user's utterance for agent commands or note-taking
            if user_final_utterance.lower() in ["exit agent", "quit agent", "stop agent please"]:
                # Agent "speaks"
                # FUTURE: Agent should speak this
                print("📢 Agent says: Ending session. Goodbye!")
                self.running = False
                continue

            if "switch project" in user_final_utterance.lower() or "change project" in user_final_utterance.lower():
                self._handle_initial_project_setup()  # Re-run project setup
                # Confirmation is handled within _handle_initial_project_setup's print statements for now
                continue

            # If not a command, assume it's content for a note.
            # The LLM integrated within conduct_realtime_conversation_turn might have already
            # structured or confirmed the note. Here, we save the user's raw utterance
            # or a processed version if the LLM provided one.
            # For this iteration, we save the user's transcribed utterance.
            note_content = user_final_utterance

            if self.current_project:
                self.note_manager.add_note_to_project(
                    self.current_project, note_content)
            else:
                self.note_manager.add_note_to_scratchpad(note_content)

            # Agent confirms note saved (text for now)
            # FUTURE: Agent should speak this confirmation
            print(f"📢 Agent: Note saved: '{note_content[:50]}...'")

            # Ideally, the speech_interface's LLM interaction would confirm this naturally.
