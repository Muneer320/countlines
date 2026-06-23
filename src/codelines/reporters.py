"""Output formatters — table (Rich), JSON, and CSV."""

import csv
import io
import json
from typing import Dict, List, Tuple

from rich.console import Console
from rich.table import Table

console = Console()


def top_n(d: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    """Return top N entries from a dict, sorted by value descending."""
    return sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]


def format_output(
    *,
    fmt: str,
    total_lines: int,
    total_files: int,
    workers: int,
    skipped_dirs: int,
    skipped_files: int,
    ext_stats: Dict[str, int],
    dir_stats: Dict[str, int],
    top: int = 5,
    sort_by: str = "lines",
) -> str:
    """Format the results in the requested output format.

    Args:
        fmt: Output format — 'table', 'json', or 'csv'.
        total_lines: Total lines counted.
        total_files: Total files processed.
        workers: Number of worker threads used.
        skipped_dirs: Number of skipped directories.
        skipped_files: Number of skipped files.
        ext_stats: Extension → lines mapping.
        dir_stats: Directory → lines mapping.
        top: Number of top entries to show.
        sort_by: Sort criterion — 'ext', 'dir', or 'lines'.

    Returns:
        Formatted output string (for 'table' format, prints directly and returns '').
    """
    if fmt == "json":
        return _format_json(
            total_lines=total_lines,
            total_files=total_files,
            workers=workers,
            skipped_dirs=skipped_dirs,
            skipped_files=skipped_files,
            ext_stats=ext_stats,
            dir_stats=dir_stats,
            top=top,
            sort_by=sort_by,
        )
    elif fmt == "csv":
        return _format_csv(
            total_lines=total_lines,
            total_files=total_files,
            workers=workers,
            skipped_dirs=skipped_dirs,
            skipped_files=skipped_files,
            ext_stats=ext_stats,
            dir_stats=dir_stats,
            top=top,
            sort_by=sort_by,
        )
    else:
        _format_table(
            total_lines=total_lines,
            total_files=total_files,
            workers=workers,
            skipped_dirs=skipped_dirs,
            skipped_files=skipped_files,
            ext_stats=ext_stats,
            dir_stats=dir_stats,
            top=top,
            sort_by=sort_by,
        )
        return ""


def _format_table(
    total_lines: int,
    total_files: int,
    workers: int,
    skipped_dirs: int,
    skipped_files: int,
    ext_stats: Dict[str, int],
    dir_stats: Dict[str, int],
    top: int,
    sort_by: str,
) -> None:
    """Render results as Rich tables."""
    console.print()

    # Summary table
    summary = Table(title="Summary", title_style="bold blue")
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", style="green")
    summary.add_row("Total Files (counted)", str(total_files))
    summary.add_row("Total Lines (real code)", f"{total_lines:,}")
    summary.add_row("Workers", str(workers))
    summary.add_row("Skipped Directories", str(skipped_dirs))
    summary.add_row("Skipped Files", str(skipped_files))
    console.print(summary)

    # Extension stats
    if ext_stats:
        ext_table = Table(title="Top File Types (Actual Code)", title_style="bold blue")
        ext_table.add_column("Extension", style="cyan")
        ext_table.add_column("Lines", style="green", justify="right")
        ext_table.add_column("%", style="dim", justify="right")

        for k, v in top_n(ext_stats, top):
            pct = (v / total_lines * 100) if total_lines > 0 else 0
            ext_table.add_row(k, f"{v:,}", f"{pct:.1f}")
        console.print(ext_table)

    # Directory stats
    if dir_stats:
        dir_table = Table(title="Top Directories", title_style="bold blue")
        dir_table.add_column("Directory", style="cyan")
        dir_table.add_column("Lines", style="green", justify="right")
        dir_table.add_column("%", style="dim", justify="right")

        for k, v in top_n(dir_stats, top):
            pct = (v / total_lines * 100) if total_lines > 0 else 0
            dir_table.add_row(k[-60:], f"{v:,}", f"{pct:.1f}")
        console.print(dir_table)

    console.print()


def _format_json(
    total_lines: int,
    total_files: int,
    workers: int,
    skipped_dirs: int,
    skipped_files: int,
    ext_stats: Dict[str, int],
    dir_stats: Dict[str, int],
    top: int,
    sort_by: str,
) -> str:
    """Render results as JSON."""
    result = {
        "summary": {
            "total_files": total_files,
            "total_lines": total_lines,
            "workers": workers,
            "skipped_directories": skipped_dirs,
            "skipped_files": skipped_files,
        },
        "by_extension": dict(top_n(ext_stats, top)),
        "by_directory": dict(top_n(dir_stats, top)),
    }
    return json.dumps(result, indent=2)


def _format_csv(
    total_lines: int,
    total_files: int,
    workers: int,
    skipped_dirs: int,
    skipped_files: int,
    ext_stats: Dict[str, int],
    dir_stats: Dict[str, int],
    top: int,
    sort_by: str,
) -> str:
    """Render results as CSV."""
    buf = io.StringIO()
    writer = csv.writer(buf)

    writer.writerow(["section", "key", "value"])
    writer.writerow(["summary", "total_files", total_files])
    writer.writerow(["summary", "total_lines", total_lines])
    writer.writerow(["summary", "workers", workers])
    writer.writerow(["summary", "skipped_directories", skipped_dirs])
    writer.writerow(["summary", "skipped_files", skipped_files])

    for k, v in top_n(ext_stats, top):
        writer.writerow(["by_extension", k, v])

    for k, v in top_n(dir_stats, top):
        writer.writerow(["by_directory", k, v])

    return buf.getvalue()
