#!/usr/bin/env python3
"""Entrypoint for the news-image-20261121 entry.

The finished image lives in this repository as entry.png (drawn by
draw_news21.py). This program does nothing but copy that file to the
output directory, so the grader's two runs write exactly the same
bytes. Python 3.13 standard library only: no Pillow, no network.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "entry.png"


def resolve_output_dir():
    """Return the directory the grader wants the image in.

    MAKEFUN_OUTPUT_DIR wins when set; otherwise the grader's default
    /output; otherwise a local out/ directory for running by hand.
    """
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured:
        return configured
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(HERE, "out")


def run():
    source = os.path.join(HERE, IMAGE_NAME)
    if not os.path.isfile(source):
        print("error: {} is missing next to main.py; run draw_news21.py first".format(source), file=sys.stderr)
        return 1
    if os.path.getsize(source) == 0:
        print("error: {} is empty; regenerate it with draw_news21.py".format(source), file=sys.stderr)
        return 1
    target_dir = resolve_output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    print("wrote {} ({} bytes)".format(target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    sys.exit(run())
