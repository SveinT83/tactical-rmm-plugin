import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from prelaunch import request_without_identity


class Reply:
    def __init__(self, status=401, login=False):
        self.code = status
        self.headers = {"WWW-Authenticate": 'Bearer resource_metadata="https://example.invalid/metadata"'}
        self.closed = False
        self.login = login

    def read(self, *args):
        if not self.login:
            raise AssertionError("Tool response body must never be read")
        return b'<a href="/admin/login">Login</a>'

    def close(self):
        self.closed = True


class Opener:
    def __init__(self, reply):
        self.reply = reply

    def open(self, request, timeout):
        if request.has_header("Authorization") or request.has_header("Cookie"):
            raise AssertionError("Identity-free test sent credentials")
        return self.reply


class PrelaunchSafetyTests(unittest.TestCase):
    def test_mutating_tools_are_rejected_before_network(self):
        for action in ["assign", "create", "rotate", "remove"]:
            with self.subTest(action=action), patch("urllib.request.build_opener") as network:
                with self.assertRaises(ValueError):
                    request_without_identity("https://example.invalid/mcp", {"method": "tools/call", "params": {"name": "tactical-rmm_access_" + action}})
                network.assert_not_called()

    def test_tool_response_body_is_not_read_even_on_unexpected_success(self):
        for status in [200, 401]:
            reply = Reply(status)
            with self.subTest(status=status), patch("urllib.request.build_opener", return_value=Opener(reply)):
                result = request_without_identity("https://example.invalid/mcp", {"method": "tools/call", "params": {"name": "tactical-rmm_access_users", "arguments": {}}})
                self.assertEqual(result["status"], status)
                self.assertTrue(reply.closed)
                self.assertNotIn("body", result)

    def test_html_read_cannot_be_enabled_for_tool_call(self):
        with patch("urllib.request.build_opener") as network:
            with self.assertRaises(ValueError):
                request_without_identity("https://example.invalid/mcp", {"method": "tools/call", "params": {"name": "tactical-rmm_access_users", "arguments": {}}}, read_login_html=True)
            network.assert_not_called()

    def test_login_html_is_reduced_to_a_marker(self):
        reply = Reply(200, login=True)
        with patch("urllib.request.build_opener", return_value=Opener(reply)):
            result = request_without_identity("https://example.invalid/admin/", read_login_html=True)
        self.assertTrue(result["keycloak_login_link_present"])
        self.assertNotIn("html", result)
        self.assertTrue(reply.closed)


if __name__ == "__main__":
    unittest.main()
