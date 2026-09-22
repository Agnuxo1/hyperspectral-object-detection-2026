"""Create a lightweight inventory before implementing the Kaggle adapter.

This script intentionally does not interpret labels. It records file extensions,
sizes and, when NumPy is available, shapes/dtypes for .npy/.npz files.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


DATA_EXTENSIONS = {".npy", ".npz", ".tif", ".tiff", ".png", ".jpg", ".jpeg", ".csv", ".txt", ".json"}


def inspect_numpy(path: Path) -> tuple[str, str]:
    try:
        import numpy as np
    except ImportError:
        return "", ""
    try:
        if path.suffix.lower() == ".npy":
            arr = np.load(path, mmap_mode="r", allow_pickle=False)
            return str(tuple(arr.shape)), str(arr.dtype)
        if path.suffix.lower() == ".npz":
            with np.load(path, mmap_mode="r", allow_pickle=False) as pack:
                details = [f"{key}:{tuple(pack[key].shape)}" for key in pack.files]
                dtypes = sorted({str(pack[key].dtype) for key in pack.files})
            return ";".join(details), ";".join(dtypes)
    except Exception as exc:  # keep the inventory useful even for a bad file
        return f"ERROR:{type(exc).__name__}", ""
    return "", ""


def build_inventory(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in DATA_EXTENSIONS):
        shape, dtype = inspect_numpy(path)
        rows.append(
            {
                "relative_path": path.relative_to(root).as_posix(),
                "suffix": path.suffix.lower(),
                "bytes": str(path.stat().st_size),
                "shape": shape,
                "dtype": dtype,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, default=Path("artifacts/dataset_inventory.csv"))
    args = parser.parse_args()
    rows = build_inventory(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["relative_path", "suffix", "bytes", "shape", "dtype"])
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["suffix"] for row in rows)
    print(f"files={len(rows)} extensions={dict(sorted(counts.items()))} output={args.output}")


if __name__ == "__main__":
    main()
