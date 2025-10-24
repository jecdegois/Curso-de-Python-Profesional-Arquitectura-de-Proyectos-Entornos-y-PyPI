"""Main entry point for Platzi News."""

import asyncio

from .io.cli import main as async_main


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
