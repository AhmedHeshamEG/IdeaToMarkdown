from idea_to_markdown.agent import Agent
from idea_to_markdown.config import AppConfig


def main():
    """
    Main function to initialize and run the Idea to Markdown agent.
    """
    print("Initializing Idea to Markdown Agent...")
    config = AppConfig()
    # Ensure necessary directories exist (e.g., notes directory)
    config.ensure_directories()

    agent = Agent(config)
    agent.start_session()


if __name__ == "__main__":
    main()
