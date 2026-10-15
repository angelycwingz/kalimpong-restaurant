
from pathlib import Path

from PIL import Image, UnidentifiedImageError


# Project root is the parent of the scripts directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = PROJECT_ROOT / "static" / "images"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
LARGE_FILE_BYTES = 500 * 1024
LARGE_DIMENSION = 2560


def audit_images() -> None:
    if not IMAGE_DIR.is_dir():
        print(f"Image directory not found: {IMAGE_DIR}")
        return

    files = [
        path
        for path in IMAGE_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        print("No supported images found.")
        return

    results = []

    for path in files:
        size_bytes = path.stat().st_size

        try:
            with Image.open(path) as image:
                width, height = image.size
                image_format = image.format or "Unknown"

        except (OSError, UnidentifiedImageError) as error:
            print(f"Could not inspect {path.name}: {error}")
            continue

        warnings = []

        if size_bytes > LARGE_FILE_BYTES:
            warnings.append("LARGE FILE")

        if max(width, height) > LARGE_DIMENSION:
            warnings.append("LARGE DIMENSIONS")

        results.append(
            (
                size_bytes,
                width,
                height,
                image_format,
                path.relative_to(PROJECT_ROOT),
                ", ".join(warnings) or "OK",
            )
        )

    results.sort(reverse=True, key=lambda item: item[0])

    print(
        f"{'SIZE (KB)':>10}  {'DIMENSIONS':>13}  "
        f"{'FORMAT':<7}  {'STATUS':<24}  FILE"
    )
    print("-" * 105)

    total_bytes = 0

    for size, width, height, image_format, path, status in results:
        total_bytes += size

        print(
            f"{size / 1024:10.1f}  "
            f"{width:5} x {height:<5}  "
            f"{image_format:<7}  "
            f"{status:<24}  "
            f"{path}"
        )

    print("-" * 105)
    print(f"Images inspected: {len(results)}")
    print(f"Total image size: {total_bytes / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    audit_images()
