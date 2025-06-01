<div align="center">
  <img src="docs/assets/icon.png" alt="Idea to Markdown Logo" width="180" height="180">
  <h1>Idea to Markdown Agent</h1>
  
  [![Python Application CI](https://github.com/AhmedHeshamEG/IdeaToMarkdown/actions/workflows/python-app.yml/badge.svg)](https://github.com/AhmedHeshamEG/IdeaToMarkdown/actions/workflows/python-app.yml)
  [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Status](https://img.shields.io/badge/status-beta-orange)](https://github.com/AhmedHeshamEG/IdeaToMarkdown)
  [![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)](https://platform.openai.com/)
  [![Documentation](https://img.shields.io/badge/docs-available-brightgreen)](docs/01_getting_started.md)
  [![Version](https://img.shields.io/badge/version-0.1.0-informational)](https://github.com/AhmedHeshamEG/IdeaToMarkdown/releases)
</div>

**Capture your fleeting thoughts and structure your ideas effortlessly with a voice-first AI agent.**

## 🚀 Overview

**Idea to Markdown** is a voice-first AI assistant that transforms your spoken thoughts into beautifully structured Markdown files. Perfect for writers, developers, researchers, and anyone who thinks faster than they type.

> "Capture ideas as quickly as you think of them, without breaking your flow."

## ✨ Key Features

- **🎙️ Voice-First Interface**: Speak naturally to an AI assistant powered by OpenAI's advanced models
- **🧠 Intelligent Structure**: AI helps format your spoken thoughts into well-organized Markdown
- **📂 Project Organization**: Keep your notes organized by project
- **📝 Scratchpad Mode**: Quickly capture fleeting thoughts without context-switching
- **🔒 Privacy-Focused**: All notes stored locally on your machine

## 🛠️ Installation

```bash
# Clone and install from source
git clone https://github.com/AhmedHeshamEG/IdeaToMarkdown.git
cd IdeaToMarkdown

# Set up a virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

You'll need an OpenAI API key with access to GPT-4o (or similar model) and speech capabilities:

```bash
# Create .env file in your project directory
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## 📖 Usage

Start the application:

```bash
python main.py
```

The agent will guide you through:

1. Selecting or creating a project
2. Capturing your ideas through voice
3. Organizing everything into Markdown files

### Voice Commands

- **"new project [name]"** - Create a new project
- **"use [project name]"** - Switch to an existing project
- **"scratchpad"** - Use the global scratchpad
- **"switch project"** - Change to a different project
- **"exit agent"** - End the session

## 📚 Documentation

For more detailed information, see:

- [Getting Started Guide](docs/01_getting_started.md)
- [Usage Guide](docs/02_usage_guide.md)
- [Contributing](CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
