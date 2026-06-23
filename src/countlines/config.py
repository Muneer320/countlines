"""Default configuration and constants for countlines."""

import os
from pathlib import Path
from typing import Set

# Chunk size for reading files (1 MiB)
CHUNK_SIZE: int = 1024 * 1024

# Default file extensions to count
CODE_EXTENSIONS: Set[str] = {
    ".py", ".pyx", ".pyi",
    ".js", ".jsx", ".mjs", ".cjs",
    ".ts", ".tsx",
    ".cpp", ".c", ".h", ".hpp", ".cc", ".cxx",
    ".java", ".kt", ".kts",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".swift",
    ".scala",
    ".html", ".htm",
    ".css", ".scss", ".sass", ".less",
    ".json", ".jsonc",
    ".yaml", ".yml",
    ".toml",
    ".xml",
    ".md", ".mdx", ".rst",
    ".sh", ".bash", ".zsh",
    ".bat", ".cmd", ".ps1",
    ".sql",
    ".graphql", ".gql",
    ".proto",
    ".lua",
    ".r",
    ".dart",
    ".ex", ".exs",
    ".erl", ".hrl",
    ".hs",
    ".clj", ".cljs", ".edn",
    ".elm",
    ".vue", ".svelte",
    ".tf", ".tfvars",
    ".dockerfile",
    ".makefile", ".mk",
    ".cmake",
}

# Default workers = 2x CPU cores, capped at 32
DEFAULT_WORKERS: int = min(32, (os.cpu_count() or 4) * 2)

# Default number of top entries to show
DEFAULT_TOP_N: int = 5

# Max recent entries to show in live display
LIVE_RECENT_MAX: int = 5
