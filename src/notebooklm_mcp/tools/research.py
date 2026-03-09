"""Research tools for web and Drive search."""

import json
from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.auth import get_client


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def research_start(
        notebook_id: str,
        query: str,
        source: str = "web",
        mode: str = "fast",
    ) -> str:
        """Start a research task to find and import sources.

        Args:
            notebook_id: The notebook ID
            query: What to research
            source: Where to search: web or drive (default: web)
            mode: Search depth: fast or deep (default: fast)
        """
        client = await get_client()
        result = await client.research.start(
            notebook_id, query, source=source, mode=mode
        )
        return json.dumps(result, indent=2, default=str)

    @mcp.tool()
    async def research_poll(notebook_id: str) -> str:
        """Check the status of an ongoing research task.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        result = await client.research.poll(notebook_id)
        return json.dumps(result, indent=2, default=str)

    @mcp.tool()
    async def research_import_sources(
        notebook_id: str, task_id: str, sources: list[dict]
    ) -> str:
        """Import discovered research sources into the notebook.

        Args:
            notebook_id: The notebook ID
            task_id: The task ID from research_start
            sources: List of source dicts from research_poll results
        """
        client = await get_client()
        result = await client.research.import_sources(
            notebook_id, task_id, sources
        )
        return json.dumps(result, indent=2, default=str)
