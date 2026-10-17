#!/usr/bin/env python3
"""Refresh videos.json from the YouTube playlist and inline it into index.html.

Usage:
  python3 scripts/fetch_playlist.py                 # runs yt-dlp, writes videos.json, inlines
  python3 scripts/fetch_playlist.py --raw dump.json # use an existing `yt-dlp --flat-playlist -J` dump
  python3 scripts/fetch_playlist.py --inline-only   # just re-inline videos.json into index.html

Requires yt-dlp on PATH (pip install yt-dlp) unless --raw/--inline-only is given.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

PLAYLIST = "https://www.youtube.com/playlist?list=PLZo9Bl-J-gqQ2Xyf1IMfnk-GZc2Y7zi4P"
ROOT = Path(__file__).resolve().parent.parent
VIDEOS = ROOT / "videos.json"
INDEX = ROOT / "index.html"
START = "<!--VIDEOS:START-->"
END = "<!--VIDEOS:END-->"


def fetch_raw():
    out = subprocess.run(["yt-dlp", "--flat-playlist", "-J", PLAYLIST],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def to_videos(raw):
    vids = []
    for i, e in enumerate(raw["entries"]):
        if e.get("title") in ("[Private video]", "[Deleted video]"):
            continue
        vids.append({
            "i": i,
            "id": e["id"],
            "t": e.get("title", ""),
            "c": e.get("channel") or e.get("uploader") or "",
            "d": int(e.get("duration") or 0),
        })
    return {"title": raw.get("title", "Playlist"), "url": PLAYLIST, "videos": vids}


def inline(data):
    html = INDEX.read_text()
    block = f'{START}<script id="videos" type="application/json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>{END}'
    new, n = re.subn(re.escape(START) + r".*?" + re.escape(END), lambda _: block, html, flags=re.S)
    if n != 1:
        sys.exit("index.html is missing the VIDEOS markers")
    INDEX.write_text(new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw")
    ap.add_argument("--inline-only", action="store_true")
    a = ap.parse_args()
    if a.inline_only:
        data = json.loads(VIDEOS.read_text())
    else:
        raw = json.loads(Path(a.raw).read_text()) if a.raw else fetch_raw()
        data = to_videos(raw)
        VIDEOS.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    inline(data)
    print(f"{len(data['videos'])} videos; inlined into index.html")


if __name__ == "__main__":
    main()
