# X Engagement Tracker

Track user engagement on an X (formerly Twitter) post in real-time.

This console-based Python script monitors a specific post and identifies users who:
- Liked the post
- Retweeted (reposted) it
- Replied to the tweet
- Followed the tweet's author

An HTML file (`draw.html`) is updated every 5 minutes with a clean grid of usernames and checkmarks.

## Features

- Tracks engagement in real-time (every 5 minutes)
- Deduplicates users across actions
- Verifies if users follow the tweet author
- Generates a stylish HTML summary with checkmarks
- Easy to run in a terminal

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/x-engagement-tracker.git
cd x-engagement-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the tracker
```bash
python x_engagement_tracker.py
```

## Output

A file called `draw.html` will be created in the directory. Open it in your browser to view the current engagement status.

## Notes

- The script only checks up to 100 replies due to API limits.
- Requires elevated access to Twitter's API v2 (Bearer Token).

## License

MIT License
