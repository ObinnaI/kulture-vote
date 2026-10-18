# Kulture Night

A tiny voting page for a music video night. Four friends spend points across the
["Kulture" YouTube playlist](https://www.youtube.com/playlist?list=PLZo9Bl-J-gqQ2Xyf1IMfnk-GZc2Y7zi4P)
and the host tallies the ballots to decide what gets played.

Live at https://obinnai.github.io/kulture-vote/

No backend, no accounts. Votes travel as a short ballot code pasted into the group chat.

## How to vote

1. Open the page, type your name.
2. You have **100 points**. Put up to **10 on any single video**. Tap a row's number to max it.
3. Tap **★ We must** on the one video you need on the big screen. It is locked in regardless of points.
4. Use the content-type chips (Music videos, Live, Dance, Comedy, Talk shows, Other) and search to find things.
5. Tap **Copy ballot** and paste the code (or the share link) into the group chat.

## How the host tallies

1. Open the page, **Results** tab.
2. Paste the whole group chat into the box and tap **Add ballots**. Codes are picked out automatically.
   Tapping a friend's share link also adds their ballot.
3. Set how many videos to watch with the slider. The list shows total points, who voted, and running time.
4. **YouTube queue** opens the chosen videos in order as a YouTube playlist. **Copy list** gives a text version.

## Selection rules

- Each person's **★ We must** video is locked in. If someone didn't pick one, their highest-pointed
  video takes that slot (ties go to playlist order).
- Remaining slots fill by total points.
- Ties: more distinct voters wins, then the higher single vote, then playlist order.
- "Best for last" reverses the play order so the night builds to #1.

Ballots and draft votes are saved in the browser, so closing the tab is fine.

## Staying in sync with the playlist

A GitHub Action (`.github/workflows/refresh.yml`) re-reads the playlist every 6 hours and
commits a new `videos.json` + `index.html` only when the list actually changed. Ballot codes
reference YouTube video IDs (`KV2|Name|<videoId>:<points>,…|<mustVideoId>`), so adding, removing or reordering
videos never shifts anyone's votes. Picks for videos that have since left the playlist are skipped
with a note. Run it by hand from the Actions tab ("Refresh playlist" → Run workflow).

## Content types

`categories.json` hand-sorts videos by id into `music`, `live`, `dance`, `comedy`, `talk` or `other`.
Anything not listed is auto-sorted from its title by `scripts/fetch_playlist.py` (new playlist additions
included). To fix a wrong label, add the video id to `categories.json` and rebuild.

## Editing the page

`src/index.html` is the source; `index.html` is generated from it with the playlist data inlined.
After editing the template:

```bash
python3 scripts/fetch_playlist.py --build-only
```

To refresh the data locally too (needs `pip install yt-dlp`):

```bash
python3 scripts/fetch_playlist.py
```
