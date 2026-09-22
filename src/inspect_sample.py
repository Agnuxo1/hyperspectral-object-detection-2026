"""Inspect one downloaded sample image without modifying it."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    with Image.open(args.image) as image:
        array = np.asarray(image)
        print(
            f"mode={image.mode} size={image.size} shape={array.shape} "
            f"dtype={array.dtype} min={array.min()} max={array.max()}"
        )


if __name__ == "__main__":
    main()
