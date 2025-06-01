# Idea to Markdown Agent

**Capture your fleeting thoughts and structure your ideas effortlessly with a voice-first AI agent.**

`idea-to-markdown` is designed for individuals who think faster than they can type, helping to organize brainstorming sessions, project notes, and daily tasks directly into clean Markdown files.

## Core Features (Vision)

- **Conversational Voice Interface:** Interact naturally with an AI agent (powered by models like GPT-4o) to capture, refine, and organize your ideas.
- **Intelligent Note Structuring:** The AI helps format your spoken thoughts into well-structured Markdown, including headings, lists, and code blocks.
- **Project-Based Organization:** Keep your ideas sorted with dedicated Markdown files for each project.
- **Scratchpad Mode:** Quickly capture raw thoughts into a global scratchpad when you're not focused on a specific project.
- **Local First:** Your notes are stored locally on your machine.

## Getting Started

For detailed setup instructions, please see the [Getting Started Guide](docs/01_getting_started.md).

**Quick Overview:**

1. Clone the repository.
2. Set up a Python virtual environment.
3. Install dependencies from `requirements.txt`.
4. Create a `.env` file with your `OPENAI_API_KEY`.
5. Run `python main.py`.

**Note on Current Voice Interaction:** The current version uses OpenAI's APIs for speech-to-text and text-to-speech in a turn-by-turn manner, simulating a conversational flow. True real-time, low-latency streaming voice conversation is a future development goal.

## Current Status

This project is in the early stages of development. The immediate focus is on building the core framework for voice interaction and note management.

## Contributing

We welcome contributions! Please see `docs/03_contributing.md` for guidelines.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
