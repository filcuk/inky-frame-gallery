# Copy this file to gallery_config.py on the device (same directory as main.py).
# gallery_config.py is gitignored — do not commit real tokens.

# Minutes between slideshow advances (stock launcher calls ih.sleep with this).
SLIDESHOW_INTERVAL_MINUTES = 60

# Where JPEGs live on the SD card (created automatically when possible).
GALLERY_SD_FOLDER = "/sd/gallery"

# --- Online sync (gallery_online only) ---

GITHUB_OWNER = "your-github-username"
GITHUB_REPO = "your-image-repo"
# Folder inside the repo (no leading slash). Use "" for repository root.
GITHUB_PATH = "images"
GITHUB_BRANCH = "main"

# Classic PAT or fine-grained token with Contents: Read on this repo.
GITHUB_PAT = ""

# How often to re-list and download from GitHub (wall clock, best effort using time.time()).
GITHUB_SYNC_INTERVAL_MINUTES = 360
