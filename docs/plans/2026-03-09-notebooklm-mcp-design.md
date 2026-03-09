# NotebookLM MCP Server Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Wrap notebooklm-py as an MCP server so any MCP client can use NotebookLM features natively.

**Architecture:** pip dependency on notebooklm-py, FastMCP server with ~40 tools organized into modules (notebooks, sources, chat, artifacts, research, notes, sharing). Lazy client initialization via `from_storage()`.

**Tech Stack:** Python 3.10+, mcp[cli] (FastMCP), notebooklm-py

---

### Task 1: Project scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `src/notebooklm_mcp/__init__.py`
- Create: `src/notebooklm_mcp/__main__.py`

### Task 2: Server core + client lifecycle

**Files:**
- Create: `src/notebooklm_mcp/server.py`
- Create: `src/notebooklm_mcp/auth.py`

### Task 3: Notebook tools

**Files:**
- Create: `src/notebooklm_mcp/tools/__init__.py`
- Create: `src/notebooklm_mcp/tools/notebooks.py`

### Task 4: Source tools

**Files:**
- Create: `src/notebooklm_mcp/tools/sources.py`

### Task 5: Chat tools

**Files:**
- Create: `src/notebooklm_mcp/tools/chat.py`

### Task 6: Artifact tools (generate + download)

**Files:**
- Create: `src/notebooklm_mcp/tools/artifacts.py`

### Task 7: Research, Notes, Sharing tools

**Files:**
- Create: `src/notebooklm_mcp/tools/research.py`
- Create: `src/notebooklm_mcp/tools/notes.py`
- Create: `src/notebooklm_mcp/tools/sharing.py`
