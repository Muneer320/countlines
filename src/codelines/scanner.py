"""File system scanner — discovers and filters files for counting."""

import os
from collections import deque
from pathlib import Path
from typing import List, Optional, Set, Tuple

from rich.console import Console
from rich.live import Live
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

from codelines.config import CODE_EXTENSIONS, LIVE_RECENT_MAX
from codelines.ignore import should_ignore

console = Console()


def collect_files(
    folder: Path,
    ignore_patterns: Set[str],
    include_exts: Optional[Set[str]] = None,
    exclude_exts: Optional[Set[str]] = None,
    max_depth: Optional[int] = None,
    verbose: bool = True,
) -> Tuple[List[Path], List[str], int]:
    """Walk a directory and collect files matching the criteria.

    Args:
        folder: Root directory to scan.
        ignore_patterns: Patterns to ignore (from .gitignore/.ignore).
        include_exts: Only include files with these extensions (None = all).
        exclude_exts: Exclude files with these extensions.
        max_depth: Maximum directory depth relative to folder.
        verbose: Show progress bars and live display.

    Returns:
        Tuple of (files, skipped_dirs, skipped_files).
    """
    files: List[Path] = []
    skipped_dirs: List[str] = []
    skipped_files: int = 0

    # Pre-compute the root depth for max_depth calculation
    root_depth = len(folder.resolve().parts)

    last_dirs: deque[str] = deque(maxlen=LIVE_RECENT_MAX)

    # First pass: count directories for progress bar
    total_dirs = sum(len(dirs) for _, dirs, _ in os.walk(folder)) or 1

    if not verbose:
        for root, dirs, filenames in os.walk(folder):
            root_path = Path(root)

            # Depth check
            if max_depth is not None:
                current_depth = len(root_path.resolve().parts) - root_depth
                if current_depth > max_depth:
                    dirs.clear()
                    continue

            if should_ignore(root_path, ignore_patterns):
                skipped_dirs.append(str(root_path))
                dirs.clear()
                continue

            _filter_dirs(dirs, root_path, ignore_patterns, skipped_dirs)

            for name in filenames:
                fp = root_path / name
                if _include_file(fp, ignore_patterns, include_exts, exclude_exts):
                    files.append(fp)
                else:
                    skipped_files += 1

        return files, skipped_dirs, skipped_files

    # Verbose mode with progress bars
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("Scanning {task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Scanning directories...", total=total_dirs)

        with Live(console=console, refresh_per_second=10) as live:
            for root, dirs, filenames in os.walk(folder):
                root_path = Path(root)
                last_dirs.append(str(root_path))

                # Depth check
                if max_depth is not None:
                    current_depth = len(root_path.resolve().parts) - root_depth
                    if current_depth >= max_depth:
                        dirs.clear()
                        progress.update(task, advance=1)
                        continue

                if should_ignore(root_path, ignore_patterns):
                    skipped_dirs.append(str(root_path))
                    dirs.clear()
                    progress.update(task, advance=1)
                    continue

                _filter_dirs(dirs, root_path, ignore_patterns, skipped_dirs)

                for name in filenames:
                    fp = root_path / name
                    if _include_file(fp, ignore_patterns, include_exts, exclude_exts):
                        files.append(fp)
                    else:
                        skipped_files += 1

                progress.update(task, advance=1)

                # Update live view
                table = Table(title="Scanning Activity")
                table.add_column("Recent Directories", style="cyan")
                for d in last_dirs:
                    table.add_row(d[-80:])
                live.update(table)

    return files, skipped_dirs, skipped_files


def _filter_dirs(
    dirs: List[str],
    root_path: Path,
    ignore_patterns: Set[str],
    skipped_dirs: List[str],
) -> None:
    """Filter directory list in-place, removing ignored ones."""
    new_dirs = []
    for d in dirs:
        full = root_path / d
        if should_ignore(full, ignore_patterns):
            skipped_dirs.append(str(full))
        else:
            new_dirs.append(d)
    dirs[:] = new_dirs


def _include_file(
    fp: Path,
    ignore_patterns: Set[str],
    include_exts: Optional[Set[str]],
    exclude_exts: Optional[Set[str]],
) -> bool:
    """Decide whether a file should be included in counting."""
    if should_ignore(fp, ignore_patterns):
        return False

    ext = fp.suffix.lower()

    # Only count known code extensions by default, but if include_exts is
    # explicitly set, use that instead.
    if include_exts is not None:
        if ext not in include_exts:
            return False
    elif ext not in CODE_EXTENSIONS:
        return False

    if exclude_exts is not None and ext in exclude_exts:
        return False

    return True
