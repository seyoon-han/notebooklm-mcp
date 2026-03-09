"""NotebookLM MCP Server — exposes notebooklm-py as MCP tools."""

from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.tools import notebooks, sources, chat, artifacts, research, notes, sharing

mcp = FastMCP(
    "notebooklm",
    instructions=(
        "NotebookLM MCP Server. Provides tools to manage Google NotebookLM "
        "notebooks, sources, chat, artifact generation (audio, video, quizzes, "
        "slides, infographics, mind maps, reports, data tables), research, "
        "notes, and sharing. Requires prior authentication via `notebooklm login`."
    ),
)

# Register all tool modules
notebooks.register(mcp)
sources.register(mcp)
chat.register(mcp)
artifacts.register(mcp)
research.register(mcp)
notes.register(mcp)
sharing.register(mcp)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
