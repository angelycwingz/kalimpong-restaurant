
import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache


class ChatbotApiTests(TestCase):
    """Test the Django API without making real Groq requests."""

    def setUp(self):
        cache.clear()
        self.url = reverse("chatbot_api")

    def post_json(self, payload):
        return self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )

    @patch("home.chatbot_views.answer_with_ai")
    def test_api_returns_ai_generated_answer(self, mock_answer):
        mock_answer.return_value = (
            "Our vegetarian steamed momos cost ₹180."
        )

        response = self.post_json({
            "message": "How much are vegetarian momos?"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["reply"],
            "Our vegetarian steamed momos cost ₹180.",
        )
        mock_answer.assert_called_once_with(
            "How much are vegetarian momos?",
            conversation_history=[],
        )

    @patch("home.chatbot_views.answer_with_ai")
    def test_api_trims_message_before_calling_ai(self, mock_answer):
        mock_answer.return_value = "Hello!"

        response = self.post_json({
            "message": "  Hello!  "
        })

        self.assertEqual(response.status_code, 200)
        mock_answer.assert_called_once_with("Hello!", conversation_history=[],)

    @patch("home.chatbot_views.answer_with_ai")
    def test_api_handles_ai_failure(self, mock_answer):
        mock_answer.side_effect = RuntimeError("Simulated AI failure")

        response = self.post_json({
            "message": "Where is the restaurant?"
        })

        self.assertEqual(response.status_code, 503)
        self.assertIn("error", response.json())
        self.assertNotIn(
            "Simulated AI failure",
            response.content.decode(),
        )

    @patch("home.chatbot_views.answer_with_ai")
    def test_api_rejects_empty_message(self, mock_answer):
        response = self.post_json({"message": "   "})

        self.assertEqual(response.status_code, 400)
        mock_answer.assert_not_called()

    @patch("home.chatbot_views.answer_with_ai")
    def test_api_rejects_message_over_500_characters(self, mock_answer):
        response = self.post_json({
            "message": "a" * 501
        })

        self.assertEqual(response.status_code, 400)
        mock_answer.assert_not_called()

    @patch("home.chatbot_views.answer_with_ai")
    def test_api_rejects_missing_message(self, mock_answer):
        response = self.post_json({})

        self.assertEqual(response.status_code, 400)
        mock_answer.assert_not_called()

    @patch("home.chatbot_views.answer_with_ai")
    def test_api_rejects_non_object_json(self, mock_answer):
        response = self.client.post(
            self.url,
            data=json.dumps(["hello"]),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        mock_answer.assert_not_called()

    def test_api_rejects_invalid_json(self):
        response = self.client.post(
            self.url,
            data="{invalid json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_api_rejects_get_requests(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)


    @patch("home.chatbot_views.answer_with_ai")
    def test_api_rate_limits_after_ten_valid_requests(self, mock_answer):
        mock_answer.return_value = "Hello! How can I help?"

        for _ in range(10):
            response = self.post_json({
                "message": "Where is the restaurant?"
            })
            self.assertEqual(response.status_code, 200)

        response = self.post_json({
            "message": "Show me the menu"
        })

        self.assertEqual(response.status_code, 429)
        self.assertIn("Retry-After", response.headers)
        self.assertEqual(mock_answer.call_count, 10)



    @patch("home.chatbot_views.answer_with_ai")
    def test_follow_up_receives_previous_conversation(self, mock_answer):
        mock_answer.side_effect = [
            "Our vegetarian steamed momos cost ₹180.",
            "Our vegetarian fried momos cost ₹200.",
        ]

        first_response = self.post_json({
            "message": "How much are momos?"
        })

        self.assertEqual(first_response.status_code, 200)

        second_response = self.post_json({
            "message": "What about the fried ones?"
        })

        self.assertEqual(second_response.status_code, 200)

        # The second AI request should receive the previous exchange.
        self.assertEqual(
            mock_answer.call_args_list[1].kwargs[
                "conversation_history"
            ],
            [
                {
                    "role": "user",
                    "content": "How much are momos?",
                },
                {
                    "role": "assistant",
                    "content": "Our vegetarian steamed momos cost ₹180.",
                },
            ],
        )