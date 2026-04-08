import os
import tempfile
import unittest
from pathlib import Path

from _server_loader import load_server_module

server = load_server_module()


class HandoffInstructionsTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.original_cwd = Path.cwd()
        self.original_env_root = os.environ.get("LOG_EFFICIENT_MCP_WORKSPACE_ROOT")
        os.chdir(self.tmpdir.name)
        os.environ["LOG_EFFICIENT_MCP_WORKSPACE_ROOT"] = self.tmpdir.name

    def tearDown(self):
        os.chdir(self.original_cwd)
        if self.original_env_root is None:
            os.environ.pop("LOG_EFFICIENT_MCP_WORKSPACE_ROOT", None)
        else:
            os.environ["LOG_EFFICIENT_MCP_WORKSPACE_ROOT"] = self.original_env_root
        self.tmpdir.cleanup()

    def test_returns_instructions_from_handoff_file(self):
        Path("HANDOFF.md").write_text("Please investigate CI flakes.\n", encoding="utf-8")
        result = server.handoff_instructions()
        self.assertEqual(result, "User >> Please investigate CI flakes.")

    def test_missing_file_requests_input(self):
        result = server.handoff_instructions()
        self.assertEqual(result, "No instruction provided .. ending turn without handoff instructions.")

    def test_empty_file_requests_input(self):
        Path("HANDOFF.md").write_text(" \n", encoding="utf-8")
        result = server.handoff_instructions()
        self.assertEqual(result, "No instruction provided .. ending turn without handoff instructions.")

    def test_resolves_workspace_root_from_env_even_if_cwd_differs(self):
        nested_dir = Path(self.tmpdir.name) / "nested" / "deeper"
        nested_dir.mkdir(parents=True)
        Path(self.tmpdir.name, "HANDOFF.md").write_text("Root-level handoff.\n", encoding="utf-8")
        os.chdir(nested_dir)

        result = server.handoff_instructions()

        self.assertEqual(result, "User >> Root-level handoff.")


if __name__ == "__main__":
    unittest.main()
