"""countlines — A blazing-fast, parallel Lines of Code counter."""

__version__ = "0.1.0"
__author__ = "Muneer Alam"
__license__ = "MIT"

from countlines.scanner import collect_files
from countlines.counter import count_lines
from countlines.ignore import load_ignore_patterns
from countlines.reporters import format_output

__all__ = [
    "__version__",
    "collect_files",
    "count_lines",
    "load_ignore_patterns",
    "format_output",
]
