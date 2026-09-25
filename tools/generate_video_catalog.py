"""Build the static video catalogue used by the GitHub Pages site."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "videos.json"
MEDIA_ROOT = (
    "https://media.githubusercontent.com/media/Enrique1987/"
    "no_technical_stuff/refs/heads/main"
)

CATEGORIES = {
    "martial-arts_contact-sport/bjj/videos/README.md": ("bjj", "BJJ"),
    "martial-arts_contact-sport/judo/videos/README.md": ("judo", "Judo"),
    "martial-arts_contact-sport/grappling/videos/README.md": (
        "grappling",
        "Grappling",
    ),
    "fitness/calisthenics/videos/README.md": ("calisthenics", "Calisthenics"),
    "food/fit-food/videos/README.md": ("fit-food", "Savoury and fit food"),
    "food/sweets/videos/README.md": ("sweets", "Sweet food"),
    "health/videos/README.md": ("health", "Health and mobility"),
    "magic/videos/README.md": ("magic", "Magic"),
    "ai/videos/README.md": ("ai", "Artificial intelligence"),
    "upbringing/videos/README.md": ("upbringing", "Parenting"),
}

ROW = re.compile(
    r"^\| \[([^]]+\.mp4)\]\(([^)]+\.mp4)\) "
    r"\| (?:\[Watch online\]\([^)]+\) \| )?"
    r"([^|]+) \| \[Instagram\]\(([^)]+)\) \| ([^|]+) \|"
)


def main() -> None:
    videos: list[dict[str, str]] = []
    for readme_name, (category_id, category_label) in CATEGORIES.items():
        readme = ROOT / readme_name
        for line in readme.read_text(encoding="utf-8").splitlines():
            match = ROW.match(line)
            if not match:
                continue
            filename, relative_video, creator, instagram, topic = match.groups()
            repo_path = (readme.parent.relative_to(ROOT) / relative_video).as_posix()
            videos.append(
                {
                    "id": filename.removesuffix(".mp4"),
                    "filename": filename,
                    "category": category_id,
                    "categoryLabel": category_label,
                    "creator": creator.strip(),
                    "topic": topic.strip(),
                    "instagram": instagram,
                    "repoPath": repo_path,
                    "mediaUrl": f"{MEDIA_ROOT}/{repo_path}",
                }
            )

    videos.sort(key=lambda video: (video["categoryLabel"], video["topic"]))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(videos, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(videos)} videos to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
