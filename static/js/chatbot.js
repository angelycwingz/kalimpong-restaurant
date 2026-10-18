document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("chatbot-toggle");
    const panel = document.getElementById("chatbot-panel");
    const close = document.getElementById("chatbot-close");
    const messages = document.getElementById("chatbot-messages");
    const form = document.getElementById("chatbot-form");
    const input = document.getElementById("chatbot-input");
    const quickReplies = document.querySelectorAll("[data-chat-question]");

    if (!toggle || !panel || !close || !messages || !form || !input) {
        return;
    }

    const endpoint = form.dataset.chatbotEndpoint;
    const csrfInput = form.querySelector("[name=csrfmiddlewaretoken]");
    const submitButton = form.querySelector('button[type="submit"]');

    let isSending = false;

    // Open and close the chat window.
    function openChat() {
        panel.hidden = false;
        toggle.setAttribute("aria-expanded", "true");
        input.focus();
    }

    function closeChat() {
        panel.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
    }

    toggle.addEventListener("click", () => {
        if (panel.hidden) {
            openChat();
        } else {
            closeChat();
        }
    });

    close.addEventListener("click", closeChat);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !panel.hidden) {
            closeChat();
        }
    });

    // Add text or a structured response containing a clickable link.
    // Use textContent for text; never inject HTML from a response.
    function addMessage(content, sender = "bot", useSanitizedHtml = false) {
        const bubble = document.createElement("div");

        bubble.classList.add("chatbot-message");
        bubble.classList.add(
            sender === "user"
                ? "chatbot-message--user"
                : "chatbot-message--bot"
        );

        if (typeof content === "string") {
            if (sender === "bot" && useSanitizedHtml) {
                bubble.innerHTML = content;
            } else {
                bubble.textContent = content;
            }
        } else if (content && typeof content.text === "string") {
            bubble.appendChild(
                document.createTextNode(content.text)
            );

            if (
                content.link &&
                typeof content.link.label === "string" &&
                typeof content.link.url === "string"
            ) {
                // Only allow HTTPS links and telephone links.
                const safeUrl =
                    content.link.url.startsWith("https://") ||
                    /^tel:\+?[0-9\s()-]+$/.test(content.link.url);

                if (safeUrl) {
                    bubble.appendChild(document.createTextNode(" "));

                    const link = document.createElement("a");
                    link.href = content.link.url;
                    link.textContent = content.link.label;
                    link.className = "chatbot-inline-link";

                    if (content.link.url.startsWith("https://")) {
                        link.target = "_blank";
                        link.rel = "noopener noreferrer";
                    }

                    bubble.appendChild(link);
                }
            }
        } else {
            bubble.textContent =
                "Sorry, I couldn't understand that response. Please try again.";
        }

        messages.appendChild(bubble);
        messages.scrollTop = messages.scrollHeight;

        return bubble;
    }

    // A small temporary indicator while Django processes a question.
    function showTypingIndicator() {
        const indicator = document.createElement("div");

        indicator.className =
            "chatbot-message chatbot-message--bot chatbot-typing";
        indicator.textContent = "momos is thinking…";
        indicator.setAttribute("aria-label", "Assistant is responding");

        messages.appendChild(indicator);
        messages.scrollTop = messages.scrollHeight;

        return indicator;
    }

    async function sendQuestion(question) {
        const cleanedQuestion = question.trim();

        if (!cleanedQuestion || isSending) {
            return;
        }

        if (!endpoint || !csrfInput?.value) {
            addMessage(
                "The chat isn't configured correctly yet. Please refresh the page and try again."
            );
            return;
        }

        addMessage(cleanedQuestion, "user");

        isSending = true;

        if (submitButton) {
            submitButton.disabled = true;
        }

        quickReplies.forEach((button) => {
            button.disabled = true;
        });

        const indicator = showTypingIndicator();

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfInput.value,
                },
                credentials: "same-origin",
                body: JSON.stringify({
                    message: cleanedQuestion,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "The restaurant assistant is temporarily unavailable."
                );
            }

            if (!Object.hasOwn(data, "reply")) {
                throw new Error("The server returned an unexpected response.");
            }

            if (typeof data.reply_html === "string") {
                addMessage(data.reply_html, "bot", true);
            } else {
                addMessage(data.reply, "bot");
            }
        } catch (error) {
            console.error("Chatbot request failed:", error);

            addMessage(
                error.message === "Failed to fetch"
                    ? "I couldn't connect to the restaurant assistant. Please check your connection and try again."
                    : error.message ||
                      "Something went wrong. Please try again in a moment."
            );
        } finally {
            indicator.remove();
            isSending = false;

            if (submitButton) {
                submitButton.disabled = false;
            }

            quickReplies.forEach((button) => {
                button.disabled = false;
            });

            input.focus();
        }
    }

    // Suggested-question buttons now ask Django for the answer.
    quickReplies.forEach((button) => {
        button.addEventListener("click", () => {
            sendQuestion(button.dataset.chatQuestion || "");
        });
    });

    // Typed questions also go to Django.
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (isSending) {
            return;
        }

        const question = input.value.trim();

        if (!question) {
            return;
        }

        input.value = "";
        sendQuestion(question);
    });
});
