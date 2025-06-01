# Contributing to Idea to Markdown Agent

Thank you for your interest in contributing to the Idea to Markdown Agent! We welcome contributions from the community to help make this tool even better.

## Ways to Contribute

- **Reporting Bugs:** If you find a bug, please open an issue on GitHub, providing as much detail as possible, including steps to reproduce, expected behavior, and actual behavior.
- **Suggesting Enhancements:** Have an idea for a new feature or an improvement to an existing one? Open an issue to discuss it.
- **Code Contributions:** If you'd like to contribute code, please follow the process outlined below.
- **Documentation:** Improving documentation is always welcome, whether it's fixing typos, clarifying explanations, or adding new sections.

## Development Setup

1.  **Fork the Repository:** Start by forking the main repository to your own GitHub account.
2.  **Clone Your Fork:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/idea-to-markdown.git
    cd idea-to-markdown
    ```
3.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    # .venv\Scripts\activate    # On Windows
    ```
4.  **Install Dependencies:**
    Install runtime dependencies and development dependencies:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```
5.  **Set Up Environment Variables:**
    Copy the `.env.example` (if one exists, otherwise create `.env` manually) to `.env` and add your `OPENAI_API_KEY`:
    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

## Making Changes

1.  **Create a New Branch:**
    ```bash
    git checkout -b feature/your-feature-name  # For new features
    # or
    git checkout -b fix/issue-description     # For bug fixes
    ```
2.  **Write Code:** Make your changes, adhering to the project's coding style.
    - **Style:** We aim to follow PEP 8. Consider using a linter like Flake8. (Formatting with Black is encouraged if adopted by the project).
    - **Type Hinting:** Please include type hints for new functions and methods.
3.  **Write Tests:** Add unit tests for any new functionality or bug fixes. Ensure existing tests pass.
    - Run tests using `pytest`.
4.  **Documentation:** Update any relevant documentation (README, usage guides, code comments) to reflect your changes.
5.  **Commit Your Changes:** Write clear and concise commit messages.
    ```bash
    git add .
    git commit -m "feat: Implement X feature"
    # or
    git commit -m "fix: Resolve Y bug by doing Z"
    ```
6.  **Push to Your Fork:**
    ```bash
    git push origin feature/your-feature-name
    ```

## Submitting a Pull Request

1.  Go to the original repository on GitHub.
2.  Click on "New pull request".
3.  Choose your fork and the branch containing your changes.
4.  Provide a clear title and description for your pull request, explaining the changes and referencing any related issues.
5.  Submit the pull request.

Your PR will be reviewed, and feedback may be provided. Please be responsive to comments and questions.

## Code of Conduct

While we don't have a formal Code of Conduct document yet, please be respectful and considerate in all interactions. We aim for a positive and collaborative community.

Thank you for contributing!
