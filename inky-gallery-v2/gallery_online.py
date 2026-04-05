import gc

import network

import gallery_common as g
import gallery_github as gh

graphics = None
WIDTH = None
HEIGHT = None

_cfg = g.get_config()
UPDATE_INTERVAL = int(getattr(_cfg, "SLIDESHOW_INTERVAL_MINUTES", 60))

_files = []
_idx = -1
_status = ""
_sync_note = ""

gc.collect()


def _wifi_ok():
    wlan = network.WLAN(network.STA_IF)
    return wlan.status() == 3


def update():
    global _files, _idx, _status, _sync_note
    gc.collect()
    cfg = g.get_config()

    if _wifi_ok() and getattr(cfg, "GITHUB_PAT", "") and gh.should_sync(cfg):
        err = gh.sync_from_github(cfg)
        _sync_note = "" if err is None else err
    elif not getattr(cfg, "GITHUB_PAT", ""):
        _sync_note = "Set GITHUB_PAT in gallery_config.py"

    g.ensure_sd()
    g.ensure_dir(cfg.GALLERY_SD_FOLDER)
    _files = g.list_jpegs(cfg.GALLERY_SD_FOLDER)
    if not _files:
        lines = ["Online gallery", _sync_note or _status or "No JPEGs after sync"]
        _status = lines[-1]
        return
    _idx = (_idx + 1) % len(_files)
    _status = ""


def draw():
    if not _files:
        lines = ["Online gallery", _sync_note or _status or "No images"]
        g.draw_status(graphics, WIDTH, HEIGHT, lines)
        return
    path = _files[_idx]
    g.draw_jpeg(graphics, WIDTH, HEIGHT, path)
