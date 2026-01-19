import os
import platform
from datetime import datetime


def get_environment_info() -> str:
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    user = os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
    shell = os.environ.get("SHELL", "unknown")
    system = platform.system()
    python_version = platform.python_version()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
## Environment

- **Working Directory**: {cwd}
- **Home Directory**: {home}
- **User**: {user}
- **Shell**: {shell}
- **OS**: {system}
- **Python Version**: {python_version}
- **Current Time**: {now}
""".strip()
