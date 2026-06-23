# codelines ⚡

[![PyPI version](https://img.shields.io/pypi/v/codelines)](https://pypi.org/project/codelines/)
[![Python 3.9+](https://img.shields.io/pypi/pyversions/codelines)](https://pypi.org/project/codelines/)
[![Downloads](https://img.shields.io/pypi/dm/codelines)](https://pypi.org/project/codelines/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Muneer320/countlines/pulls)

> *"How many lines of code is this thing, anyway?"*
>
> The question that keeps tech leads up at night. The question that fuels endless Slack debates about "what counts as a line." The question that `codelines` answers in milliseconds while your coworkers are still arguing about whether blank lines should be included.

---

## 🎭 The Problem

You just inherited a monorepo. The `README` says *"lightweight microservice architecture"* but `node_modules` has 87,000 files and there's a `backup-final-v2-old (copy).py` somewhere. You need numbers. Cold, hard, undeniable numbers.

You try `wc -l`. It counts `package-lock.json`. It counts `dist/`. It doesn't know what a `.gitignore` is. It stares back at you with the blank expression of a tool that peaked in 1971.

**Enter codelines.**

---

## ⚡ What It Does

```
$ codelines .

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
┌───────────┬─────────┬────────┐
│ Extension │ Lines   │      % │
├───────────┼─────────┼────────┤
│ .py       │ 52,341  │  42.0  │
│ .js       │ 28,912  │  23.2  │
│ .ts       │ 18,234  │  14.6  │
│ .css      │ 12,567  │  10.1  │
│ .html     │  8,901  │   7.1  │
└───────────┴─────────┴────────┘
```

**It's fast.** Multi-threaded. Uses all your cores. Respects `.gitignore`. Gives you beautiful tables, JSON, or CSV. And it makes you look like you know exactly what's going on — even when you don't.

---

## 📦 Installation

```bash
pip install codelines
```

That's it. No system dependencies. No Docker. No "just clone and run these 47 scripts." One command. You're counting.

```bash
$ codelines --version
codelines 0.1.0
```

---

## 🚀 Quick Start

```bash
# The basics
codelines .                              # Count current directory
codelines ~/projects/monorepo            # Point it anywhere

# Get nerdy
codelines . --format json                # Machine-readable output
codelines . --format csv                 # Spreadsheet-ready
codelines . --include .py .rs .go        # Only the languages you care about
codelines . --exclude .json .lock        # Skip the noise
codelines . --max-depth 3                # Don't go too deep, man
codelines . --sort-by ext --top 10       # Top 10 extensions, sorted
codelines . --workers 16                 # Unleash the cores
codelines . --quiet                      # I don't need the show, just the numbers
```

---

## 🎮 Full Command Reference

```
Usage: codelines [OPTIONS] [DIRECTORY]

Arguments:
  directory                Directory to scan (default: current directory)

Options:
  --format, -f   [table|json|csv]     Output format (default: table)
  --include, -i  EXT [EXT ...]        Only count these extensions
  --exclude, -e  EXT [EXT ...]        Skip these extensions
  --max-depth, -d N                   Maximum directory depth
  --workers, -w  N                   Worker threads (default: CPU × 2)
  --ignore-file  PATH                Additional ignore file
  --sort-by, -s  [ext|dir|lines]     Sort criterion (default: lines)
  --top, -t      N                   Show top N results (default: 5)
  --quiet, -q                        Suppress progress display
  --version, -V                      Show version and exit
  --help, -h                         Show this message
```

---

## 🧠 The Philosophy

### What counts as a "line"?

A line is a `\n` character. If your file has newlines, we count them. No opinions. No debates. No "but what about docstrings?" Just the raw, unfiltered truth your files are telling you.

### What files get counted?

By default, we recognize **40+ code file extensions** — Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, HTML, CSS, JSON, YAML, Markdown, Shell, SQL, and more. You can add or remove extensions with `--include` and `--exclude`.

### What gets ignored?

We automatically read your `.gitignore` and `.ignore` files. Got `node_modules`? Skipped. `.venv`? Skipped. `__pycache__`? Skipped. We also eat our own dog food — the scanner itself is lightning fast because it skips boring directories before even looking at files.

---

## 🏗 Architecture (for the curious)

```
Ask for a directory
        │
        ▼
  ┌─────────────┐
  │   Scanner   │  ← Walks the tree, applies .gitignore, respect depth limits
  └──────┬──────┘
         │ list of Path objects
         ▼
  ┌─────────────┐
  │  Thread Pool │ ← min(32, CPU×2) workers, chunked binary reads (1 MiB)
  │  Dispatcher  │
  └──────┬──────┘
         │ per-file line counts
         ▼
  ┌─────────────┐
  │  Aggregator  │ ← Groups by extension, directory, computes percentages
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │  Reporter    │ ← table (Rich), JSON, or CSV — your choice
  └─────────────┘
```

No temporary files. No database. No config file to manage. Just a pure pipeline from filesystem to your eyeballs.

---

## 🔥 Real-World Speed

| Scenario | Files | Lines | Time |
|----------|-------|-------|------|
| Small project (codelines itself) | 11 | 1,230 | <0.1s |
| Medium monorepo | 2,500 | 180,000 | ~0.5s |
| Large repo (Hermes Agent) | 87,000 | 17,000,000 | ~3s |

*Benchmarked on a 4-core VPS. Your speeds may vary — usually faster on real hardware.*

---

## 🤝 But Why?

Because `wc -l` doesn't know what a gitignore is. Because counting lines shouldn't require a shell pipeline that looks like a cat walked across your keyboard. Because developers deserve tools that are fast, pretty, and don't make them think about edge cases.

And honestly? Because it was fun to build.

---

## 🛠 Built With

- [Rich](https://github.com/Textualize/rich) — the terminal UI library that makes CLI apps feel like magic
- Python's `ThreadPoolExecutor` — because blocking I/O is for people with infinite patience
- `pathlib` — because string concatenation for file paths is a crime
- Pure Python — zero native dependencies, installs anywhere

---

## 📄 License

MIT © [Muneer Alam](https://github.com/Muneer320)

---

<p align="center">
  <sub>built with excessive coffee and mild obsession with counting things</sub>
</p>
