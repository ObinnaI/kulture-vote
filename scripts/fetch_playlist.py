#!/usr/bin/env python3
"""Refresh videos.json from the YouTube playlist and build index.html from src/index.html.

Usage:
  python3 scripts/fetch_playlist.py                 # runs yt-dlp, updates videos.json, builds index.html
  python3 scripts/fetch_playlist.py --raw dump.json # use an existing `yt-dlp --flat-playlist -J` dump
  python3 scripts/fetch_playlist.py --build-only    # just rebuild index.html from videos.json

Requires yt-dlp on PATH (pip install yt-dlp) unless --raw/--build-only is given.
videos.json's "updated" stamp only changes when the list of videos changes, so a scheduled
run that finds nothing new leaves the repo untouched.
"""
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

PLAYLIST = "https://www.youtube.com/playlist?list=PLZo9Bl-J-gqQ2Xyf1IMfnk-GZc2Y7zi4P"
ROOT = Path(__file__).resolve().parent.parent
VIDEOS = ROOT / "videos.json"
TEMPLATE = ROOT / "src" / "index.html"
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
    return vids


def build(data):
    html = TEMPLATE.read_text()
    block = f'{START}<script id="videos" type="application/json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>{END}'
    new, n = re.subn(re.escape(START) + r".*?" + re.escape(END), lambda _: block, html, flags=re.S)
    if n != 1:
        sys.exit("src/index.html is missing the VIDEOS markers")
    INDEX.write_text(new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw")
    ap.add_argument("--build-only", action="store_true")
    a = ap.parse_args()
    old = json.loads(VIDEOS.read_text()) if VIDEOS.exists() else {}
    if a.build_only:
        data = old
    else:
        raw = json.loads(Path(a.raw).read_text()) if a.raw else fetch_raw()
        vids = to_videos(raw)
        if not vids:
            sys.exit("playlist came back empty; leaving files alone")
        changed = vids != old.get("videos")
        data = {
            "title": raw.get("title") or old.get("title") or "Playlist",
            "url": PLAYLIST,
            "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if changed or not old.get("updated") else old["updated"],
            "videos": vids,
        }
        if data != old:
            VIDEOS.write_text(json.dumps(data, ensure_ascii=False, indent=1))
        print("playlist changed" if changed else "playlist unchanged")
    build(data)
    print(f"{len(data['videos'])} videos; built index.html")


if __name__ == "__main__":
    main()
