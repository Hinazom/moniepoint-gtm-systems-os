
from pathlib import Path
from datetime import datetime
import argparse
import difflib
import hashlib
import json
import os
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent

WORK_LOG = ROOT / "work-log"
OUTPUT = WORK_LOG / "retrospective-audit.md"
STATE_FILE = WORK_LOG / ".audit-state.json"

MAX_DIFF_FILE_SIZE = 1_000_000  # 1 MB
MAX_DIFF_LINES = 300
EVENT_DEBOUNCE_SECONDS = 0.75

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
}

EXCLUDED_FILES = {
    ".env",
    "retrospective-audit.md",
    ".audit-state.json",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
    ".swp",
    ".DS_Store",
    ".pem",
    ".key",
}

# Files with these extensions are treated as text for diffs.
TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".sh", ".sql", ".csv",
    ".html", ".css", ".js", ".ts", ".xml", ".gitignore",
}


# ============================================================
# GENERAL HELPERS
# ============================================================

def timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def relative_path(path):
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return None


def should_ignore(path):
    path = Path(path)

    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True

    if path.name in EXCLUDED_FILES:
        return True

    if path.name.startswith(".env"):
        return True

    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True

    return False


def is_text_file(path):
    return Path(path).suffix.lower() in TEXT_EXTENSIONS


def git_command(*args):
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
    except (subprocess.SubprocessError, OSError):
        pass

    return None


def file_hash(path):
    digest = hashlib.sha256()

    try:
        with open(path, "rb") as file:
            for chunk in iter(lambda: file.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except (OSError, PermissionError):
        return None


def read_text(path):
    path = Path(path)

    try:
        if path.stat().st_size > MAX_DIFF_FILE_SIZE:
            return None

        if not is_text_file(path):
            return None

        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def append_to_report(lines):
    WORK_LOG.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines))
        file.write("\n")


# ============================================================
# HISTORICAL AUDIT
# Runs once. Existing report content is preserved.
# ============================================================

BASELINE_MARKER = "<!-- RETROSPECTIVE BASELINE CAPTURED -->"


def generate_retrospective_audit():
    WORK_LOG.mkdir(parents=True, exist_ok=True)

    existing = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""

    if BASELINE_MARKER in existing:
        print("Retrospective baseline already exists. Preserving it.")
        return

    history = git_command(
        "log", "--all", "--reverse",
        "--date=iso-strict",
        "--format=COMMIT%x09%H%x09%aI%x09%cI%x09%s",
        "--name-status"
    )

    reflog = git_command(
        "reflog", "--all",
        "--date=iso-strict",
        "--format=%gd%x09%gs"
    )

    status = git_command("status", "--short")

    file_records = []

    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [
            directory for directory in dirs
            if directory not in EXCLUDED_DIRS
        ]

        for filename in files:
            path = Path(folder) / filename

            if should_ignore(path):
                continue

            try:
                stat = path.stat()
                created = getattr(stat, "st_birthtime", None)

                file_records.append({
                    "path": relative_path(path),
                    "created": (
                        datetime.fromtimestamp(created)
                        .astimezone().isoformat(timespec="seconds")
                        if created else "Unavailable"
                    ),
                    "modified": datetime.fromtimestamp(
                        stat.st_mtime
                    ).astimezone().isoformat(timespec="seconds"),
                    "size": stat.st_size,
                })
            except OSError:
                continue

    report = [
        "",
        BASELINE_MARKER,
        "",
        "## Retrospective Baseline",
        "",
        f"Captured: {timestamp()}",
        "",
        "This section records historical evidence available when "
        "automatic monitoring was first configured.",
        "",
        "### 1. Git Commit History",
        "",
        "Author and committer timestamps are shown separately.",
        "",
    ]

    if history:
        for line in history.splitlines():
            if line.startswith("COMMIT\t"):
                parts = line.split("\t", 4)

                if len(parts) == 5:
                    _, commit, author_date, committer_date, subject = parts
                    report.extend([
                        f"#### {subject}",
                        f"- Commit: `{commit}`",
                        f"- Author timestamp: {author_date}",
                        f"- Committer timestamp: {committer_date}",
                    ])

            elif line.strip():
                report.append(f"- Changed file: `{line}`")
    else:
        report.append("Git history could not be retrieved.")

    report.extend([
        "",
        "### 2. Local Git Reflog",
        "",
    ])

    if reflog:
        report.extend(reflog.splitlines())
    else:
        report.append("No reflog information available.")

    report.extend([
        "",
        "### 3. Current File-System Inventory",
        "",
        "| File | Created (if available) | Last modified | Size (bytes) |",
        "|---|---|---|---:|",
    ])

    for record in sorted(file_records, key=lambda item: item["modified"]):
        report.append(
            f"| `{record['path']}` | {record['created']} "
            f"| {record['modified']} | {record['size']} |"
        )

    report.extend([
        "",
        "### 4. Git Working-Tree Status",
        "",
        "```text",
        status or "No uncommitted changes reported.",
        "```",
        "",
        "### Historical Audit Limitations",
        "",
        "- Git history records committed changes, not every edit.",
        "- Reflog records local Git reference movements, not every action.",
        "- File timestamps are evidence, not proof of when or how a change occurred.",
        "- Deleted files may be visible in Git history but absent from the current inventory.",
        "- Actions that left no surviving evidence cannot be reconstructed.",
        "",
    ])

    append_to_report(report)

    print(f"Retrospective baseline appended to: {OUTPUT}")
    print(f"Files inventoried: {len(file_records)}")


