#!/usr/bin/python3

"""Convert XFB dump to RGB8 PNG

This script takes in a XFB dump in YUYV (4:2:2) format,
and produces a RGB8 PNG. The width and height of the
resulting picture must be specified in advance.
"""

import argparse
import struct
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("path", metavar="PATH", type=str, nargs="+")
parser.add_argument("--width", default=608, type=int, required=True)
parser.add_argument("--height", default=542, type=int, required=True)
args = parser.parse_args()


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def convert_file(out, src_bytes):
    for elem in struct.iter_unpack(">I", src_bytes):
        y1 = float((elem[0] >> 24) & 0xFF)
        u = float((elem[0] >> 16) & 0xFF)
        y2 = float((elem[0] >> 8) & 0xFF)
        v = float(elem[0] & 0xFF)

        y1 = 1.164 * (y1 - 16.0)
        y2 = 1.164 * (y2 - 16.0)
        u = u - 128.0
        v = v - 128.0

        r1 = y1 + 1.596 * v
        g1 = y1 - 0.391 * u - 0.813 * v
        b1 = y1 + 2.018 * u
        r2 = y2 + 1.596 * v
        g2 = y2 - 0.391 * u - 0.813 * v
        b2 = y2 + 2.018 * u
        r1 = clamp(r1, 0, 255)
        g1 = clamp(g1, 0, 255)
        b1 = clamp(b1, 0, 255)
        r2 = clamp(r2, 0, 255)
        g2 = clamp(g2, 0, 255)
        b2 = clamp(b2, 0, 255)
        next_bytes = struct.pack(
            ">BBBBBBBB", int(r1), int(g1), int(b1), int(r2), int(g2), int(b2),
        )
        out.extend(next_bytes)


for path in args.path:
    with open(path, "rb") as src:
        src_bytes = src.read()
    dst = bytearray()
    convert_file(dst, src_bytes)
    img = Image.frombuffer(
        "RGB", (args.width, args.height), bytes(dst), "raw", ("RGB", 0, 1)
    )
    img.save(path + ".png")
