"""I/O helpers for the challenge VIS mosaic representation."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def load_vis_mosaic(path: str | Path, grid: int = 4) -> np.ndarray:
    """Load a row-major ``grid x grid`` band mosaic as ``(bands, height, width)``.

    The challenge samples observed so far are uint16 single-channel PNGs whose
    height and width are divisible by four. The function rejects ambiguous
    dimensions rather than silently cropping pixels.
    """
    with Image.open(path) as image:
        array = np.asarray(image)
    if array.ndim != 2:
        raise ValueError(f"expected one-channel mosaic, got shape={array.shape}")
    height, width = array.shape
    if height % grid or width % grid:
        raise ValueError(f"mosaic shape {array.shape} is not divisible by grid={grid}")
    tile_height, tile_width = height // grid, width // grid
    bands = np.empty((grid * grid, tile_height, tile_width), dtype=array.dtype)
    band_index = 0
    for row in range(grid):
        for col in range(grid):
            y0, y1 = row * tile_height, (row + 1) * tile_height
            x0, x1 = col * tile_width, (col + 1) * tile_width
            bands[band_index] = array[y0:y1, x0:x1]
            band_index += 1
    return bands
