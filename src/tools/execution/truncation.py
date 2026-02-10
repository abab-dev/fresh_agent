import os
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

MAX_LINES = 2000
MAX_BYTES = 50 * 1024  # 50KB

OUTPUT_DIR = Path.home() / ".fresh_agent" / "tool-output"


@dataclass
class TruncateResult:
    content: str
    truncated: bool
    output_path: Optional[str] = None


def truncate_output(
    text: str,
    max_lines: int = MAX_LINES,
    max_bytes: int = MAX_BYTES,
    direction: str = "head",  # "head" or "tail"
) -> TruncateResult:
    """
    Truncate output if it exceeds limits.

    Returns truncated content with a hint about where full output is saved.
    """
    lines = text.split("\n")
    total_bytes = len(text.encode("utf-8"))

    if len(lines) <= max_lines and total_bytes <= max_bytes:
        return TruncateResult(content=text, truncated=False)

    # Truncate
    result_lines = []
    current_bytes = 0
    hit_bytes = False

    if direction == "head":
        for i, line in enumerate(lines):
            if i >= max_lines:
                break
            line_bytes = len(line.encode("utf-8")) + (1 if result_lines else 0)
            if current_bytes + line_bytes > max_bytes:
                hit_bytes = True
                break
            result_lines.append(line)
            current_bytes += line_bytes
    else:  # tail
        for i in range(len(lines) - 1, -1, -1):
            if len(result_lines) >= max_lines:
                break
            line_bytes = len(lines[i].encode("utf-8")) + (1 if result_lines else 0)
            if current_bytes + line_bytes > max_bytes:
                hit_bytes = True
                break
            result_lines.insert(0, lines[i])
            current_bytes += line_bytes

    removed = (
        total_bytes - current_bytes if hit_bytes else len(lines) - len(result_lines)
    )
    unit = "bytes" if hit_bytes else "lines"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_id = f"output_{int(time.time())}_{os.getpid()}"
    output_path = OUTPUT_DIR / f"{output_id}.txt"
    output_path.write_text(text, encoding="utf-8")

    preview = "\n".join(result_lines)
    hint = (
        f"\n\n... {removed} {unit} truncated ...\n"
        f"Full output saved to: {output_path}\n"
        f"Use ripgrep to search or read_file with line range to view specific sections."
    )

    if direction == "head":
        content = preview + hint
    else:
        content = f"... {removed} {unit} truncated ...\n\n{preview}"

    return TruncateResult(content=content, truncated=True, output_path=str(output_path))


def cleanup_old_outputs(max_age_days: int = 7):
    """Remove output files older than max_age_days."""
    if not OUTPUT_DIR.exists():
        return

    cutoff = time.time() - (max_age_days * 24 * 60 * 60)
    for f in OUTPUT_DIR.glob("output_*.txt"):
        try:
            if f.stat().st_mtime < cutoff:
                f.unlink()
        except Exception:
            pass
