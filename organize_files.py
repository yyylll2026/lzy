#!/usr/bin/env python3
"""Organize files in a directory into categorized subfolders."""

import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".md", ".xlsx", ".csv"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".sh"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Media": {".mp4", ".mov", ".mp3", ".wav", ".flac"},
}


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize(target_dir: Path, dry_run: bool = False) -> None:
    if not target_dir.is_dir():
        raise ValueError(f"Not a valid directory: {target_dir}")

    for item in target_dir.iterdir():
        if not item.is_file() or item.name.startswith("."):
            continue
        category = get_category(item.suffix)
        dest_dir = target_dir / category
        dest_path = dest_dir / item.name
        if dry_run:
            print(f"[DRY RUN] {item.name} -> {category}/")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
            print(f"Moved: {item.name} -> {category}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by extension.")
    parser.add_argument("directory", type=Path, help="Target directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    args = parser.parse_args()
    organize(args.directory, dry_run=args.dry_run)
