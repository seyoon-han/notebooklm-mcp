# notebooklm-mcp

MCP server wrapping [notebooklm-py](https://github.com/teng-lin/notebooklm-py) for use with Claude Code, Codex, and other MCP clients.

## Install

```bash
pip install notebooklm-mcp
```

## Setup

1. Authenticate first:
```bash
pip install "notebooklm-py[browser]"
playwright install chromium
notebooklm login
```

2. Add to your MCP config (e.g. `.mcp.json`):
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm-mcp"
    }
  }
}
```

## Tools

~40 tools covering the full NotebookLM API:

- **Notebooks**: create, list, get, delete, rename, describe, summarize
- **Sources**: add URL/YouTube/file/text, list, get fulltext, refresh, delete
- **Chat**: ask questions with citations, conversation history
- **Artifacts**: generate and download audio, video, quizzes, flashcards, slides, infographics, mind maps, reports, data tables
- **Research**: web/Drive search with auto-import
- **Notes**: CRUD operations
- **Sharing**: public/private toggle, user permissions
