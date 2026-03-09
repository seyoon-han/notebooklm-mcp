"""Source management tools."""

import json
from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.auth import get_client


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def source_list(notebook_id: str) -> str:
        """List all sources in a notebook.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        sources = await client.sources.list(notebook_id)
        return json.dumps(
            [{"id": s.id, "title": s.title} for s in sources],
            indent=2,
        )

    @mcp.tool()
    async def source_get(notebook_id: str, source_id: str) -> str:
        """Get details of a specific source.

        Args:
            notebook_id: The notebook ID
            source_id: The source ID
        """
        client = await get_client()
        s = await client.sources.get(notebook_id, source_id)
        return json.dumps({"id": s.id, "title": s.title})

    @mcp.tool()
    async def source_get_fulltext(notebook_id: str, source_id: str) -> str:
        """Get the full indexed text content of a source.

        Args:
            notebook_id: The notebook ID
            source_id: The source ID
        """
        client = await get_client()
        fulltext = await client.sources.get_fulltext(notebook_id, source_id)
        return str(fulltext)

    @mcp.tool()
    async def source_get_guide(notebook_id: str, source_id: str) -> str:
        """Get AI-generated summary and keywords for a source.

        Args:
            notebook_id: The notebook ID
            source_id: The source ID
        """
        client = await get_client()
        guide = await client.sources.get_guide(notebook_id, source_id)
        return json.dumps(guide, indent=2)

    @mcp.tool()
    async def source_add_url(notebook_id: str, url: str) -> str:
        """Add a URL as a source to a notebook.

        Args:
            notebook_id: The notebook ID
            url: The URL to add
        """
        client = await get_client()
        s = await client.sources.add_url(notebook_id, url)
        return json.dumps({"id": s.id, "title": s.title})

    @mcp.tool()
    async def source_add_youtube(notebook_id: str, url: str) -> str:
        """Add a YouTube video as a source to a notebook.

        Args:
            notebook_id: The notebook ID
            url: The YouTube URL
        """
        client = await get_client()
        s = await client.sources.add_youtube(notebook_id, url)
        return json.dumps({"id": s.id, "title": s.title})

    @mcp.tool()
    async def source_add_text(notebook_id: str, title: str, content: str) -> str:
        """Add text content directly as a source.

        Args:
            notebook_id: The notebook ID
            title: Title for the source
            content: The text content
        """
        client = await get_client()
        s = await client.sources.add_text(notebook_id, title, content)
        return json.dumps({"id": s.id, "title": s.title})

    @mcp.tool()
    async def source_add_file(notebook_id: str, file_path: str) -> str:
        """Upload a local file as a source (PDF, TXT, etc.).

        Args:
            notebook_id: The notebook ID
            file_path: Absolute path to the file
        """
        from pathlib import Path

        client = await get_client()
        s = await client.sources.add_file(notebook_id, Path(file_path))
        return json.dumps({"id": s.id, "title": s.title})

    @mcp.tool()
    async def source_refresh(notebook_id: str, source_id: str) -> str:
        """Refresh a URL or Drive source to get updated content.

        Args:
            notebook_id: The notebook ID
            source_id: The source ID to refresh
        """
        client = await get_client()
        result = await client.sources.refresh(notebook_id, source_id)
        return json.dumps({"refreshed": result})

    @mcp.tool()
    async def source_delete(notebook_id: str, source_id: str) -> str:
        """Delete a source from a notebook.

        Args:
            notebook_id: The notebook ID
            source_id: The source ID to delete
        """
        client = await get_client()
        result = await client.sources.delete(notebook_id, source_id)
        return json.dumps({"deleted": result})
