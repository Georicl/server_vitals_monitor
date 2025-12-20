import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))


def test_import_modules():
    try:
        from server_monitor import monitor  # noqa: F401
        from server_monitor import daily_job  # noqa: F401
        from server_monitor import task_guard  # noqa: F401
        from server_monitor import reporter  # noqa: F401

        print("All modules imported successfully.")
    except ImportError as e:
        assert False, f"Import failed: {e}"
