# notebooklm-mcp

Google NotebookLM을 MCP(Model Context Protocol) 서버로 래핑하여, Claude Code, Codex 등 MCP 클라이언트에서 NotebookLM의 모든 기능을 자연어로 사용할 수 있게 해주는 프로젝트입니다.

[notebooklm-py](https://github.com/teng-lin/notebooklm-py)를 pip 의존성으로 래핑하며, 원본 프로젝트는 수정하지 않아 업스트림 업데이트를 그대로 반영할 수 있습니다.

## Why?

NotebookLM은 문서를 업로드하면 AI가 분석하고, 팟캐스트/퀴즈/슬라이드 등을 자동 생성해주는 강력한 도구입니다. 하지만 웹 UI에서만 사용할 수 있다는 한계가 있습니다.

**notebooklm-mcp**는 이 한계를 없앱니다:

- **Claude Code에서 자연어로** — "이 프로젝트 문서를 NotebookLM에 올려줘"
- **개발 워크플로우에 통합** — 코드 작성 → 문서 업데이트 → NotebookLM 동기화를 하나의 흐름으로
- **프로젝트 지식 베이스** — 프로젝트 문서를 NotebookLM에 동기화하여 언제든 질문하고, 아티팩트를 생성

## Install

```bash
pip install notebooklm-mcp
```

또는 소스에서 설치:

```bash
git clone https://github.com/seyoon-han/notebooklm-mcp.git
cd notebooklm-mcp
pip install -e .
```

## Setup

### 1. NotebookLM 인증

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
notebooklm login
```

브라우저가 열리면 Google 계정으로 로그인하고, NotebookLM 메인 페이지가 로드되면 터미널에서 Enter.

### 2. MCP 서버 등록

프로젝트 루트에 `.mcp.json` 생성 (또는 `~/.claude/settings.json`에 글로벌 등록):

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm-mcp"
    }
  }
}
```

이후 Claude Code를 열면 자동으로 NotebookLM MCP 서버에 연결됩니다.

## Tools (53개)

전체 NotebookLM API를 MCP 도구로 노출합니다:

### Notebooks (7)
| Tool | Description |
|------|-------------|
| `notebook_list` | 모든 노트북 목록 조회 |
| `notebook_create` | 새 노트북 생성 |
| `notebook_get` | 노트북 상세 정보 |
| `notebook_delete` | 노트북 삭제 |
| `notebook_rename` | 노트북 이름 변경 |
| `notebook_get_description` | AI 생성 설명 및 토픽 |
| `notebook_get_summary` | 노트북 요약 |

### Sources (10)
| Tool | Description |
|------|-------------|
| `source_add_url` | URL을 소스로 추가 |
| `source_add_youtube` | YouTube 영상을 소스로 추가 |
| `source_add_text` | 텍스트 콘텐츠를 소스로 추가 |
| `source_add_file` | 로컬 파일(PDF 등)을 소스로 업로드 |
| `source_list` | 소스 목록 조회 |
| `source_get` | 소스 상세 정보 |
| `source_get_fulltext` | 소스의 전체 인덱싱된 텍스트 |
| `source_get_guide` | AI 생성 소스 요약/키워드 |
| `source_refresh` | URL/Drive 소스 새로고침 |
| `source_delete` | 소스 삭제 |

### Chat (2)
| Tool | Description |
|------|-------------|
| `chat_ask` | 소스 기반 질문 (인용 포함, 멀티턴 대화 지원) |
| `chat_get_history` | 대화 기록 조회 |

### Artifacts — Generate (9)
| Tool | Description |
|------|-------------|
| `generate_audio` | 팟캐스트 스타일 오디오 생성 (4 포맷, 3 길이, 50+ 언어) |
| `generate_video` | 비디오 생성 (2 포맷, 9 비주얼 스타일) |
| `generate_quiz` | 퀴즈 생성 (난이도/수량 설정) |
| `generate_flashcards` | 플래시카드 생성 |
| `generate_slide_deck` | 슬라이드 덱 생성 (PDF/PPTX) |
| `generate_infographic` | 인포그래픽 생성 (3 방향, 3 상세도) |
| `generate_mind_map` | 마인드맵 생성 (JSON) |
| `generate_report` | 리포트 생성 (study guide, FAQ, timeline 등) |
| `generate_data_table` | 데이터 테이블 생성 (CSV) |

### Artifacts — Download (9)
| Tool | Description |
|------|-------------|
| `download_audio` | MP3/MP4로 저장 |
| `download_video` | MP4로 저장 |
| `download_quiz` | JSON/Markdown/HTML로 저장 |
| `download_flashcards` | JSON/Markdown/HTML로 저장 |
| `download_slide_deck` | PDF/PPTX로 저장 |
| `download_infographic` | PNG로 저장 |
| `download_report` | Markdown으로 저장 |
| `download_mind_map` | JSON으로 저장 |
| `download_data_table` | CSV로 저장 |

### Artifacts — Management (3)
| Tool | Description |
|------|-------------|
| `artifact_list` | 생성된 아티팩트 목록 |
| `artifact_wait` | 생성 작업 완료 대기 |
| `artifact_poll_status` | 생성 작업 상태 확인 |

### Research (3)
| Tool | Description |
|------|-------------|
| `research_start` | 웹/Drive 리서치 시작 (fast/deep 모드) |
| `research_poll` | 리서치 진행 상태 확인 |
| `research_import_sources` | 발견된 소스를 노트북에 임포트 |

### Notes (5)
| Tool | Description |
|------|-------------|
| `note_list` | 노트 목록 |
| `note_create` | 노트 생성 |
| `note_get` | 노트 내용 조회 |
| `note_update` | 노트 수정 |
| `note_delete` | 노트 삭제 |

### Sharing (4)
| Tool | Description |
|------|-------------|
| `sharing_get_status` | 공유 상태 확인 |
| `sharing_set_public` | 공개/비공개 전환 |
| `sharing_add_user` | 사용자에게 공유 (viewer/editor) |
| `sharing_remove_user` | 공유 해제 |

## Claude Code Skill: notebooklm-sync

프로젝트 문서를 NotebookLM과 자동 동기화하는 Claude Code skill이 포함되어 있습니다.

### 설치

프로젝트의 `.claude/skills/notebooklm-sync/` 디렉토리를 복사하거나, 개인 skill로 설치:

```bash
cp -r .claude/skills/notebooklm-sync ~/.claude/skills/
```

### 주요 기능

- **자동 감지**: 문서 파일 수정 시 "NotebookLM에도 동기화할까요?" 제안
- **해시 기반 변경 감지**: md5 해시로 변경된 파일만 효율적으로 동기화
- **프로젝트 설정 파일**: `.notebooklm.json`으로 추적 대상 패턴과 소스 매핑 관리
- **아티팩트 생성 가이드**: 마일스톤 달성 시 팟캐스트, 퀴즈, 슬라이드 생성 제안

## Usage Examples

### Example 1: 프로젝트 문서를 NotebookLM에 등록

```
You: "이 프로젝트의 문서를 NotebookLM에 올려줘"

Claude: 프로젝트 문서를 감지했습니다:
  - README.md
  - docs/plans/design.md
  - CLAUDE.md

  NotebookLM 노트북 "my-project docs"를 생성하고 3개 파일을 업로드했습니다.
  .notebooklm.json을 저장했습니다.
```

### Example 2: 프로젝트에 대해 질문하기

```
You: "이 프로젝트의 아키텍처를 설명해줘 — NotebookLM에서 찾아봐"

Claude: [chat_ask 호출]

  이 프로젝트는 FastMCP 기반 MCP 서버로, notebooklm-py를 래핑합니다.
  7개 모듈(notebooks, sources, chat, artifacts, research, notes, sharing)로
  구성되며, 각 모듈은 NotebookLMClient의 async 메서드를 thin wrapper로
  노출합니다... [인용 포함]
```

### Example 3: 문서 변경 후 자동 동기화

```
You: [README.md를 수정]

Claude: README.md가 변경되었습니다. NotebookLM에도 동기화할까요?

You: "응"

Claude: README.md를 NotebookLM에 업데이트했습니다.
  (이전 소스 삭제 → 새 소스 추가, 해시 갱신)
```

### Example 4: 팟캐스트 생성

```
You: "이 프로젝트 문서로 팟캐스트 만들어줘"

Claude: [generate_audio 호출 → artifact_wait → download_audio]

  팟캐스트를 생성했습니다: ./project-podcast.mp4
  (2명의 호스트가 프로젝트에 대해 토론하는 형식, 약 10분)
```

### Example 5: 온보딩 퀴즈 생성

```
You: "신규 팀원용으로 이 프로젝트 퀴즈 만들어줘"

Claude: [generate_quiz 호출 → artifact_wait → download_quiz]

  quiz.json으로 저장했습니다. 15문제, 중간 난이도.
  주요 토픽: MCP 프로토콜, 도구 구조, 인증 흐름
```

### Example 6: 웹 리서치 → 소스 추가

```
You: "MCP 프로토콜 관련 최신 자료를 리서치해서 노트북에 추가해줘"

Claude: [research_start(query="MCP protocol", source="web") → research_poll → research_import_sources]

  3개의 관련 문서를 발견하고 노트북에 추가했습니다:
  - Model Context Protocol Specification
  - MCP Server Development Guide
  - FastMCP Python SDK Reference
```

## Architecture

```
notebooklm-mcp/
├── .mcp.json                        # MCP 서버 설정
├── .notebooklm.json                 # 프로젝트 ↔ NotebookLM 동기화 설정
├── .claude/skills/notebooklm-sync/  # Claude Code skill
│   └── SKILL.md
├── pyproject.toml
├── src/notebooklm_mcp/
│   ├── __init__.py
│   ├── __main__.py                  # python -m notebooklm_mcp
│   ├── server.py                    # FastMCP 서버 + 도구 등록
│   ├── auth.py                      # NotebookLMClient 라이프사이클
│   └── tools/
│       ├── notebooks.py             # 노트북 CRUD
│       ├── sources.py               # 소스 관리
│       ├── chat.py                  # 질의응답
│       ├── artifacts.py             # 아티팩트 생성/다운로드
│       ├── research.py              # 웹/Drive 리서치
│       ├── notes.py                 # 노트 CRUD
│       └── sharing.py               # 공유/권한
└── docs/plans/                      # 설계 문서
```

**설계 원칙:**
- `notebooklm-py`는 pip 의존성으로만 사용 (원본 수정 없음)
- 각 도구는 `NotebookLMClient`의 async 메서드를 thin wrapper로 래핑
- 클라이언트는 첫 호출 시 lazy 초기화 (`from_storage()`)
- 모든 도구는 JSON 문자열을 반환하여 MCP 클라이언트가 쉽게 파싱

## License

MIT
