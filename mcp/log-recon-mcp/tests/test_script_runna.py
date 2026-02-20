import tempfile
import unittest
from pathlib import Path

from _server_loader import load_server_module

server = load_server_module()


class ScriptRunnaTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.log_dir = Path(self.tmpdir.name) / "logs"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_auto_returns_inline_for_small_output(self):
        result = server.script_runna(
            script="echo hello",
            output_dir=str(self.log_dir),
            inline_output_epsilon=1000,
            return_mode="auto",
        )
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("hello", result["output"])
        self.assertTrue(Path(result["output_file"]).exists())

    def test_path_only_returns_path_for_small_output(self):
        result = server.script_runna(
            script="echo hello",
            output_dir=str(self.log_dir),
            return_mode="path_only",
        )
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("output_file", result)
        self.assertNotIn("output", result)

    def test_inline_only_returns_output_for_large_output(self):
        result = server.script_runna(
            script="for i in $(seq 1 200); do echo line-$i; done",
            output_dir=str(self.log_dir),
            inline_output_epsilon=10,
            return_mode="inline_only",
        )
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("line-200", result["output"])
        self.assertGreater(result["output_size_bytes"], 10)

    def test_auto_returns_path_for_large_output(self):
        result = server.script_runna(
            script="for i in $(seq 1 200); do echo line-$i; done",
            output_dir=str(self.log_dir),
            inline_output_epsilon=10,
            return_mode="auto",
        )
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("output_file", result)
        self.assertNotIn("output", result)


if __name__ == "__main__":
    unittest.main()
