
from pathlib import Path

from PIL import Image, ImageOps

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    PROJECT_ROOT
    / "assets_reference"
    / "originals"
    / "hero-mountains.webp"
)

OUTPUT = (
    PROJECT_ROOT
    / "static"
    / "images"
    / "hero"
    / "hero-mountains-mobile.webp"
)

TARGET_SIZE = (900, 1800)

# 0.0 = left, 0.5 = center, 1.0 = right.
# We can adjust this after inspecting the crop.
FOCAL_X = 0.5


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(
            f"Original mountain image not found: {SOURCE}"
        )

    with Image.open(SOURCE) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")

    width, height = image.size
    target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
    source_ratio = width / height

    if source_ratio > target_ratio:
        # Crop the sides to create a portrait composition.
        crop_width = round(height * target_ratio)
        center_x = round(width * FOCAL_X)

        left = max(
            0,
            min(width - crop_width, center_x - crop_width // 2),
        )

        crop_box = (left, 0, left + crop_width, height)
    else:
        # Crop the top and bottom if the source is already narrow.
        crop_height = round(width / target_ratio)
        top = (height - crop_height) // 2
        crop_box = (0, top, width, top + crop_height)

    mobile_image = image.crop(crop_box)
    mobile_image = mobile_image.resize(
        TARGET_SIZE,
        Image.Resampling.LANCZOS,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    mobile_image.save(
        OUTPUT,
        format="WEBP",
        quality=82,
        method=6,
    )

    print(f"Created: {OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Dimensions: {mobile_image.size}")
    print(f"File size: {OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
