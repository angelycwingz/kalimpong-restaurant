import json
import logging

import bleach
import markdown as markdown_lib
import hashlib
import time

from django.core.cache import cache

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .chatbot_agent import answer_with_ai, clean_conversation_history

logger = logging.getLogger(__name__)


RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW_SECONDS = 60


def check_chatbot_rate_limit(request):
    """Allow at most 10 valid questions per IP per minute."""

    client_ip = request.META.get("REMOTE_ADDR", "unknown")
    ip_hash = hashlib.sha256(
        client_ip.encode("utf-8")
    ).hexdigest()[:32]

    now = time.time()
    window_id = int(now // RATE_LIMIT_WINDOW_SECONDS)
    seconds_until_reset = max(
        1,
        RATE_LIMIT_WINDOW_SECONDS
        - int(now % RATE_LIMIT_WINDOW_SECONDS),
    )

    cache_key = (
        f"chatbot:rate-limit:{ip_hash}:{window_id}"
    )

    # First request creates the counter for this minute.
    if cache.add(
        cache_key,
        1,
        timeout=RATE_LIMIT_WINDOW_SECONDS + 5,
    ):
        count = 1
    else:
        try:
            count = cache.incr(cache_key)
        except ValueError:
            # Recover if the key expired between the cache
            # lookup and increment.
            cache.add(
                cache_key,
                1,
                timeout=RATE_LIMIT_WINDOW_SECONDS + 5,
            )
            count = 1

    return count > RATE_LIMIT_REQUESTS, seconds_until_reset



@require_POST
def chatbot_api(request):
    """Receive a question and return a Groq-generated answer."""

    
    # HTML elements permitted in formatted chatbot responses.
    ALLOWED_CHAT_TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
        "p",
        "br",
        "strong",
        "em",
        "ul",
        "ol",
        "li",
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
        "blockquote",
        "pre",
        "code",
        "hr",
        "h1",
        "h2",
        "h3",
        "h4",
    }

    ALLOWED_CHAT_ATTRIBUTES = {
        "a": ["href", "title"],
        "th": ["align"],
        "td": ["align"],
    }

    ALLOWED_CHAT_PROTOCOLS = {
        "http",
        "https",
        "mailto",
        "tel",
    }


    def render_safe_markdown(text):
        """Convert AI-generated Markdown to sanitized HTML."""
        rendered_html = markdown_lib.markdown(
            text,
            extensions=["tables", "nl2br", "sane_lists"],
        )

        return bleach.clean(
            rendered_html,
            tags=ALLOWED_CHAT_TAGS,
            attributes=ALLOWED_CHAT_ATTRIBUTES,
            protocols=ALLOWED_CHAT_PROTOCOLS,
            strip=True,
        )


    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON request."},
            status=400,
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {"error": "Request must be a JSON object."},
            status=400,
        )

    message = data.get("message")

    if not isinstance(message, str):
        return JsonResponse(
            {"error": "Please provide a message as text."},
            status=400,
        )

    message = message.strip()

    if not message:
        return JsonResponse(
            {"error": "Please type a question."},
            status=400,
        )

    if len(message) > 500:
        return JsonResponse(
            {"error": "Your question must be 500 characters or fewer."},
            status=400,
        )

    
    is_limited, retry_after = check_chatbot_rate_limit(request)

    if is_limited:
        response = JsonResponse(
            {
                "error": (
                    "You've sent several questions in a short time. "
                    "Please wait a little before asking again."
                )
            },
            status=429,
        )
        response["Retry-After"] = str(retry_after)
        return response

    try:
        # The LLM interprets the question and decides when to use tools.
        conversation_history = clean_conversation_history(
            request.session.get("restaurant_chat_history", [])
        )

        reply = answer_with_ai(
            message,
            conversation_history=conversation_history,
        )

        if not isinstance(reply, str) or not reply.strip():
            raise RuntimeError("The AI returned an invalid response.")

        clean_reply = reply.strip()

        payload = {
            "reply": clean_reply,
            "reply_html": render_safe_markdown(clean_reply),
        }

        # Save only text messages, not system prompts or tool calls.
        updated_history = conversation_history + [
            {
                "role": "user",
                "content": message,
            },
            {
                "role": "assistant",
                "content": clean_reply,
            },
        ]

        # Keep at most four recent exchanges (eight messages).
        request.session["restaurant_chat_history"] = updated_history[-8:]

        return JsonResponse(payload)


    except Exception:
        # Keep technical details in server logs, not in the public response.
        logger.exception("Restaurant AI assistant request failed.")

        return JsonResponse(
            {
                "error": (
                    "Our restaurant assistant is temporarily unavailable. "
                    "Please try again shortly."
                )
            },
            status=503,
        )
