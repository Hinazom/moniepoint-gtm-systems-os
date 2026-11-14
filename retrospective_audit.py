
from pathlib import Path
from datetime import datetime
import subprocess
import os

ROOT = Path.cwd()
OUTPUT = ROOT / "work-log" / "retrospective-audit.md"

def git_command(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout

# 1. Git commit history, including files changed in each commit
history = git_command(
    "log", "--all", "--reverse",
    "--date=iso-strict",
    "--format=COMMIT%x09%H%x09%aI%x09%cI%x09%s",
    "--name-status"
)

# 2. Local Git reference history
reflog = git_command(
    "reflog", "--all",
    "--date=iso-strict",
    "--format=%gd%x09%gs"
)

# 3. Current file-system timestamps
file_records = []

excluded = {".git", ".venv", "__pycache__"}

for folder, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in excluded]

    for filename in files:
        path = Path(folder) / filename
        relative = path.relative_to(ROOT)

        if filename == ".env":
            continue

        try:
            stat = path.stat()
            created = getattr(stat, "st_birthtime", None)

            file_records.append({
                "path": str(relative),
                "created": (
                    datetime.fromtimestamp(created).astimezone().isoformat()
                    if created else "Unavailable"
                ),
                "modified": datetime.fromtimestamp(
                    stat.st_mtime
                ).astimezone().isoformat()
            })
        except OSError:
            pass

# 4. Current working-tree status
status = git_command("status", "--short")

# Assemble report
report = [
    "# Moniepoint GTM Systems OS: Retrospective Activity Audit",
    "",
    f"Generated: {datetime.now().astimezone().isoformat()}",
    "",
    "## 1. Git Commit History",
    "",
    "Author and committer timestamps are shown separately.",
    "",
]

if history:
    for line in history.splitlines():
        if line.startswith("COMMIT\t"):
            _, commit, author_date, committer_date, subject = (
                line.split("\t", 4)
            )
            report.append(f"### {subject}")
            report.append(f"- Commit: `{commit}`")
            report.append(f"- Author timestamp: {author_date}")
            report.append(f"- Committer timestamp: {committer_date}")
        elif line.strip():
            report.append(f"- Changed file: `{line}`")
else:
    report.append("Git history could not be retrieved.")

report.extend([
    "",
    "## 2. Local Git Reflog",
    ""
])

if reflog:
    report.extend(reflog.splitlines())
else:
    report.append("No reflog information available.")

report.extend([
    "",
    "## 3. Current File-System Timestamps",
    "",
    "| File | Created (if available) | Last modified |",
    "|---|---|---|"
])

for record in sorted(file_records, key=lambda x: x["modified"]):
    report.append(
        f"| `{record['path']}` | {record['created']} "
        f"| {record['modified']} |"
    )

report.extend([
    "",
    "## 4. Current Git Status",
    "",
    "```text",
    status or "No uncommitted changes reported.",
    "```",
    "",
    "## Important limitations",
    "",
    "- Commit timestamps do not establish exact GitHub push times.",
    "- File creation and modification timestamps can change when files "
    "are copied, downloaded or edited.",
    "- Deleted files may not appear in the current file-system inventory, "
    "but can appear in Git history.",
    "- Reflog records local Git reference movements, not every action "
    "performed in the repository.",
    ""
])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(report), encoding="utf-8")

print(f"Audit generated: {OUTPUT}")
print(f"Current files inspected: {len(file_records)}")
print("Review the report before using its timestamps in your Build Log.")
