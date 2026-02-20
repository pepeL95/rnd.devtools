import unittest

from _server_loader import load_server_module

server = load_server_module()


class HealthTests(unittest.TestCase):
    def test_health_returns_ok_payload(self):
        result = server.health()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["service"], "log-recon-mcp")
        self.assertIn("timestamp_utc", result)
        self.assertTrue(result["timestamp_utc"])


if __name__ == "__main__":
    unittest.main()
