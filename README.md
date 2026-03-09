# notebooklm-mcp

An MCP (Model Context Protocol) server that wraps [notebooklm-py](https://github.com/teng-lin/notebooklm-py), enabling Claude Code, Codex, and any MCP-compatible client to use the full Google NotebookLM API through natural language.

`notebooklm-py` is used as a pip dependency — the original project is never modified, so upstream updates can be adopted at any time.

## Why?

Google NotebookLM is a powerful tool that analyzes uploaded documents and auto-generates podcasts, quizzes, slides, and more. But it's locked behind a web UI.

**notebooklm-mcp** removes that limitation:

- **Natural language in Claude Code** — "Upload this project's docs to NotebookLM"
- **Integrated into dev workflow** — Write code → update docs → sync to NotebookLM in one flow
- **Project knowledge base** — Sync project docs to NotebookLM, then query and generate artifacts at any time

## Install

```bash
pip install notebooklm-mcp
```

Or install from source:

```bash
git clone https://github.com/seyoon-han/notebooklm-mcp.git
cd notebooklm-mcp
pip install -e .
```

## Setup

### 1. Authenticate with NotebookLM

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
notebooklm login
```

A browser window will open. Sign in with your Google account, wait for the NotebookLM homepage to load, then press Enter in the terminal.

### 2. Register the MCP Server

Create `.mcp.json` in your project root (or add to `~/.claude/settings.json` for global access):

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm-mcp"
    }
  }
}
```

Claude Code will automatically connect to the NotebookLM MCP server on startup.

## Tools (53)

Exposes the full NotebookLM API as MCP tools:

### Notebooks (7)
| Tool | Description |
|------|-------------|
| `notebook_list` | List all notebooks |
| `notebook_create` | Create a new notebook |
| `notebook_get` | Get notebook details |
| `notebook_delete` | Delete a notebook |
| `notebook_rename` | Rename a notebook |
| `notebook_get_description` | Get AI-generated description and topics |
| `notebook_get_summary` | Get notebook summary |

### Sources (10)
| Tool | Description |
|------|-------------|
| `source_add_url` | Add a URL as a source |
| `source_add_youtube` | Add a YouTube video as a source |
| `source_add_text` | Add text content as a source |
| `source_add_file` | Upload a local file (PDF, etc.) |
| `source_list` | List all sources |
| `source_get` | Get source details |
| `source_get_fulltext` | Get full indexed text of a source |
| `source_get_guide` | Get AI-generated summary and keywords |
| `source_refresh` | Refresh a URL/Drive source |
| `source_delete` | Delete a source |

### Chat (2)
| Tool | Description |
|------|-------------|
| `chat_ask` | Ask questions with citations (multi-turn supported) |
| `chat_get_history` | Get conversation history |

### Artifacts — Generate (9)
| Tool | Description |
|------|-------------|
| `generate_audio` | Podcast-style audio (4 formats, 3 lengths, 50+ languages) |
| `generate_video` | Video overview (2 formats, 9 visual styles) |
| `generate_quiz` | Quiz with configurable difficulty and count |
| `generate_flashcards` | Flashcard generation |
| `generate_slide_deck` | Slide deck (PDF/PPTX) |
| `generate_infographic` | Infographic (3 orientations, 3 detail levels) |
| `generate_mind_map` | Mind map (hierarchical JSON) |
| `generate_report` | Report (study guide, FAQ, timeline, etc.) |
| `generate_data_table` | Data table (CSV) |

### Artifacts — Download (9)
| Tool | Description |
|------|-------------|
| `download_audio` | Save as MP3/MP4 |
| `download_video` | Save as MP4 |
| `download_quiz` | Save as JSON/Markdown/HTML |
| `download_flashcards` | Save as JSON/Markdown/HTML |
| `download_slide_deck` | Save as PDF/PPTX |
| `download_infographic` | Save as PNG |
| `download_report` | Save as Markdown |
| `download_mind_map` | Save as JSON |
| `download_data_table` | Save as CSV |

### Artifacts — Management (3)
| Tool | Description |
|------|-------------|
| `artifact_list` | List generated artifacts |
| `artifact_wait` | Wait for generation task to complete |
| `artifact_poll_status` | Check generation task status |

### Research (3)
| Tool | Description |
|------|-------------|
| `research_start` | Start web/Drive research (fast/deep mode) |
| `research_poll` | Check research progress |
| `research_import_sources` | Import discovered sources into notebook |

### Notes (5)
| Tool | Description |
|------|-------------|
| `note_list` | List notes |
| `note_create` | Create a note |
| `note_get` | Get note content |
| `note_update` | Update a note |
| `note_delete` | Delete a note |

### Sharing (4)
| Tool | Description |
|------|-------------|
| `sharing_get_status` | Get sharing status |
| `sharing_set_public` | Toggle public/private |
| `sharing_add_user` | Share with a user (viewer/editor) |
| `sharing_remove_user` | Revoke access |

## Claude Code Skill: notebooklm-sync

A bundled Claude Code skill that automatically syncs project documents with NotebookLM.

### Install

Copy the project-level skill to your personal skills directory:

```bash
cp -r .claude/skills/notebooklm-sync ~/.claude/skills/
```

### Features

- **Auto-detect**: Suggests "Sync to NotebookLM?" when you modify tracked document files
- **Hash-based change detection**: Only syncs files that actually changed (md5)
- **Project config**: `.notebooklm.json` tracks file patterns and source mappings
- **Artifact suggestions**: Suggests generating podcasts, quizzes, or slides after milestones

## Usage Examples

### Example 1: Register Project Docs

```
You: "Upload this project's docs to NotebookLM"

Claude: Detected project documents:
  - README.md
  - docs/plans/design.md
  - CLAUDE.md

  Created notebook "my-project docs" and uploaded 3 files.
  Saved .notebooklm.json.
```

### Example 2: Ask About Your Project

```
You: "Explain this project's architecture — check NotebookLM"

Claude: [calls chat_ask]

  This project is a FastMCP-based MCP server wrapping notebooklm-py.
  It consists of 7 modules (notebooks, sources, chat, artifacts, research,
  notes, sharing), each exposing NotebookLMClient async methods as thin
  wrappers... [with citations]
```

### Example 3: Auto-Sync After Doc Changes

```
You: [edits README.md]

Claude: README.md has changed. Sync to NotebookLM?

You: "Yes"

Claude: Updated README.md in NotebookLM.
  (deleted old source → added new source, hash updated)
```

### Example 4: Generate a Podcast

```
You: "Create a podcast from this project's docs"

Claude: [generate_audio → artifact_wait → download_audio]

  Generated podcast: ./project-podcast.mp4
  (Two hosts discussing the project, ~10 minutes)
```

### Example 5: Generate an Onboarding Quiz

```
You: "Make a quiz about this project for new team members"

Claude: [generate_quiz → artifact_wait → download_quiz]

  Saved to quiz.json. 15 questions, medium difficulty.
  Topics: MCP protocol, tool structure, auth flow
```

### Example 6: Web Research → Add Sources

```
You: "Research the latest MCP protocol docs and add them to the notebook"

Claude: [research_start → research_poll → research_import_sources]

  Found and imported 3 relevant documents:
  - Model Context Protocol Specification
  - MCP Server Development Guide
  - FastMCP Python SDK Reference
```

## Architecture

```
notebooklm-mcp/
├── .mcp.json                        # MCP server config
├── .notebooklm.json                 # Project ↔ NotebookLM sync config
├── .claude/skills/notebooklm-sync/  # Claude Code skill
│   └── SKILL.md
├── pyproject.toml
├── src/notebooklm_mcp/
│   ├── __init__.py
│   ├── __main__.py                  # python -m notebooklm_mcp
│   ├── server.py                    # FastMCP server + tool registration
│   ├── auth.py                      # NotebookLMClient lifecycle
│   └── tools/
│       ├── notebooks.py             # Notebook CRUD
│       ├── sources.py               # Source management
│       ├── chat.py                  # Q&A with citations
│       ├── artifacts.py             # Artifact generation & download
│       ├── research.py              # Web/Drive research
│       ├── notes.py                 # Note CRUD
│       └── sharing.py               # Sharing & permissions
└── docs/plans/                      # Design documents
```

**Design principles:**
- `notebooklm-py` is a pip dependency only (original untouched)
- Each tool is a thin async wrapper around `NotebookLMClient` methods
- Client is lazily initialized on first tool call via `from_storage()`
- All tools return JSON strings for easy parsing by MCP clients

## License

MIT
