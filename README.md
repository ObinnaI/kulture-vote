# Kulture Night

A tiny voting page for a music video night. Four friends spend points across the
["Kulture" YouTube playlist](https://www.youtube.com/playlist?list=PLZo9Bl-J-gqQ2Xyf1IMfnk-GZc2Y7zi4P)
and the host tallies the ballots to decide what gets played.

No backend, no accounts. Votes travel as a short ballot code pasted into the group chat.

## How to vote

1. Open the page, type your name.
2. You have **100 points**. Put up to **10 on any single video**.
3. Tap **Copy ballot** and paste the code (or the share link) into the group chat.

## How the host tallies

1. Open the page, **Results** tab.
2. Paste the whole group chat into the box and tap **Add ballots**. Codes are picked out automatically.
   Tapping a friend's share link also adds their ballot.
3. Set how many videos to watch with the slider. The list shows total points, who voted, and running time.
4. **Open as YouTube queue** opens the chosen videos in order as a YouTube playlist. **Copy list** gives a text version.

## Selection rules

- Each person's single highest-pointed video is locked in (the ★ "golden pick").
- Remaining slots fill by total points.
- Ties: more distinct voters wins, then the higher single vote, then playlist order.
- "Save the best for last" reverses the play order so the night builds to #1.

Ballots and draft votes are saved in the browser, so closing the tab is fine.

## Refreshing the playlist

```bash
pip install yt-dlp
python3 scripts/fetch_playlist.py
```

This rewrites `videos.json` and inlines it into `index.html`.
