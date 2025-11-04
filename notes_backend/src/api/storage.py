from __future__ import annotations

import threading
from typing import Dict, List, Optional
from uuid import UUID

from .models import Note, NoteCreate, NoteUpdate, new_note_from_create, utcnow


# PUBLIC_INTERFACE
class NotesRepository:
    """Repository interface for notes storage."""

    def list(self, q: Optional[str], skip: int, limit: int) -> List[Note]:
        """List notes with optional search and pagination."""
        raise NotImplementedError

    def total(self, q: Optional[str]) -> int:
        """Total count of notes matching the optional search."""
        raise NotImplementedError

    def get(self, note_id: UUID) -> Optional[Note]:
        """Retrieve a single note by id."""
        raise NotImplementedError

    def create(self, data: NoteCreate) -> Note:
        """Create and persist a new note."""
        raise NotImplementedError

    def update(self, note_id: UUID, data: NoteUpdate) -> Optional[Note]:
        """Update an existing note by id, returning None if not found."""
        raise NotImplementedError

    def delete(self, note_id: UUID) -> bool:
        """Delete a note by id. Returns True if deleted, False if not found."""
        raise NotImplementedError


class InMemoryNotesRepository(NotesRepository):
    """Thread-safe in-memory repository backed by a dict[UUID, Note]."""

    def __init__(self) -> None:
        self._store: Dict[UUID, Note] = {}
        self._lock = threading.Lock()

    def list(self, q: Optional[str], skip: int, limit: int) -> List[Note]:
        # Read operations can be done without lock for performance, but to keep it simple and safe,
        # we copy under lock to avoid race conditions with writes.
        with self._lock:
            values = list(self._store.values())

        if q:
            q_lower = q.lower()
            values = [
                n
                for n in values
                if (n.title and q_lower in n.title.lower())
                or (n.content and q_lower in n.content.lower())
            ]

        # Sort by updated_at desc then created_at desc for consistent results
        values.sort(key=lambda n: (n.updated_at, n.created_at), reverse=True)
        return values[skip : skip + limit]

    def total(self, q: Optional[str]) -> int:
        with self._lock:
            values = list(self._store.values())
        if q:
            q_lower = q.lower()
            values = [
                n
                for n in values
                if (n.title and q_lower in n.title.lower())
                or (n.content and q_lower in n.content.lower())
            ]
        return len(values)

    def get(self, note_id: UUID) -> Optional[Note]:
        with self._lock:
            return self._store.get(note_id)

    def create(self, data: NoteCreate) -> Note:
        note = new_note_from_create(data)
        with self._lock:
            self._store[note.id] = note
        return note

    def update(self, note_id: UUID, data: NoteUpdate) -> Optional[Note]:
        with self._lock:
            note = self._store.get(note_id)
            if note is None:
                return None
            updated = note.model_copy(
                update={
                    "title": data.title if data.title is not None else note.title,
                    "content": data.content if data.content is not None else note.content,
                    "updated_at": utcnow(),
                }
            )
            self._store[note_id] = updated
            return updated

    def delete(self, note_id: UUID) -> bool:
        with self._lock:
            if note_id in self._store:
                del self._store[note_id]
                return True
            return False


# Simple DI factory
_repo_singleton: Optional[InMemoryNotesRepository] = None


# PUBLIC_INTERFACE
def get_repository() -> NotesRepository:
    """FastAPI dependency provider for the notes repository (singleton in-memory)."""
    global _repo_singleton
    if _repo_singleton is None:
        _repo_singleton = InMemoryNotesRepository()
    return _repo_singleton
