import tempfile
import unittest
from pathlib import Path

from _server_loader import load_server_module

server = load_server_module()


class FileReckoningTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.tmpdir.name) / "sample.log"
        self.file_path.write_text(
            "\n".join(
                [
                    "INFO start",
                    "WARN disk low",
                    "ERROR failed to connect id=abc123 code=500",
                    "INFO retry",
                    "ERROR failed to connect id=def456 code=503",
                    "INFO done",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_stats_action(self):
        result = server.file_reckoning(path=str(self.file_path), action="stats")
        self.assertEqual(result["action"], "stats")
        self.assertEqual(result["stats"]["lines"], 6)
        self.assertGreater(result["stats"]["bytes"], 0)

    def test_head_action(self):
        result = server.file_reckoning(path=str(self.file_path), action="head", max_lines=2)
        self.assertEqual(len(result["rows"]), 2)
        self.assertEqual(result["rows"][0]["line"], 1)
        self.assertEqual(result["rows"][0]["text"], "INFO start")

    def test_tail_action(self):
        result = server.file_reckoning(path=str(self.file_path), action="tail", max_lines=2)
        self.assertEqual(len(result["rows"]), 2)
        self.assertEqual(result["rows"][0]["line"], 5)
        self.assertEqual(result["rows"][1]["text"], "INFO done")

    def test_search_action_with_context(self):
        result = server.file_reckoning(
            path=str(self.file_path),
            action="search",
            query="ERROR",
            before=1,
            after=1,
            max_matches=1,
        )
        kinds = [row["kind"] for row in result["rows"]]
        self.assertIn("before", kinds)
        self.assertIn("match", kinds)
        self.assertIn("after", kinds)

    def test_extract_action(self):
        result = server.file_reckoning(
            path=str(self.file_path),
            action="extract",
            query=r"id=(\w+)\s+code=(\d+)",
            max_matches=2,
        )
        self.assertEqual(len(result["rows"]), 2)
        self.assertEqual(result["rows"][0]["groups"], ["abc123", "500"])

    def test_search_requires_query(self):
        with self.assertRaises(ValueError):
            server.file_reckoning(path=str(self.file_path), action="search", query="")


if __name__ == "__main__":
    unittest.main()
