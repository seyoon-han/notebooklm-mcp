"""Client lifecycle management for NotebookLM."""

from notebooklm import NotebookLMClient

_client: NotebookLMClient | None = None


async def get_client() -> NotebookLMClient:
    """Get or create the NotebookLM client (lazy singleton)."""
    global _client
    if _client is None:
        client = await NotebookLMClient.from_storage()
        _client = await client.__aenter__()
    return _client


async def shutdown_client() -> None:
    """Close the client connection if open."""
    global _client
    if _client is not None:
        await _client.__aexit__(None, None, None)
        _client = None
