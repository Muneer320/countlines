"""Parallel line counter — counts lines in files using thread pools."""

import os
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from rich.console import Console
from rich.live import Live
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

from countlines.config import CHUNK_SIZE, DEFAULT_WORKERS, LIVE_RECENT_MAX

console = Console()


def fast_count(file_path: Path) -> int:
    """Count newlines in a file using chunked binary reading.

    Args:
        file_path: Path to the file.

    Returns:
        Number of lines in the file, or 0 on error.
    """
    try:
        with file_path.open("rb") as f:
            return sum(
                chunk.count(b"\n")
                for chunk in iter(lambda: f.read(CHUNK_SIZE), b"")
            )
    except (OSError, PermissionError, UnicodeError):
        return 0


def count_lines(
    files: List[Path],
    workers: Optional[int] = None,
    verbose: bool = True,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> Tuple[int, Dict[str, int], Dict[str, int]]:
    """Count lines in a list of files using parallel workers.

    Args:
        files: List of file paths to count.
        workers: Number of worker threads (default: CPU count × 2, capped at 32).
        verbose: Show progress bars and live display.
        progress_callback: Optional callback(completed, total) for external tracking.

    Returns:
        Tuple of (total_lines, ext_stats, dir_stats).
        - ext_stats: dict mapping file extension → total lines
        - dir_stats: dict mapping directory → total lines
    """
    if workers is None:
        workers = DEFAULT_WORKERS

    total = 0
    ext_stats: Dict[str, int] = defaultdict(int)
    dir_stats: Dict[str, int] = defaultdict(int)

    if not files:
        return total, dict(ext_stats), dict(dir_stats)

    if not verbose:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(fast_count, f): f for f in files}
            for future in as_completed(futures):
                f = futures[future]
                lines = future.result()
                total += lines
                if lines > 0:
                    ext = f.suffix.lower() or "(no ext)"
                    ext_stats[ext] += lines
                    dir_stats[str(f.parent)] += lines

        return total, dict(ext_stats), dict(dir_stats)

    # Verbose mode with rich progress
    last_files: deque[str] = deque(maxlen=LIVE_RECENT_MAX)

    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[green]Processing...", total=len(files))

        with Live(console=console, refresh_per_second=10) as live:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(fast_count, f): f for f in files}

                completed = 0
                for future in as_completed(futures):
                    f = futures[future]
                    lines = future.result()
                    total += lines
                    completed += 1

                    if lines > 0:
                        ext = f.suffix.lower() or "(no ext)"
                        ext_stats[ext] += lines
                        dir_stats[str(f.parent)] += lines

                    last_files.append(str(f))
                    progress.update(task, advance=1)
                    if progress_callback:
                        progress_callback(completed, len(files))

                    table = Table(title="Live Activity")
                    table.add_column("Recent Files", style="cyan")
                    for lf in last_files:
                        table.add_row(lf[-80:])
                    live.update(table)

    return total, dict(ext_stats), dict(dir_stats)
