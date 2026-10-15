
document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector("#site-navbar");
    const hero = document.querySelector("#hero");

    // 1. Change navbar appearance when leaving the hero.
    if (navbar && hero) {
        const observer = new IntersectionObserver(
            ([entry]) => {
                navbar.classList.toggle(
                    "is-scrolled",
                    !entry.isIntersecting
                );
            },
            { threshold: 0.05 }
        );

        observer.observe(hero);
    }

    // 2. Set up the mobile navigation.
    const menuButton = document.querySelector("#mobile-menu-button");
    const mobileMenu = document.querySelector("#mobile-navigation");

    if (!menuButton || !mobileMenu) {
        return;
    }

    const hamburgerIcon = `
        <svg viewBox="0 0 24 24" class="h-6 w-6"
            fill="none" stroke="currentColor" stroke-width="1.8"
            stroke-linecap="round" aria-hidden="true">
            <path d="M4 7h16M4 12h16M4 17h16"/>
        </svg>`;

    const closeIcon = `
        <svg viewBox="0 0 24 24" class="h-6 w-6"
            fill="none" stroke="currentColor" stroke-width="1.8"
            stroke-linecap="round" aria-hidden="true">
            <path d="M6 6l12 12M18 6L6 18"/>
        </svg>`;

    function setMenuOpen(isOpen) {
        mobileMenu.classList.toggle("hidden", !isOpen);

        menuButton.setAttribute("aria-expanded", String(isOpen));
        menuButton.setAttribute(
            "aria-label",
            isOpen ? "Close navigation menu" : "Open navigation menu"
        );

        menuButton.innerHTML = isOpen ? closeIcon : hamburgerIcon;
    }

    menuButton.addEventListener("click", () => {
        const isOpen =
            menuButton.getAttribute("aria-expanded") === "true";

        setMenuOpen(!isOpen);
    });

    // Close the menu after choosing a destination.
    mobileMenu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => setMenuOpen(false));
    });

    // Allow visitors to close the menu using Escape.
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            setMenuOpen(false);
        }
    });

    // Close the mobile menu if the viewport becomes desktop-sized.
    window.addEventListener("resize", () => {
        if (window.innerWidth >= 768) {
            setMenuOpen(false);
        }
    });
});
