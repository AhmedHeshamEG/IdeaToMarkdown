from .agent import Agent
from .config import AppConfig
import sys


def main():
    """
    Main function to initialize and run the Idea to Markdown agent.
    """
    print("Initializing Idea to Markdown Agent...")

    try:
        config = AppConfig()

        # Ensure necessary directories exist
        config.ensure_directories()

        # Initialize and start the agent
        agent = Agent(config)
        agent.start_session()

    except KeyboardInterrupt:
        print("\nShutting down Idea to Markdown Agent...")
    except Exception as e:
        print(f"Error starting Idea to Markdown Agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
