import gc

import gallery_common as g

graphics = None
WIDTH = None
HEIGHT = None

_cfg = g.get_config()
UPDATE_INTERVAL = int(getattr(_cfg, "SLIDESHOW_INTERVAL_MINUTES", 60))

_files = []
_idx = -1
_status = ""

gc.collect()


def update():
    global _files, _idx, _status
    gc.collect()
    cfg = g.get_config()
    g.ensure_sd()
    g.ensure_dir(cfg.GALLERY_SD_FOLDER)
    _files = g.list_jpegs(cfg.GALLERY_SD_FOLDER)
    if not _files:
        _status = "No JPEGs in " + cfg.GALLERY_SD_FOLDER
        return
    _idx = (_idx + 1) % len(_files)
    _status = ""


def draw():
    if not _files:
        g.draw_status(graphics, WIDTH, HEIGHT, ["Offline gallery", _status or "No images"])
        return
    path = _files[_idx]
    g.draw_jpeg(graphics, WIDTH, HEIGHT, path)
