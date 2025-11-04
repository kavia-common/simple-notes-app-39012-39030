from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base fields for a Note used across create/update operations."""

    title: str = Field(..., description="Title of the note", min_length=1, max_length=200)
    content: Optional[str] = Field(None, description="Optional content/body of the note", max_length=10000)


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating an existing note. All fields optional."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=200)
    content: Optional[str] = Field(None, description="Updated content of the note", max_length=10000)


# PUBLIC_INTERFACE
class Note(NoteBase):
    """The complete Note model returned in API responses."""
    id: UUID = Field(..., description="Unique identifier for the note (UUID)")
    created_at: datetime = Field(..., description="UTC timestamp when the note was created")
    updated_at: datetime = Field(..., description="UTC timestamp when the note was last updated")

    model_config = ConfigDict(from_attributes=True)


# PUBLIC_INTERFACE
class NotesList(BaseModel):
    """Container for list responses to allow future extension with metadata."""
    items: List[Note] = Field(..., description="List of notes matching the query")
    total: int = Field(..., description="Total count of notes matching the query (before pagination)")
    skip: int = Field(..., description="Number of items skipped for pagination")
    limit: int = Field(..., description="Maximum number of items returned")


# Utility for timestamps
def utcnow() -> datetime:
    """Return a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


# PUBLIC_INTERFACE
def new_note_from_create(data: NoteCreate) -> Note:
    """Create a new Note object from NoteCreate with server-generated fields."""
    now = utcnow()
    return Note(
        id=uuid4(),
        title=data.title,
        content=data.content,
        created_at=now,
        updated_at=now,
    )
