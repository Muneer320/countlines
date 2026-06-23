"""codelines — A blazing-fast, parallel Lines of Code counter."""

__version__ = "0.1.1"
__author__ = "Muneer Alam"
__license__ = "MIT"

from codelines.scanner import collect_files
from codelines.counter import count_lines
from codelines.ignore import load_ignore_patterns
from codelines.reporters import format_output

__all__ = [
    "__version__",
    "collect_files",
    "count_lines",
    "load_ignore_patterns",
    "format_output",
]
