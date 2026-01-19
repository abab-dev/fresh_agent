import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentConfig:
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    base_url: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL"))
    model: str = field(default_factory=lambda: os.getenv("MODEL_NAME", "gpt-4o"))
    
    timeout: float = 120.0
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    
    max_tokens: int = field(default_factory=lambda: int(os.getenv("MODEL_MAX_TOKENS", "200")) * 1024)
    compress_threshold: float = field(default_factory=lambda: float(os.getenv("COMPRESS_THRESHOLD", "0.8")))
    
    def __post_init__(self):
        if not self.api_key:
            raise ValueError("API key is required. Set OPENAI_API_KEY environment variable.")
