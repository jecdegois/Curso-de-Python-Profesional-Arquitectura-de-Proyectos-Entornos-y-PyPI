"""CLI interface for Platzi News."""

import logging
import sys
from types import SimpleNamespace
from typing import NoReturn

from ..core.services import NewsService
from .display import display_answer, display_articles, display_error


def print_help() -> None:
    """Print help message."""
    print("Usage: platzi-news [command] [options]")
    print("Commands:")
    print("  search <query> --source <source>    Search articles")
    print("  ask <query> <question> --source <source>    Ask about news")
    print("Options:")
    print(
        "  --log-level <level>    Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )


def parse_args() -> SimpleNamespace:
    """Parse command line arguments manually."""
    log_level = None

    # Check for --log-level and remove it
    if "--log-level" in sys.argv:
        idx = sys.argv.index("--log-level")
        if idx + 1 < len(sys.argv):
            log_level = sys.argv[idx + 1]
            # Remove them from sys.argv
            del sys.argv[idx : idx + 2]
        else:
            print("Error: --log-level requires a value")
            sys.exit(1)

    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "search":
        if len(sys.argv) != 5 or sys.argv[3] != "--source":
            print("Usage: platzi-news search <query> --source <source>")
            sys.exit(1)
        query = sys.argv[2]
        source = sys.argv[4]
        return SimpleNamespace(
            command=command, query=query, source=source, log_level=log_level
        )
    elif command == "ask":
        if len(sys.argv) != 6 or sys.argv[4] != "--source":
            print("Usage: platzi-news ask <query> <question> --source <source>")
            sys.exit(1)
        query = sys.argv[2]
        question = sys.argv[3]
        source = sys.argv[5]
        return SimpleNamespace(
            command=command,
            query=query,
            question=question,
            source=source,
            log_level=log_level,
        )
    else:
        print_help()
        sys.exit(1)


async def main() -> NoReturn:
    """Main entry point for the CLI application."""
    args = parse_args()

    # Configure logging only if --log-level is provided
    if args.log_level:
        logging.basicConfig(
            level=getattr(logging, args.log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
    logger = logging.getLogger(__name__)

    try:
        service = NewsService()
        if args.command == "search":
            logger.info(f"Searching for '{args.query}' in {args.source}")
            articles = await service.asearch_articles(args.source, args.query)
            logger.info(f"Found {len(articles)} articles")
            display_articles(articles)
        elif args.command == "ask":
            logger.info(
                f"Asking '{args.question}' about '{args.query}' from {args.source}"
            )
            articles = await service.asearch_articles(args.source, args.query)
            logger.info(f"Retrieved {len(articles)} articles for analysis")
            answer = service.analyze_articles(articles, args.question)
            logger.info("Analysis completed successfully")
            display_answer(answer)
        else:
            print_help()
            sys.exit(1)
    except Exception as e:
        logger.error(f"Application error: {e}")
        display_error(str(e))
        sys.exit(1)

    sys.exit(0)
