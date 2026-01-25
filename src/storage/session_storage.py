"""
Session storage for persisting agent state to disk.

Saves sessions as JSON files in ~/.fresh_agent/sessions/{session_id}/
"""

import json
import os
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import uuid


class SessionStorage:
    """Simple JSON file storage for agent sessions."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(
            base_dir or os.path.expanduser("~/.fresh_agent/sessions")
        )
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _session_dir(self, session_id: str) -> Path:
        return self.base_dir / session_id

    def save_session(
        self,
        session_id: str,
        state: Dict[str, Any],
        messages: List[Dict[str, Any]],
        workspace: Optional[str] = None,
        title: Optional[str] = None,
    ) -> None:
        """
        Save session state and messages to disk.

        Args:
            session_id: Unique session identifier
            state: AgentState as dict
            messages: List of conversation messages
            workspace: Working directory for this session
            title: Optional human-readable title
        """
        session_dir = self._session_dir(session_id)
        session_dir.mkdir(exist_ok=True)

        # Save session metadata and state
        state_file = session_dir / "session.json"
        session_data = {
            "id": session_id,
            "title": title or f"Session {session_id[:8]}",
            "workspace": workspace or os.getcwd(),
            "state": state,
            "created_at": self._get_created_at(session_id),
            "updated_at": datetime.now().isoformat(),
        }

        with open(state_file, "w") as f:
            json.dump(session_data, f, indent=2, default=str)

        # Save messages separately (can get large)
        messages_file = session_dir / "messages.json"
        with open(messages_file, "w") as f:
            json.dump(messages, f, indent=2, default=str)

    def _get_created_at(self, session_id: str) -> str:
        """Get created_at from existing session or return now."""
        try:
            state_file = self._session_dir(session_id) / "session.json"
            if state_file.exists():
                with open(state_file) as f:
                    data = json.load(f)
                    return data.get("created_at", datetime.now().isoformat())
        except Exception:
            pass
        return datetime.now().isoformat()

    def load_session(
        self, session_id: str
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
        """
        Load session state and messages from disk.

        Args:
            session_id: Session ID to load

        Returns:
            Tuple of (state_dict, messages_list, metadata_dict)

        Raises:
            FileNotFoundError: If session doesn't exist
        """
        session_dir = self._session_dir(session_id)

        state_file = session_dir / "session.json"
        messages_file = session_dir / "messages.json"

        if not state_file.exists():
            raise FileNotFoundError(f"Session not found: {session_id}")

        with open(state_file) as f:
            data = json.load(f)

        messages = []
        if messages_file.exists():
            with open(messages_file) as f:
                messages = json.load(f)

        metadata = {
            "id": data["id"],
            "title": data.get("title"),
            "workspace": data.get("workspace"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
        }

        return data.get("state", {}), messages, metadata

    def list_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        List all saved sessions, most recent first.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of session metadata dicts
        """
        sessions = []

        if not self.base_dir.exists():
            return sessions

        for session_dir in self.base_dir.iterdir():
            if not session_dir.is_dir():
                continue

            state_file = session_dir / "session.json"
            if not state_file.exists():
                continue

            try:
                with open(state_file) as f:
                    data = json.load(f)
                    sessions.append(
                        {
                            "id": data.get("id", session_dir.name),
                            "title": data.get("title", "Untitled"),
                            "workspace": data.get("workspace"),
                            "created_at": data.get("created_at"),
                            "updated_at": data.get("updated_at"),
                        }
                    )
            except Exception:
                # Skip corrupted sessions
                continue

        # Sort by updated_at, most recent first
        sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)

        return sessions[:limit]

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session ID to delete

        Returns:
            True if deleted, False if not found
        """
        session_dir = self._session_dir(session_id)
        if session_dir.exists():
            shutil.rmtree(session_dir)
            return True
        return False

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        state_file = self._session_dir(session_id) / "session.json"
        return state_file.exists()

    def get_latest_session(self, workspace: Optional[str] = None) -> Optional[str]:
        """
        Get the most recent session ID, optionally filtered by workspace.

        Args:
            workspace: If provided, only consider sessions for this workspace

        Returns:
            Session ID or None
        """
        sessions = self.list_sessions()

        if workspace:
            # Normalize workspace path
            workspace = os.path.abspath(workspace)
            sessions = [
                s
                for s in sessions
                if s.get("workspace") and os.path.abspath(s["workspace"]) == workspace
            ]

        if sessions:
            return sessions[0]["id"]
        return None

    @staticmethod
    def generate_session_id() -> str:
        """Generate a new unique session ID."""
        return f"ses_{uuid.uuid4().hex[:24]}"
