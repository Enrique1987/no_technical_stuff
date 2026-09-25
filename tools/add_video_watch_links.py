"""Add direct GitHub Pages playback links to every video table."""

from __future__ import annotations

import re
from urllib.parse import quote

from generate_video_catalog import CATEGORIES, ROOT


SITE_ROOT = "https://enrique1987.github.io/no_technical_stuff/"
VIDEO_CELL = re.compile(r"^\| \[([^]]+\.mp4)\]\(([^)]+\.mp4)\) \|")
PLAYBACK_NOTE = (
    "Use **Watch online** to open the video in the browser player. "
    "The filename points to the stored Git LFS file and may download instead."
)


def watch_link(filename: str) -> str:
    video_id = filename.removesuffix(".mp4")
    return f"[Watch online]({SITE_ROOT}?video={quote(video_id)})"


def update_readme(readme_name: str) -> int:
    path = ROOT / readme_name
    lines = path.read_text(encoding="utf-8").splitlines()
    updated: list[str] = []
    added = 0
    add_separator_cell = False
    has_playback_note = PLAYBACK_NOTE in lines

    for line in lines:
        if line.startswith("| Video |") and not has_playback_note:
            if updated and updated[-1] == "":
                updated.pop()
            updated.extend(["", PLAYBACK_NOTE, ""])
            has_playback_note = True
        if line.startswith("| Video |") and "| Watch online |" not in line:
            line = line.replace("| Video |", "| Video | Watch online |", 1)
            add_separator_cell = True
        elif add_separator_cell and line.startswith("| --- |"):
            line = line.replace("| --- |", "| --- | --- |", 1)
            add_separator_cell = False

        match = VIDEO_CELL.match(line)
        if match and "| [Watch online](" not in line:
            filename = match.group(1)
            line = line.replace(match.group(0), f"{match.group(0)} {watch_link(filename)} |", 1)
            added += 1
        updated.append(line)

    path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    return added


def main() -> None:
    added = sum(update_readme(readme_name) for readme_name in CATEGORIES)
    print(f"Added {added} direct playback links across {len(CATEGORIES)} video tables")


if __name__ == "__main__":
    main()
