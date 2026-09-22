"""Validate the Kaggle submission contract without needing the training stack."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


REQUIRED = ["id", "image_id", "class_id", "confidence", "x1", "y1", "x2", "y2"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != REQUIRED:
            raise ValueError(f"header inválido: {reader.fieldnames!r}; esperado {REQUIRED!r}")
        return list(reader)


def load_image_ids(path: Path | None) -> set[str] | None:
    if path is None:
        return None
    with path.open("r", newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if "image_id" not in (reader.fieldnames or []):
            raise ValueError("image-index debe contener la columna image_id")
        return {row["image_id"] for row in reader}


def as_float(row: dict[str, str], key: str, line: int) -> float:
    try:
        value = float(row[key])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"línea {line}: {key} no es numérico") from exc
    if not math.isfinite(value):
        raise ValueError(f"línea {line}: {key} no es finito")
    return value


def validate(path: Path, image_index: Path | None) -> tuple[int, int]:
    rows = read_rows(path)
    known_ids = load_image_ids(image_index)
    seen_ids: set[str] = set()
    errors: list[str] = []
    for line, row in enumerate(rows, start=2):
        try:
            row_id = int(row["id"])
            class_id = int(row["class_id"])
        except ValueError:
            errors.append(f"línea {line}: id/class_id no es entero")
            continue
        if row_id != line - 2:
            errors.append(f"línea {line}: id={row_id}, esperado {line - 2}")
        if class_id < 0 or class_id >= 18:
            errors.append(f"línea {line}: class_id fuera de 0..17")
        if row["image_id"] == "":
            errors.append(f"línea {line}: image_id vacío")
        if known_ids is not None and row["image_id"] not in known_ids:
            errors.append(f"línea {line}: image_id desconocido {row['image_id']!r}")
        confidence = as_float(row, "confidence", line)
        if not 0.0 <= confidence <= 1.0:
            errors.append(f"línea {line}: confidence fuera de [0,1]")
        coords = [as_float(row, key, line) for key in ("x1", "y1", "x2", "y2")]
        if coords[2] <= coords[0] or coords[3] <= coords[1]:
            errors.append(f"línea {line}: caja degenerada {coords}")
        seen_ids.add(row["image_id"])
    if errors:
        raise ValueError("\n".join(errors[:30]) + ("\n..." if len(errors) > 30 else ""))
    return len(rows), len(seen_ids)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path)
    parser.add_argument("--image-index", type=Path)
    args = parser.parse_args()
    rows, images = validate(args.submission, args.image_index)
    print(f"OK: {rows} detecciones en {images} imágenes; header y rangos válidos")


if __name__ == "__main__":
    main()
