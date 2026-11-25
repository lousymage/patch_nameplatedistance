import argparse
import math
import shutil
import struct
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Patch a stock WoW 1.12.1 executable in place. Default: 41 yards."
)
parser.add_argument("exe", type=Path)
parser.add_argument("yards", type=float, nargs="?", default=41.0)
args = parser.parse_args()

try:
    distance = struct.pack("<f", args.yards)
except OverflowError:
    parser.error("distance is too large")
if not math.isfinite(args.yards) or args.yards <= 0 or distance == bytes(4):
    parser.error("distance must be a positive, finite 32-bit float")

offset = 0x40C448
backup_path = args.exe.with_name(args.exe.name + ".bak")

with args.exe.open("r+b") as exe:
    exe.seek(offset)
    if exe.read(4) != struct.pack("<f", 20.0):
        parser.error("expected the stock 20-yard value at offset 0x40C448")

    try:
        backup = backup_path.open("xb")
    except FileExistsError:
        parser.error(f"backup already exists: {backup_path}")

    try:
        with backup:
            exe.seek(0)
            shutil.copyfileobj(exe, backup)
    except OSError:
        backup_path.unlink()
        raise

    exe.seek(offset)
    exe.write(distance)
