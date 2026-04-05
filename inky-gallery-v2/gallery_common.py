import gc
import os

from machine import Pin, SPI

import jpegdec
import sdcard

_sd_mounted = False
_jpeg = None


class _Defaults:
    SLIDESHOW_INTERVAL_MINUTES = 60
    GALLERY_SD_FOLDER = "/sd/gallery"
    GITHUB_OWNER = ""
    GITHUB_REPO = ""
    GITHUB_PATH = ""
    GITHUB_BRANCH = "main"
    GITHUB_PAT = ""
    GITHUB_SYNC_INTERVAL_MINUTES = 360


def get_config():
    try:
        import gallery_config

        return gallery_config
    except ImportError:
        return _Defaults()


def ensure_sd():
    global _sd_mounted
    if _sd_mounted:
        return
    sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
    sd = sdcard.SDCard(sd_spi, Pin(22))
    os.mount(sd, "/sd")
    _sd_mounted = True


def ensure_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        pass


def list_jpegs(folder):
    ensure_sd()
    try:
        names = os.listdir(folder)
    except OSError:
        return []
    out = []
    for n in names:
        if n.startswith("."):
            continue
        low = n.lower()
        if low.endswith(".jpg") or low.endswith(".jpeg"):
            out.append(folder + "/" + n)
    out.sort()
    return out


def get_jpeg_decoder(graphics):
    global _jpeg
    if _jpeg is None:
        _jpeg = jpegdec.JPEG(graphics)
    return _jpeg


def draw_status(graphics, width, height, lines):
    graphics.set_pen(1)
    graphics.clear()
    graphics.set_pen(0)
    y = 20
    for line in lines:
        graphics.text(line, 8, y, width - 16, 2)
        y += 22
    graphics.update()
    gc.collect()


def draw_jpeg(graphics, width, height, path):
    gc.collect()
    j = get_jpeg_decoder(graphics)
    graphics.set_pen(1)
    graphics.clear()
    try:
        j.open_file(path)
        j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    except OSError:
        graphics.set_pen(0)
        graphics.rectangle(0, (height // 2) - 24, width, 48)
        graphics.set_pen(1)
        graphics.text("Cannot open JPEG", 8, (height // 2) - 18, width - 16, 2)
        graphics.text(path[-40:], 8, (height // 2) + 2, width - 16, 2)
    graphics.update()
    gc.collect()
