"""Simple logger setup using rich logging."""
from rich.logging import RichHandler
import logging

def get_logger(name: str = "hermes" ) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    return logging.getLogger(name)