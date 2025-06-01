# Getting Started with Idea to Markdown Agent

Welcome to the Idea to Markdown Agent! This guide will help you get the agent up and running on your local machine.

## Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)
- An OpenAI API Key (for voice interaction and AI features)
- Microphone access for your system
- (Potentially) C++ Build Tools for Windows if you encounter issues installing `PyAudio`.

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/OWNER/REPOSITORY.git
    cd REPOSITORY
    ```

    _(Replace `OWNER/REPOSITORY` with the actual path to the repository, e.g., `YourGitHubUsername/idea-to-markdown` if you've forked it, or the main project's URL.)_

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv .venv
    ```

    Activate the virtual environment:

    - Windows: `.venv\Scripts\activate`
    - macOS/Linux: `source .venv/bin/activate`

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a file named `.env` in the root directory of the project (`idea-to-markdown/.env`).
    Add your OpenAI API key to this file:
    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    Replace `"your_openai_api_key_here"` with your actual OpenAI API key.

## Running the Agent

Once you have completed the installation and setup, you can run the agent using the main script:

```bash
python main.py
```

The agent will initialize, and if your OpenAI API key is correctly set up and microphone access is working, it will guide you through selecting a project or using the scratchpad via voice (simulated by console input in the current version if full voice isn't implemented).

## First Interaction

- The agent will greet you and ask which project you're working on.
- You can respond by saying:
  - `"new project [your project name]"` (e.g., "new project My Novel Ideas")
  - `"use [existing project name]"` (if you've used it before)
  - `"scratchpad"` to use the global scratchpad.
- Follow the agent's voice prompts to capture your ideas.
- Say `"exit agent"` or `"quit agent"` to end the session.

Your notes will be saved in the `my_markdown_notes` directory within the project folder.

## Troubleshooting

- **PyAudio Installation Issues (Windows):** If `pip install pyaudio` fails, you might need to install Microsoft C++ Build Tools. Alternatively, you can try installing PyAudio using a pre-compiled wheel from a trusted source like Christoph Gohlke's Unofficial Windows Binaries for Python Extension Packages.
- **`OPENAI_API_KEY not found`:** Ensure your `.env` file is in the root project directory and correctly formatted.
- **Microphone Not Working:** Check your system's microphone settings and ensure the application has permission to access it.

Happy note-taking!
