from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..models import Note, NoteCreate, NoteUpdate, NotesList
from ..storage import NotesRepository, get_repository

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get(
    "",
    response_model=NotesList,
    summary="List notes",
    description="List notes with optional case-insensitive search over title and content, with pagination.",
)
# PUBLIC_INTERFACE
def list_notes(
    q: Optional[str] = Query(None, description="Optional case-insensitive substring to search in title or content"),
    skip: int = Query(0, ge=0, description="Number of items to skip for pagination"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of items to return"),
    repo: NotesRepository = Depends(get_repository),
):
    """List notes with optional search and pagination."""
    items = repo.list(q=q, skip=skip, limit=limit)
    total = repo.total(q=q)
    return NotesList(items=items, total=total, skip=skip, limit=limit)


@router.post(
    "",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note. The server generates the UUID id and timestamps.",
)
# PUBLIC_INTERFACE
def create_note(
    payload: NoteCreate,
    repo: NotesRepository = Depends(get_repository),
):
    """Create a new note with server-generated id and timestamps."""
    note = repo.create(payload)
    return note


@router.get(
    "/{note_id}",
    response_model=Note,
    summary="Get note",
    description="Retrieve a single note by its UUID.",
)
# PUBLIC_INTERFACE
def get_note(
    note_id: UUID,
    repo: NotesRepository = Depends(get_repository),
):
    """Retrieve a note by id or return 404 if not found."""
    note = repo.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.put(
    "/{note_id}",
    response_model=Note,
    summary="Update note",
    description="Update an existing note. Only provided fields are updated.",
)
# PUBLIC_INTERFACE
def update_note(
    note_id: UUID,
    payload: NoteUpdate,
    repo: NotesRepository = Depends(get_repository),
):
    """Update an existing note or return 404 if not found."""
    updated = repo.update(note_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return updated


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note by its UUID. Returns 204 No Content on success.",
)
# PUBLIC_INTERFACE
def delete_note(
    note_id: UUID,
    repo: NotesRepository = Depends(get_repository),
):
    """Delete a note or return 404 if not found."""
    removed = repo.delete(note_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    # 204 No Content responses should return None
    return None
