import sys
import os

# 把 src 加入路径，确保能导入模块
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

def test_import_modules():
    try:
        from server_monitor import monitor
        from server_monitor import daily_job
        from server_monitor import task_guard
        from server_monitor import reporter
        print("All modules imported successfully.")
    except ImportError as e:
        assert False, f"Import failed: {e}"