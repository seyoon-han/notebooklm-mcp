"""Notebook management tools."""

import json
from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.auth import get_client


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def notebook_list() -> str:
        """List all notebooks in the user's NotebookLM account."""
        client = await get_client()
        notebooks = await client.notebooks.list()
        return json.dumps(
            [{"id": nb.id, "title": nb.title} for nb in notebooks],
            indent=2,
        )

    @mcp.tool()
    async def notebook_create(title: str) -> str:
        """Create a new notebook.

        Args:
            title: Name for the new notebook
        """
        client = await get_client()
        nb = await client.notebooks.create(title)
        return json.dumps({"id": nb.id, "title": nb.title})

    @mcp.tool()
    async def notebook_get(notebook_id: str) -> str:
        """Get details of a specific notebook.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        nb = await client.notebooks.get(notebook_id)
        return json.dumps({"id": nb.id, "title": nb.title})

    @mcp.tool()
    async def notebook_delete(notebook_id: str) -> str:
        """Delete a notebook.

        Args:
            notebook_id: The notebook ID to delete
        """
        client = await get_client()
        result = await client.notebooks.delete(notebook_id)
        return json.dumps({"deleted": result})

    @mcp.tool()
    async def notebook_rename(notebook_id: str, new_title: str) -> str:
        """Rename a notebook.

        Args:
            notebook_id: The notebook ID
            new_title: New title for the notebook
        """
        client = await get_client()
        nb = await client.notebooks.rename(notebook_id, new_title)
        return json.dumps({"id": nb.id, "title": nb.title})

    @mcp.tool()
    async def notebook_get_description(notebook_id: str) -> str:
        """Get AI-generated description and topics for a notebook.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        desc = await client.notebooks.get_description(notebook_id)
        return str(desc)

    @mcp.tool()
    async def notebook_get_summary(notebook_id: str) -> str:
        """Get a text summary of a notebook's contents.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        return await client.notebooks.get_summary(notebook_id)
