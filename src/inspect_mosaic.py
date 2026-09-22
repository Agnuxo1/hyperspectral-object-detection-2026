"""Inspect the decoded spectral tiles of a challenge image."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from hyperspectral_io import load_vis_mosaic


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    bands = load_vis_mosaic(args.image)
    means = bands.mean(axis=(1, 2))
    mins = bands.min(axis=(1, 2))
    maxs = bands.max(axis=(1, 2))
    print(f"bands_shape={bands.shape} dtype={bands.dtype}")
    print("band_stats=" + ";".join(f"{i}:{mins[i]}..{maxs[i]} mean={means[i]:.3f}" for i in range(len(means))))
    print(f"finite={bool(np.isfinite(bands).all())}")


if __name__ == "__main__":
    main()
