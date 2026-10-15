document.addEventListener("DOMContentLoaded", () => {
    const dialog = document.getElementById("gallery-lightbox");

    // The gallery might not be present on every page.
    if (!dialog) return;

    const triggers = Array.from(
        document.querySelectorAll("[data-gallery-trigger]")
    );

    const image = document.getElementById("gallery-lightbox-image");
    const caption = document.getElementById("gallery-lightbox-caption");
    const counter = document.getElementById("gallery-lightbox-counter");

    const closeButton = dialog.querySelector("[data-gallery-close]");
    const previousButton = dialog.querySelector("[data-gallery-prev]");
    const nextButton = dialog.querySelector("[data-gallery-next]");
    const stage = dialog.querySelector("[data-gallery-stage]");

    if (
        !triggers.length ||
        !image ||
        !caption ||
        !counter ||
        !closeButton ||
        !previousButton ||
        !nextButton
    ) {
        console.warn("Gallery lightbox markup is incomplete.");
        return;
    }

    let currentIndex = 0;
    let lastTrigger = null;
    let pointerStart = null;

    function updateImage(index) {
        currentIndex = (index + triggers.length) % triggers.length;

        const trigger = triggers[currentIndex];

        image.src = trigger.dataset.gallerySrc;
        image.alt = trigger.dataset.galleryAlt || "";
        caption.textContent =
            trigger.dataset.galleryCaption ||
            trigger.dataset.galleryAlt ||
            "Gallery image";

        counter.textContent =
            `${currentIndex + 1} of ${triggers.length}`;

        const navigationDisabled = triggers.length < 2;

        previousButton.disabled = navigationDisabled;
        nextButton.disabled = navigationDisabled;

        // Prepare adjacent images to make navigation feel faster.
        if (triggers.length > 1) {
            const previousIndex =
                (currentIndex - 1 + triggers.length) % triggers.length;

            const nextIndex = (currentIndex + 1) % triggers.length;

            [previousIndex, nextIndex].forEach((itemIndex) => {
                const preload = new Image();
                preload.src = triggers[itemIndex].dataset.gallerySrc;
            });
        }
    }

    function openViewer(trigger) {
        lastTrigger = trigger;

        const index = triggers.indexOf(trigger);
        if (index === -1) return;

        updateImage(index);

        if (!dialog.open) {
            dialog.showModal();
        }
    }

    function closeViewer() {
        if (dialog.open) {
            dialog.close();
        }
    }

    triggers.forEach((trigger) => {
        trigger.addEventListener("click", () => {
            openViewer(trigger);
        });
    });

    closeButton.addEventListener("click", closeViewer);

    previousButton.addEventListener("click", () => {
        updateImage(currentIndex - 1);
    });

    nextButton.addEventListener("click", () => {
        updateImage(currentIndex + 1);
    });

    // Keyboard navigation. Escape is handled by the native dialog.
    dialog.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft") {
            event.preventDefault();
            updateImage(currentIndex - 1);
        }

        if (event.key === "ArrowRight") {
            event.preventDefault();
            updateImage(currentIndex + 1);
        }
    });

    // Restore keyboard focus to the thumbnail after closing.
    dialog.addEventListener("close", () => {
        image.removeAttribute("src");

        if (lastTrigger?.isConnected) {
            lastTrigger.focus({ preventScroll: true });
        }

        lastTrigger = null;
    });

    // Allow clicking the empty dialog background to close the viewer.
    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) {
            closeViewer();
        }
    });

    // Enable horizontal swipe gestures on touchscreens.
    if (stage) {
        stage.addEventListener("pointerdown", (event) => {
            if (
                event.target.closest("button") ||
                event.button !== 0
            ) {
                pointerStart = null;
                return;
            }

            pointerStart = {
                x: event.clientX,
                y: event.clientY,
            };
        });

        stage.addEventListener("pointerup", (event) => {
            if (!pointerStart) return;

            const deltaX = event.clientX - pointerStart.x;
            const deltaY = event.clientY - pointerStart.y;

            pointerStart = null;

            if (
                Math.abs(deltaX) < 55 ||
                Math.abs(deltaX) < Math.abs(deltaY) * 1.3
            ) {
                return;
            }

            if (deltaX < 0) {
                updateImage(currentIndex + 1);
            } else {
                updateImage(currentIndex - 1);
            }
        });

        stage.addEventListener("pointercancel", () => {
            pointerStart = null;
        });
    }
});