# ============================================================
# LIGHTWEIGHT STATE
# Stores metadata, not copies of project files.
# ============================================================

def load_state():
    if not STATE_FILE.exists():
        return {}

    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(state):
    WORK_LOG.mkdir(parents=True, exist_ok=True)

    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )
    temporary.replace(STATE_FILE)


def get_metadata(path):
    try:
        stat = Path(path).stat()

        return {
            "size": stat.st_size,
            "modified_ns": stat.st_mtime_ns,
        }
    except OSError:
        return None


def scan_current_files():
    current = {}

    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [
            directory for directory in dirs
            if directory not in EXCLUDED_DIRS
        ]

        for filename in files:
            path = Path(folder) / filename

            if should_ignore(path):
                continue

            relative = relative_path(path)
            metadata = get_metadata(path)

            if relative and metadata:
                current[relative] = metadata

    return current


def reconcile_after_restart(state):
    """
    Detects metadata changes that happened while monitoring was offline.
    It cannot reconstruct the exact contents of changes missed during downtime.
    """

    current = scan_current_files()
    previous = state.get("files", {})

    changes = []

    for path, metadata in current.items():
        old = previous.get(path)

        if old is None:
            changes.append((path, "Detected new file during downtime"))

        elif old != metadata:
            changes.append((path, "Detected modification during downtime"))

    for path in previous:
        if path not in current:
            changes.append((path, "File missing since previous monitoring session"))

    if changes:
        lines = [
            "",
            "## Changes Detected During Monitoring Downtime",
            "",
            f"Reconciled: {timestamp()}",
            "",
            "These changes were detected from file metadata. Their exact "
            "contents may not be recoverable.",
            "",
        ]

        for path, description in changes:
            lines.append(f"- **{description}:** `{path}`")

        lines.append("")
        append_to_report(lines)

        print(f"Downtime reconciliation: {len(changes)} changes detected.")

    state["files"] = current
    save_state(state)


# ============================================================
# CHANGE RECORDING
# ============================================================

