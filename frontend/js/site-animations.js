
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

document.addEventListener("DOMContentLoaded", () => {
    // Respect visitors who prefer reduced motion.
    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) {
        return;
    }

    // ----------------------------------
    // 1. Hero entrance animation
    // ----------------------------------

    const hero = document.querySelector("#hero");

    if (hero) {
        const heroItems = hero.querySelectorAll("[data-hero-reveal]");
        const background = hero.querySelector("[data-hero-background]");
        const scrollIndicator = hero.querySelector("[data-hero-scroll]");
        const scrollArrow = hero.querySelector("[data-scroll-arrow]");

        // Warn us if the background image isn't connected correctly.
        if (!background) {
            console.warn(
                "Hero zoom skipped: add data-hero-background to the mountain image."
            );
        } else {
            // Slowly zoom in, then ease back out.
            // The image always remains at scale 1 or greater,
            // so it continues to cover the hero without gaps.
            gsap.fromTo(
                background,
                {
                    scale: 1,
                    transformOrigin: "center center"
                },
                {
                    scale: 1.07,
                    duration: 24,
                    ease: "sine.inOut",
                    repeat: -1,
                    yoyo: true
                }
            );
        }

        // Animate the hero content with a softer entrance.
        if (heroItems.length > 0) {
            gsap.from(heroItems, {
                autoAlpha: 0,
                y: 20,
                duration: 1.1,
                stagger: 0.16,
                ease: "power3.out",
                delay: 0.2,
                clearProps: "transform"
            });

            // Keep the LCP paragraph visible, animating position only.
            const heroLcpText = hero.querySelector("[data-hero-lcp]");

            if (heroLcpText) {
                gsap.from(heroLcpText, {
                    y: 14,
                    duration: 0.9,
                    delay: 0.45,
                    ease: "power3.out",
                    clearProps: "transform"
                });
            }
        }

        // Keep the scroll prompt gently moving.
        if (scrollIndicator) {
            gsap.to(scrollIndicator, {
                y: 5,
                duration: 1.4,
                ease: "sine.inOut",
                repeat: -1,
                yoyo: true
            });
        }

        if (scrollArrow) {
            gsap.to(scrollArrow, {
                y: 5,
                duration: 1.4,
                ease: "sine.inOut",
                repeat: -1,
                yoyo: true
            });
}
    }


    // ----------------------------------
    // 2. Reveal individual elements
    // ----------------------------------
    gsap.utils.toArray("[data-reveal]").forEach((element) => {
        gsap.from(element, {
            autoAlpha: 0,
            y: 28,
            duration: 0.8,
            ease: "power2.out",
            scrollTrigger: {
                trigger: element,
                start: "top 86%",
                once: true
            }
        });
    });

    // ----------------------------------
    // 3. Reveal groups in a stagger
    // ----------------------------------
    gsap.utils.toArray("[data-reveal-group]").forEach((group) => {
        const items = Array.from(group.children);

        if (items.length === 0) {
            return;
        }

        gsap.from(items, {
            autoAlpha: 0,
            y: 24,
            duration: 0.75,
            stagger: 0.13,
            ease: "power2.out",
            scrollTrigger: {
                trigger: group,
                start: "top 85%",
                once: true
            }
        });
    });
});
