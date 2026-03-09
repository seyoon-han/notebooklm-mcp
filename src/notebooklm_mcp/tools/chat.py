"""Chat tools for querying notebook sources."""

import json
from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.auth import get_client


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def chat_ask(
        notebook_id: str,
        question: str,
        source_ids: list[str] | None = None,
        conversation_id: str | None = None,
    ) -> str:
        """Ask a question about the notebook's sources. Supports multi-turn conversation.

        Args:
            notebook_id: The notebook ID
            question: The question to ask
            source_ids: Optional list of source IDs to restrict the query to
            conversation_id: Optional conversation ID for follow-up questions
        """
        client = await get_client()
        result = await client.chat.ask(
            notebook_id,
            question,
            source_ids=source_ids,
            conversation_id=conversation_id,
        )
        references = []
        if hasattr(result, "references") and result.references:
            references = [
                {
                    "citation_number": ref.citation_number,
                    "source_id": ref.source_id,
                }
                for ref in result.references
            ]
        return json.dumps(
            {
                "answer": result.answer,
                "conversation_id": getattr(result, "conversation_id", None),
                "references": references,
            },
            indent=2,
        )

    @mcp.tool()
    async def chat_get_history(
        notebook_id: str,
        limit: int = 100,
        conversation_id: str | None = None,
    ) -> str:
        """Get conversation history for a notebook.

        Args:
            notebook_id: The notebook ID
            limit: Max number of Q&A pairs to return (default 100)
            conversation_id: Optional specific conversation ID
        """
        client = await get_client()
        history = await client.chat.get_history(
            notebook_id, limit=limit, conversation_id=conversation_id
        )
        return json.dumps(
            [{"question": q, "answer": a} for q, a in history],
            indent=2,
        )
