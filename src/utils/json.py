import json
import re
from typing import Any, Dict, Tuple, Optional


def parse_tool_arguments(arguments_str: str) -> Tuple[Dict[str, Any], Optional[str]]:
    if not arguments_str or not arguments_str.strip():
        return {}, None
    
    try:
        return json.loads(arguments_str), None
    except json.JSONDecodeError:
        pass
    
    try:
        fixed = _attempt_json_repair(arguments_str)
        return json.loads(fixed), None
    except json.JSONDecodeError as e:
        return {}, f"Invalid JSON arguments: {str(e)}"


def _attempt_json_repair(s: str) -> str:
    s = s.strip()
    
    if not s.startswith("{"):
        s = "{" + s
    if not s.endswith("}"):
        s = s + "}"
    
    s = re.sub(r',\s*}', '}', s)
    s = re.sub(r',\s*]', ']', s)
    
    return s


def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return default


def truncate_json_string(s: str, max_length: int = 1000) -> str:
    if len(s) <= max_length:
        return s
    return s[:max_length] + f"... [truncated {len(s) - max_length} chars]"
