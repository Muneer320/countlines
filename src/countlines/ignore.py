""".gitignore / .ignore pattern loading and matching."""

from pathlib import Path
from typing import Set


def load_ignore_patterns(ignore_file: Path) -> Set[str]:
    """Load ignore patterns from a gitignore-style file.

    Args:
        ignore_file: Path to the ignore file (e.g., .gitignore, .ignore).

    Returns:
        A set of pattern strings, or an empty set if the file doesn't exist.
    """
    if not ignore_file.is_file():
        return set()

    patterns: Set[str] = set()
    with ignore_file.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.add(line.rstrip("/"))

    return patterns


def should_ignore(path: Path, ignore_patterns: Set[str]) -> bool:
    """Check if a path matches any ignore pattern.

    Args:
        path: The file or directory path to check.
        ignore_patterns: Set of gitignore-style patterns.

    Returns:
        True if the path should be ignored.
    """
    if not ignore_patterns:
        return False

    parts = set(path.parts)
    for pattern in ignore_patterns:
        if pattern in parts:
            return True
        if path.match(pattern):
            return True
        if path.match(f"{pattern}/**"):
            return True
    return False