class ProjectChangeHandler(FileSystemEventHandler):

    def __init__(self, state):
        self.state = state
        self.previous_text = {}
        self.last_event = {}

        # Load small text files into memory for change comparisons.
        # These contents are not saved as duplicate files on disk.
        for relative in state.get("files", {}):
            content = read_text(ROOT / relative)

            if content is not None:
                self.previous_text[relative] = content

    def record_change(self, path, event_type, old_path=None):
        relative = relative_path(path)

        if not relative or should_ignore(Path(relative)):
            return

        now = time.time()
        last = self.last_event.get(relative, 0)

        if now - last < EVENT_DEBOUNCE_SECONDS:
            return

        self.last_event[relative] = now

        path = Path(path)

        if event_type == "deleted" or not path.exists():
            self.record_deletion(relative)
            return

        metadata = get_metadata(path)

        if metadata is None:
            return

        digest = file_hash(path)
        new_text = read_text(path)
        old_text = self.previous_text.get(relative)

        lines = [
            "",
            f"## File {event_type.capitalize()}",
            "",
            f"- **Detected:** {timestamp()}",
            f"- **Path:** `{relative}`",
            f"- **Size:** {metadata['size']:,} bytes",
            f"- **SHA-256:** `{digest or 'Unavailable'}`",
        ]

        if old_path:
            old_relative = relative_path(old_path)
            if old_relative:
                lines.append(f"- **Previous path:** `{old_relative}`")
                self.previous_text.pop(old_relative, None)
                self.state.get("files", {}).pop(old_relative, None)

        if old_text is not None and new_text is not None:
            diff = list(difflib.unified_diff(
                old_text.splitlines(),
                new_text.splitlines(),
                fromfile="previous",
                tofile="current",
                lineterm=""
            ))

            if diff:
                if len(diff) > MAX_DIFF_LINES:
                    diff = diff[:MAX_DIFF_LINES]
                    diff.append("... diff truncated ...")

                lines.extend([
                    "",
                    "### Text Change",
                    "",
                    "```diff",
                    *diff,
                    "```",
                ])

        elif new_text is not None:
            lines.extend([
                "",
                "### Content Capture",
                "",
                "No previous in-memory version was available for comparison.",
            ])

        else:
            lines.extend([
                "",
                "### Content Capture",
                "",
                "Content diff skipped. File is binary, too large or unreadable.",
            ])

        lines.append("")

        append_to_report(lines)

        if new_text is not None:
            self.previous_text[relative] = new_text
        else:
            self.previous_text.pop(relative, None)

        self.state.setdefault("files", {})[relative] = metadata
        save_state(self.state)

        print(f"Recorded {event_type}: {relative}")

    def record_deletion(self, relative):
        self.previous_text.pop(relative, None)
        self.state.setdefault("files", {}).pop(relative, None)

        append_to_report([
            "",
            "## File Deleted",
            "",
            f"- **Detected:** {timestamp()}",
            f"- **Path:** `{relative}`",
            "",
        ])

        save_state(self.state)
        print(f"Recorded deletion: {relative}")

    def on_created(self, event):
        if not event.is_directory:
            self.record_change(event.src_path, "created")

    def on_modified(self, event):
        if not event.is_directory:
            self.record_change(event.src_path, "modified")

    def on_deleted(self, event):
        if not event.is_directory:
            self.record_change(event.src_path, "deleted")

    def on_moved(self, event):
        if not event.is_directory:
            self.record_change(
                event.dest_path,
                "moved",
                old_path=event.src_path
            )


# ============================================================
# WATCHER
# ============================================================

def start_monitoring():
    print("Starting Moniepoint GTM Systems OS file monitor.")
    print(f"Project folder: {ROOT}")
    print("Monitoring project file changes. Press Ctrl+C to stop.")

    state = load_state()

    if "files" not in state:
        state["files"] = scan_current_files()
        save_state(state)
    else:
        reconcile_after_restart(state)

    handler = ProjectChangeHandler(state)
    observer = Observer()
    observer.schedule(handler, str(ROOT), recursive=True)
    observer.start()

    append_to_report([
        "",
        "## Automatic File Monitoring Started",
        "",
        f"- **Started:** {timestamp()}",
        "- **Scope:** Project folder changes only.",
        "- **Git internals, secrets, caches and audit outputs:** Excluded.",
        "- **Storage:** Metadata and hashes, with small text diffs where available.",
        "",
    ])

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file monitor.")
    finally:
        observer.stop()
        observer.join()

        append_to_report([
            "",
            "## Automatic File Monitoring Stopped",
            "",
            f"- **Stopped:** {timestamp()}",
            "",
        ])


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Moniepoint GTM Systems OS audit and file monitor"
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Start continuous project-folder monitoring"
    )

    args = parser.parse_args()

    generate_retrospective_audit()

    if args.watch:
        start_monitoring()
    else:
        print("")
        print("Retrospective audit completed.")
        print("To start automatic monitoring, run:")
        print("python retrospective_audit.py --watch")


if __name__ == "__main__":
    main()
