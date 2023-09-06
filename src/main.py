import argparse
import os
import sys
from dotenv import load_dotenv
from streamlit.web import cli as stcli
from utils.process import process

# Load environment variables from a .env file (containing OPENAI_API_KEY)
load_dotenv()


def extract_repo_name(repo_url):
    """Extract the repository name from the given repository URL."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    return repo_name


def process_repo(args):
    """
    Process the git repository by cloning it, filtering files, and
    creating an Activeloop dataset with the contents.
    """
    repo_name = extract_repo_name(args.repo_url)
    process(
        args.repo_url,
        args.include_file_extensions,
        args.repo_destination,
    )


def chat(args):
    """
    Start the Streamlit chat application using the specified Activeloop dataset.
    """
    sys.argv = [
        "streamlit",
        "run",
        "src/utils/chat.py",
        "--",
        f"--repo-url={args.repo_url}",
    ]

    sys.exit(stcli.main())


def main():
    """Define and parse CLI arguments, then execute the appropriate subcommand."""
    parser = argparse.ArgumentParser(description="Chat with a git repository")
    subparsers = parser.add_subparsers(dest="command")

    # Process subcommand
    process_parser = subparsers.add_parser("process", help="Process a git repository")
    process_parser.add_argument(
        "--repo-url", required=True, help="The git repository URL"
    )
    process_parser.add_argument(
        "--include-file-extensions",
        nargs="+",
        default=None,
        help=(
            "Exclude all files not matching these extensions. Example:"
            " --include-file-extensions .py .js .ts .html .css .md .txt"
        ),
    )
    process_parser.add_argument(
        "--repo-destination",
        default="repos",
        help="The destination to clone the repository. Defaults to 'repos'.",
    )

    # Chat subcommand
    chat_parser = subparsers.add_parser("chat", help="Start the chat application")
    chat_parser.add_argument(
        "--repo-url", required=True, help="The git repository URL"
    )

    args = parser.parse_args()

    if args.command == "process":
        process_repo(args)
    elif args.command == "chat":
        chat(args)


if __name__ == "__main__":
    main()
