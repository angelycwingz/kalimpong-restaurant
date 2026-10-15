
from pathlib import Path

from PIL import Image, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Keep the original photographs untouched.
JOBS = [
    {
        "source": Path("assets_reference/originals/hero-mountains.webp"),
        "output": Path(
            "static/images/hero/hero-mountains-optimized.webp"
        ),
        "max_size": (2560, 1600),
        "quality": 84,
    },
]


def optimize_image(job: dict) -> None:
    source = PROJECT_ROOT / job["source"]
    output = PROJECT_ROOT / job["output"]

    if not source.is_file():
        print(f"ERROR: Source not found: {source}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(source) as original:
            original.load()

            original_size = source.stat().st_size
            original_dimensions = original.size

            # Correct orientation using EXIF metadata.
            image = ImageOps.exif_transpose(original)

            # Resize while preserving aspect ratio.
            image.thumbnail(
                job["max_size"],
                Image.Resampling.LANCZOS,
            )

            # These source files are photographs, not transparent artwork.
            image = image.convert("RGB")

            # Write a separate WebP file; never overwrite the original.
            image.save(
                output,
                format="WEBP",
                quality=job["quality"],
                method=6,
            )

        optimized_size = output.stat().st_size
        reduction = (
            (original_size - optimized_size) / original_size
        ) * 100

        with Image.open(output) as optimized:
            optimized_dimensions = optimized.size

        print(f"\nImage: {job['source'].name}")
        print(f"Original: {original_dimensions}")
        print(f"Optimized: {optimized_dimensions}")
        print(f"Before: {original_size / 1024:.1f} KB")
        print(f"After:  {optimized_size / 1024:.1f} KB")
        print(f"Reduction: {reduction:.1f}%")
        print(f"Output: {job['output']}")

    except (OSError, ValueError) as error:
        print(f"ERROR optimizing {source.name}: {error}")


def main() -> None:
    for job in JOBS:
        optimize_image(job)


if __name__ == "__main__":
    main()
