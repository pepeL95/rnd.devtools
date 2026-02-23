import importlib.util
import sys
import types
from pathlib import Path


def load_server_module():
    # Minimal fastmcp stub so tests can import server.py without the package.
    fastmcp_stub = types.ModuleType("fastmcp")

    class FastMCP:
        def __init__(self, name: str):
            self.name = name

        def tool(self, name=None):
            def decorator(func):
                return func

            return decorator

        def run(self, *args, **kwargs):
            return None

    fastmcp_stub.FastMCP = FastMCP
    sys.modules["fastmcp"] = fastmcp_stub

    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    server_path = project_root / "server.py"
    spec = importlib.util.spec_from_file_location("server_under_test", server_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module
