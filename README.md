# codelines 🚀

[![PyPI version](https://img.shields.io/pypi/v/codelines)](https://pypi.org/project/codelines/)
[![Python 3.9+](https://img.shields.io/pypi/pyversions/codelines)](https://pypi.org/project/codelines/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A blazing-fast, parallel Lines of Code counter with a beautiful terminal UI.**

Count lines of actual code in any project — respects `.gitignore` and `.ignore` files, uses multi-threaded parallel counting, and displays results in rich, interactive tables.

## Features

- ⚡ **Parallel counting** — uses all CPU cores for maximum speed
- 🎨 **Rich terminal UI** — live progress bars, spinners, and formatted tables
- 📁 **Git-aware** — automatically respects `.gitignore` and `.ignore` patterns
- 📊 **Smart stats** — breakdowns by file extension, directory, and root folder
- 🔧 **Flexible output** — table (default), JSON, CSV formats
- 🎯 **Filtering** — include/exclude specific file extensions
- 📏 **Depth control** — limit directory traversal depth

## Installation

```bash
pip install codelines
```

## Quick Start

```bash
# Count lines in current directory
codelines .

# Count lines in a specific directory
codelines ~/my-project

# Output as JSON
codelines . --format json

# Only count Python and JavaScript files
codelines . --include .py .js

# Limit to 3 levels deep
codelines . --max-depth 3
```

## Usage

```
Usage: codelines [OPTIONS] [DIRECTORY]

Options:
  --format [table|json|csv]   Output format (default: table)
  --include EXT [EXT ...]     Only count files with these extensions
  --exclude EXT [EXT ...]     Skip files with these extensions
  --max-depth N              Maximum directory depth to traverse
  --workers N                Number of worker threads (default: CPU count × 2)
  --ignore-file PATH         Additional ignore file to use
  --detail / --no-detail     Show per-file line counts (default: --no-detail)
  --sort-by [ext|dir|lines]  Sort results by (default: lines)
  --top N                    Show top N results (default: 5)
  --version                  Show version and exit
  --help                     Show this message and exit
```

## Example Output

```
                    Summary
┌─────────────────────────┬─────────┐
│ Metric                  │ Value   │
├─────────────────────────┼─────────┤
│ Total Files (counted)   │ 847     │
│ Total Lines (real code) │ 124,532 │
│ Workers                 │ 16      │
│ Skipped Directories     │ 23      │
│ Skipped Files           │ 156     │
└─────────────────────────┴─────────┘

             Top File Types (Actual Code)
┌───────────┬─────────┐
│ Extension │ Lines   │
├───────────┼─────────┤
│ .py       │ 52,341  │
│ .js       │ 28,912  │
│ .ts       │ 18,234  │
│ .css      │ 12,567  │
│ .html     │  8,901  │
└───────────┴─────────┘
```

## License

MIT © Muneer Alam
