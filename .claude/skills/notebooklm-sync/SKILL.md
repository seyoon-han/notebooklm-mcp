---
name: notebooklm-sync
description: Use when creating, modifying, or reviewing project documentation files (README, CLAUDE.md, docs/, plans/). Use when the user mentions NotebookLM, project knowledge base, or documentation sync. Use when suggesting documentation updates after completing features or plans.
---

# NotebookLM Project Sync

Sync project documents to Google NotebookLM as a living knowledge base. Keeps NotebookLM as the source of truth for any project.

## Prerequisites

- `notebooklm-mcp` MCP server running (tools prefixed with `mcp__notebooklm__`)
- User authenticated via `notebooklm login`

## Core Workflows

### 1. Initialize Project Notebook

When a project has no `.notebooklm.json` yet:

```
1. Ask user: "Set up NotebookLM for this project?"
2. Call notebook_create with project name
3. Detect doc files: README.md, CLAUDE.md, docs/**/*.md, *.md in root
4. Upload each as text source (read file → source_add_text)
5. Save .notebooklm.json to project root
```

**`.notebooklm.json` format:**
```json
{
  "notebook_id": "<id>",
  "notebook_title": "<project-name> docs",
  "tracked_patterns": ["README.md", "CLAUDE.md", "docs/**/*.md"],
  "sources": {
    "README.md": {
      "source_id": "<id>",
      "content_hash": "<md5>"
    }
  }
}
```

### 2. Sync Documents

When docs are modified or user requests sync:

```
1. Read .notebooklm.json
2. Glob tracked_patterns to find all matching files
3. For each file:
   - Compute md5 hash of current content
   - If hash differs from stored → file changed
   - If no stored entry → new file
4. For changed files: delete old source, add new source
5. For new files: add source
6. For deleted files: remove source entry
7. Update .notebooklm.json with new hashes and source IDs
```

### 3. Auto-Detect Suggestions

After modifying any tracked document file, suggest:
> "This file is tracked by NotebookLM. Sync now?"

Trigger on: writing/editing files matching tracked_patterns in `.notebooklm.json`.

### 4. Query Project Knowledge

Use `chat_ask` with the project notebook to:
- Answer questions about project architecture
- Cross-reference documentation
- Find inconsistencies between docs

### 5. Generate Artifacts

Offer artifact generation when useful:
- **After major milestone**: "Generate an audio overview of the project?"
- **For onboarding**: "Generate a quiz about the codebase?"
- **For presentations**: "Generate slides from the docs?"

## Implementation Notes

**Hashing:** Use Python's hashlib.md5 via Bash to compute content hashes:
```bash
md5 -q <file>
```

**Source updates:** NotebookLM has no source update API. To update: delete old source → add new source with same title.

**File reading:** Read file content, then call `source_add_text(notebook_id, title, content)`. Use the relative path as the title for easy identification.

**Large files:** If a file exceeds 500KB, warn the user before uploading.

## Quick Reference

| Action | MCP Tools |
|--------|-----------|
| Create notebook | `notebook_create` |
| Add doc as source | `source_add_text` |
| Upload binary file | `source_add_file` |
| Remove old source | `source_delete` |
| List sources | `source_list` |
| Ask about project | `chat_ask` |
| Generate podcast | `generate_audio` → `artifact_wait` → `download_audio` |
| Generate quiz | `generate_quiz` → `artifact_wait` → `download_quiz` |
| Generate slides | `generate_slide_deck` → `artifact_wait` → `download_slide_deck` |

## Common Mistakes

- **Forgetting to wait**: Generation tools return a task_id. Must call `artifact_wait` before downloading.
- **Duplicate sources**: Always check `.notebooklm.json` before adding. Don't add same file twice.
- **Stale config**: If `.notebooklm.json` exists but notebook was deleted, detect the error and offer to reinitialize.
