"""Note management tools."""

import json
from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.auth import get_client


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def note_list(notebook_id: str) -> str:
        """List all notes in a notebook.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        notes = await client.notes.list(notebook_id)
        return json.dumps(
            [{"id": n.id, "title": getattr(n, "title", None)} for n in notes],
            indent=2,
        )

    @mcp.tool()
    async def note_create(
        notebook_id: str, title: str = "New Note", content: str = ""
    ) -> str:
        """Create a new note in a notebook.

        Args:
            notebook_id: The notebook ID
            title: Note title (default: "New Note")
            content: Note content
        """
        client = await get_client()
        note = await client.notes.create(notebook_id, title=title, content=content)
        return json.dumps({"id": note.id, "title": getattr(note, "title", None)})

    @mcp.tool()
    async def note_get(notebook_id: str, note_id: str) -> str:
        """Get a specific note's content.

        Args:
            notebook_id: The notebook ID
            note_id: The note ID
        """
        client = await get_client()
        note = await client.notes.get(notebook_id, note_id)
        if note is None:
            return json.dumps({"error": "Note not found"})
        return json.dumps({
            "id": note.id,
            "title": getattr(note, "title", None),
            "content": getattr(note, "content", None),
        })

    @mcp.tool()
    async def note_update(
        notebook_id: str, note_id: str, content: str, title: str
    ) -> str:
        """Update a note's content and title.

        Args:
            notebook_id: The notebook ID
            note_id: The note ID
            content: New content
            title: New title
        """
        client = await get_client()
        await client.notes.update(notebook_id, note_id, content=content, title=title)
        return json.dumps({"updated": True})

    @mcp.tool()
    async def note_delete(notebook_id: str, note_id: str) -> str:
        """Delete a note.

        Args:
            notebook_id: The notebook ID
            note_id: The note ID
        """
        client = await get_client()
        result = await client.notes.delete(notebook_id, note_id)
        return json.dumps({"deleted": result})
