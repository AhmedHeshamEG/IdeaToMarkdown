# Usage Guide - Idea to Markdown Agent

This guide explains how to interact with the Idea to Markdown Agent and understand its core functionalities.

## Starting the Agent

Ensure you have followed the [Getting Started Guide](01_getting_started.md) for installation and setup.
Run the agent from the root project directory:

```bash
python main.py
```

## Initial Interaction: Project Selection

Upon starting, the agent will greet you and ask about the project context:

- **Agent:** "Welcome! Which project are you working on today? Or shall we use the general scratchpad? Existing projects are: [list of projects]. You can say 'new project [name]', 'use [project name]', or 'scratchpad'. Default is 'General_Ideas'."

You can respond by speaking (the agent will transcribe your voice):

- **To create a new project:** Say `"new project My Awesome Project"`
- **To use an existing project:** Say `"use My Awesome Project"`
- **To use the general scratchpad:** Say `"scratchpad"`
- **To use the default project:** You can often just state a new idea, or if no specific command is recognized, it might default to the `General_Ideas` project or the last used one.

The agent will confirm your selection.

## Capturing Ideas

Once a project (or the scratchpad) is active:

- **Agent:** "Listening for '[current project/scratchpad]' (or say 'switch project', 'exit agent')..."
- **You:** Speak your idea or note naturally.
  - Example: "Remember to research advanced voice streaming APIs for the next iteration."
- **Agent:** (After processing with OpenAI) The agent will typically confirm the note has been saved or respond conversationally.
  - Example Console Output: `📢 Agent: Note saved: 'Remember to research advanced voice strea...'`
  - The agent will also speak its response.

Your spoken idea will be appended as a new entry in the corresponding Markdown file located in the `my_markdown_notes` directory.

## Key Voice Commands

While in an active session:

- **`"switch project"` or `"change project"`:** The agent will re-initiate the project selection process, allowing you to switch to a different project, create a new one, or go to the scratchpad.
- **`"exit agent"` or `"quit agent"` or `"stop agent please"`:** This will end the current session with the agent.

## Note Structure in Markdown Files

- **Project Files (`my_markdown_notes/ProjectName.md`):**

  ```markdown
  # Project: ProjectName - Created YYYY-MM-DD HH:MM:SS

  ## Entry: YYYY-MM-DD HH:MM:SS

  Your first idea for this project.

  ## Entry: YYYY-MM-DD HH:MM:SS

  Another idea or note.
  ```

- **Scratchpad File (`my_markdown_notes/_GLOBAL_SCRATCHPAD.md`):**

  ```markdown
  # Global Scratchpad - YYYY-MM-DD HH:MM:SS

  ## Scratchpad Entry: YYYY-MM-DD HH:MM:SS

  A quick thought captured here.

  ## Scratchpad Entry: YYYY-MM-DD HH:MM:SS

  Another random idea.
  ```

## Current Limitations

- **Voice Interaction:** The current voice interaction uses OpenAI's STT and TTS APIs in a turn-by-turn fashion. True real-time, low-latency streaming (like a continuous phone call) is a future goal. There might be slight delays between you speaking, the AI processing, and the AI responding.
- **Complex Commands:** Advanced note structuring commands (e.g., "make that a bullet list," "summarize my last three ideas") are part of the future vision and may not be fully implemented or robust in the current version. The agent primarily focuses on capturing raw ideas.
- **Error Handling:** While basic error handling is in place, comprehensive spoken feedback for all types of errors (e.g., network issues, API limits) is still being refined.

## Troubleshooting

Refer to the [Getting Started Guide](01_getting_started.md#troubleshooting) for common setup issues.

- **Agent doesn't understand me / Transcription is poor:**
  - Ensure you are in a relatively quiet environment.
  - Speak clearly and at a moderate pace.
  - Check your microphone input levels.
- **Agent doesn't respond or seems stuck:**
  - Check your internet connection, as OpenAI API calls require it.
  - Look at the console output for any error messages.
  - You might have hit an API rate limit with OpenAI if you're making many requests quickly.
