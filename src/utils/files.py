import os
from pathlib import Path
from typing import Tuple, List, Optional


def read_file_lines(
    file_path: str,
    start_line: int = 1,
    end_line: Optional[int] = None,
    max_lines: int = 500
) -> Tuple[Optional[str], List[str], int]:
    path = Path(file_path)
    
    if not path.exists():
        return f"File not found: {file_path}", [], 0
    
    if not path.is_file():
        return f"Not a file: {file_path}", [], 0
    
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
    except PermissionError:
        return f"Permission denied: {file_path}", [], 0
    except Exception as e:
        return f"Error reading file: {str(e)}", [], 0
    
    total_lines = len(all_lines)
    
    start_idx = max(0, start_line - 1)
    if end_line is None:
        end_idx = min(start_idx + max_lines, total_lines)
    else:
        end_idx = min(end_line, total_lines)
    
    selected_lines = all_lines[start_idx:end_idx]
    
    return None, selected_lines, total_lines


def write_file_content(
    file_path: str,
    content: str,
    create_dirs: bool = True
) -> Optional[str]:
    path = Path(file_path)
    
    if create_dirs:
        path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return None
    except PermissionError:
        return f"Permission denied: {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def ensure_directory(dir_path: str) -> Optional[str]:
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return None
    except Exception as e:
        return f"Error creating directory: {str(e)}"


def get_file_info(file_path: str) -> dict:
    path = Path(file_path)
    
    if not path.exists():
        return {"exists": False}
    
    stat = path.stat()
    return {
        "exists": True,
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "size": stat.st_size,
        "modified": stat.st_mtime,
    }
