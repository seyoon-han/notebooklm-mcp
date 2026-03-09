"""Artifact generation and download tools."""

import json
from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.auth import get_client


def _status_to_json(status) -> str:
    return json.dumps({
        "task_id": getattr(status, "task_id", None),
        "status": str(status),
    })


def register(mcp: FastMCP) -> None:
    # ── List artifacts ──────────────────────────────────────────────

    @mcp.tool()
    async def artifact_list(notebook_id: str) -> str:
        """List all artifacts in a notebook.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        artifacts = await client.artifacts.list(notebook_id)
        return json.dumps(
            [{"id": a.id, "title": getattr(a, "title", None), "type": getattr(a, "type", None)} for a in artifacts],
            indent=2,
        )

    @mcp.tool()
    async def artifact_delete(notebook_id: str, artifact_id: str) -> str:
        """Delete an artifact.

        Args:
            notebook_id: The notebook ID
            artifact_id: The artifact ID to delete
        """
        client = await get_client()
        result = await client.artifacts.delete(notebook_id, artifact_id)
        return json.dumps({"deleted": result})

    # ── Wait / Poll ─────────────────────────────────────────────────

    @mcp.tool()
    async def artifact_wait(notebook_id: str, task_id: str, timeout: int = 300) -> str:
        """Wait for an artifact generation task to complete.

        Args:
            notebook_id: The notebook ID
            task_id: The task ID returned by a generate_* tool
            timeout: Max seconds to wait (default 300)
        """
        client = await get_client()
        status = await client.artifacts.wait_for_completion(
            notebook_id, task_id, timeout=timeout
        )
        return _status_to_json(status)

    @mcp.tool()
    async def artifact_poll_status(notebook_id: str, task_id: str) -> str:
        """Check the current status of an artifact generation task without waiting.

        Args:
            notebook_id: The notebook ID
            task_id: The task ID returned by a generate_* tool
        """
        client = await get_client()
        status = await client.artifacts.poll_status(notebook_id, task_id)
        return _status_to_json(status)

    # ── Generate ────────────────────────────────────────────────────

    @mcp.tool()
    async def generate_audio(
        notebook_id: str,
        instructions: str | None = None,
        source_ids: list[str] | None = None,
        audio_format: str = "deep_dive",
        audio_length: str = "default",
        language: str = "en",
    ) -> str:
        """Generate an audio overview (podcast-style) from notebook sources.

        Args:
            notebook_id: The notebook ID
            instructions: Optional instructions for the audio generation
            source_ids: Optional list of source IDs to use
            audio_format: Format: deep_dive, briefing, conversation, lecture (default: deep_dive)
            audio_length: Length: short, default, long (default: default)
            language: Language code (default: en)
        """
        from notebooklm import AudioFormat, AudioLength

        fmt_map = {
            "deep_dive": AudioFormat.DEEP_DIVE,
            "briefing": AudioFormat.BRIEFING,
            "conversation": AudioFormat.CONVERSATION,
            "lecture": AudioFormat.LECTURE,
        }
        len_map = {
            "short": AudioLength.SHORT,
            "default": AudioLength.DEFAULT,
            "long": AudioLength.LONG,
        }
        client = await get_client()
        status = await client.artifacts.generate_audio(
            notebook_id,
            source_ids=source_ids,
            instructions=instructions,
            audio_format=fmt_map.get(audio_format, AudioFormat.DEEP_DIVE),
            audio_length=len_map.get(audio_length, AudioLength.DEFAULT),
            language=language,
        )
        return _status_to_json(status)

    @mcp.tool()
    async def generate_video(
        notebook_id: str,
        instructions: str | None = None,
        source_ids: list[str] | None = None,
        video_format: str = "explainer",
        video_style: str = "auto_select",
        language: str = "en",
    ) -> str:
        """Generate a video overview from notebook sources.

        Args:
            notebook_id: The notebook ID
            instructions: Optional instructions
            source_ids: Optional source IDs to use
            video_format: Format: explainer, tutorial (default: explainer)
            video_style: Style: auto_select, whiteboard, kawaii, anime, etc. (default: auto_select)
            language: Language code (default: en)
        """
        from notebooklm import VideoFormat, VideoStyle

        fmt_map = {
            "explainer": VideoFormat.EXPLAINER,
            "tutorial": VideoFormat.TUTORIAL,
        }
        style_map = {
            "auto_select": VideoStyle.AUTO_SELECT,
            "whiteboard": VideoStyle.WHITEBOARD,
            "kawaii": VideoStyle.KAWAII,
            "anime": VideoStyle.ANIME,
        }
        client = await get_client()
        status = await client.artifacts.generate_video(
            notebook_id,
            source_ids=source_ids,
            instructions=instructions,
            video_format=fmt_map.get(video_format, VideoFormat.EXPLAINER),
            video_style=style_map.get(video_style, VideoStyle.AUTO_SELECT),
            language=language,
        )
        return _status_to_json(status)

    @mcp.tool()
    async def generate_quiz(
        notebook_id: str,
        instructions: str | None = None,
        source_ids: list[str] | None = None,
        quantity: str = "standard",
        difficulty: str = "medium",
        language: str = "en",
    ) -> str:
        """Generate a quiz from notebook sources.

        Args:
            notebook_id: The notebook ID
            instructions: Optional instructions
            source_ids: Optional source IDs to use
            quantity: Number of questions: few, standard, many (default: standard)
            difficulty: Difficulty: easy, medium, hard (default: medium)
            language: Language code (default: en)
        """
        from notebooklm import QuizQuantity, QuizDifficulty

        qty_map = {
            "few": QuizQuantity.FEW,
            "standard": QuizQuantity.STANDARD,
            "many": QuizQuantity.MANY,
        }
        diff_map = {
            "easy": QuizDifficulty.EASY,
            "medium": QuizDifficulty.MEDIUM,
            "hard": QuizDifficulty.HARD,
        }
        client = await get_client()
        status = await client.artifacts.generate_quiz(
            notebook_id,
            source_ids=source_ids,
            instructions=instructions,
            quantity=qty_map.get(quantity, QuizQuantity.STANDARD),
            difficulty=diff_map.get(difficulty, QuizDifficulty.MEDIUM),
            language=language,
        )
        return _status_to_json(status)

    @mcp.tool()
    async def generate_flashcards(
        notebook_id: str,
        instructions: str | None = None,
        source_ids: list[str] | None = None,
        quantity: str = "standard",
        language: str = "en",
    ) -> str:
        """Generate flashcards from notebook sources.

        Args:
            notebook_id: The notebook ID
            instructions: Optional instructions
            source_ids: Optional source IDs to use
            quantity: Number of cards: few, standard, many (default: standard)
            language: Language code (default: en)
        """
        from notebooklm import QuizQuantity

        qty_map = {
            "few": QuizQuantity.FEW,
            "standard": QuizQuantity.STANDARD,
            "many": QuizQuantity.MANY,
        }
        client = await get_client()
        status = await client.artifacts.generate_flashcards(
            notebook_id,
            source_ids=source_ids,
            instructions=instructions,
            quantity=qty_map.get(quantity, QuizQuantity.STANDARD),
            language=language,
        )
        return _status_to_json(status)

    @mcp.tool()
    async def generate_slide_deck(
        notebook_id: str,
        source_ids: list[str] | None = None,
        format: str = "detailed_deck",
        length: str = "default",
        language: str = "en",
    ) -> str:
        """Generate a slide deck from notebook sources.

        Args:
            notebook_id: The notebook ID
            source_ids: Optional source IDs to use
            format: Format: detailed_deck, presenter_deck (default: detailed_deck)
            length: Length: short, default, long (default: default)
            language: Language code (default: en)
        """
        from notebooklm import SlideDeckFormat, SlideDeckLength

        fmt_map = {
            "detailed_deck": SlideDeckFormat.DETAILED_DECK,
            "presenter_deck": SlideDeckFormat.PRESENTER_DECK,
        }
        len_map = {
            "short": SlideDeckLength.SHORT,
            "default": SlideDeckLength.DEFAULT,
            "long": SlideDeckLength.LONG,
        }
        client = await get_client()
        status = await client.artifacts.generate_slide_deck(
            notebook_id,
            source_ids=source_ids,
            format=fmt_map.get(format, SlideDeckFormat.DETAILED_DECK),
            length=len_map.get(length, SlideDeckLength.DEFAULT),
            language=language,
        )
        return _status_to_json(status)

    @mcp.tool()
    async def generate_infographic(
        notebook_id: str,
        source_ids: list[str] | None = None,
        orientation: str = "landscape",
        detail: str = "standard",
        language: str = "en",
    ) -> str:
        """Generate an infographic from notebook sources.

        Args:
            notebook_id: The notebook ID
            source_ids: Optional source IDs to use
            orientation: Orientation: landscape, portrait, square (default: landscape)
            detail: Detail level: minimal, standard, detailed (default: standard)
            language: Language code (default: en)
        """
        from notebooklm import InfographicOrientation, InfographicDetail

        orient_map = {
            "landscape": InfographicOrientation.LANDSCAPE,
            "portrait": InfographicOrientation.PORTRAIT,
            "square": InfographicOrientation.SQUARE,
        }
        detail_map = {
            "minimal": InfographicDetail.MINIMAL,
            "standard": InfographicDetail.STANDARD,
            "detailed": InfographicDetail.DETAILED,
        }
        client = await get_client()
        status = await client.artifacts.generate_infographic(
            notebook_id,
            source_ids=source_ids,
            orientation=orient_map.get(orientation, InfographicOrientation.LANDSCAPE),
            detail=detail_map.get(detail, InfographicDetail.STANDARD),
            language=language,
        )
        return _status_to_json(status)

    @mcp.tool()
    async def generate_mind_map(
        notebook_id: str,
        instructions: str | None = None,
        source_ids: list[str] | None = None,
        language: str = "en",
    ) -> str:
        """Generate a mind map from notebook sources. Returns hierarchical JSON.

        Args:
            notebook_id: The notebook ID
            instructions: Optional instructions
            source_ids: Optional source IDs to use
            language: Language code (default: en)
        """
        client = await get_client()
        result = await client.artifacts.generate_mind_map(
            notebook_id,
            source_ids=source_ids,
            instructions=instructions,
            language=language,
        )
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def generate_report(
        notebook_id: str,
        title: str | None = None,
        description: str | None = None,
        source_ids: list[str] | None = None,
        format: str = "study_guide",
        language: str = "en",
    ) -> str:
        """Generate a report from notebook sources.

        Args:
            notebook_id: The notebook ID
            title: Optional report title
            description: Optional report description
            source_ids: Optional source IDs to use
            format: Format: study_guide, briefing_doc, faq, timeline (default: study_guide)
            language: Language code (default: en)
        """
        from notebooklm import ReportFormat

        fmt_map = {
            "study_guide": ReportFormat.STUDY_GUIDE,
            "briefing_doc": ReportFormat.BRIEFING_DOC,
            "faq": ReportFormat.FAQ,
            "timeline": ReportFormat.TIMELINE,
        }
        client = await get_client()
        status = await client.artifacts.generate_report(
            notebook_id,
            source_ids=source_ids,
            title=title,
            description=description,
            format=fmt_map.get(format, ReportFormat.STUDY_GUIDE),
            language=language,
        )
        return _status_to_json(status)

    @mcp.tool()
    async def generate_data_table(
        notebook_id: str,
        instructions: str | None = None,
        source_ids: list[str] | None = None,
        language: str = "en",
    ) -> str:
        """Generate a data table from notebook sources.

        Args:
            notebook_id: The notebook ID
            instructions: Natural language instructions for table contents
            source_ids: Optional source IDs to use
            language: Language code (default: en)
        """
        client = await get_client()
        status = await client.artifacts.generate_data_table(
            notebook_id,
            source_ids=source_ids,
            instructions=instructions,
            language=language,
        )
        return _status_to_json(status)

    # ── Download ────────────────────────────────────────────────────

    @mcp.tool()
    async def download_audio(
        notebook_id: str, output_path: str, artifact_id: str | None = None
    ) -> str:
        """Download generated audio to a file.

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the audio file (MP3/MP4)
            artifact_id: Optional specific artifact ID (uses latest if omitted)
        """
        client = await get_client()
        path = await client.artifacts.download_audio(
            notebook_id, output_path, artifact_id=artifact_id
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_video(
        notebook_id: str, output_path: str, artifact_id: str | None = None
    ) -> str:
        """Download generated video to a file.

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the video file (MP4)
            artifact_id: Optional specific artifact ID
        """
        client = await get_client()
        path = await client.artifacts.download_video(
            notebook_id, output_path, artifact_id=artifact_id
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_quiz(
        notebook_id: str,
        output_path: str,
        artifact_id: str | None = None,
        output_format: str = "json",
    ) -> str:
        """Download generated quiz.

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the quiz
            artifact_id: Optional specific artifact ID
            output_format: Format: json, markdown, html (default: json)
        """
        client = await get_client()
        path = await client.artifacts.download_quiz(
            notebook_id, output_path, artifact_id=artifact_id, output_format=output_format
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_flashcards(
        notebook_id: str,
        output_path: str,
        artifact_id: str | None = None,
        output_format: str = "json",
    ) -> str:
        """Download generated flashcards.

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the flashcards
            artifact_id: Optional specific artifact ID
            output_format: Format: json, markdown, html (default: json)
        """
        client = await get_client()
        path = await client.artifacts.download_flashcards(
            notebook_id, output_path, artifact_id=artifact_id, output_format=output_format
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_slide_deck(
        notebook_id: str, output_path: str, artifact_id: str | None = None
    ) -> str:
        """Download generated slide deck (PDF or PPTX).

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the slide deck
            artifact_id: Optional specific artifact ID
        """
        client = await get_client()
        path = await client.artifacts.download_slide_deck(
            notebook_id, output_path, artifact_id=artifact_id
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_infographic(
        notebook_id: str, output_path: str, artifact_id: str | None = None
    ) -> str:
        """Download generated infographic (PNG).

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the infographic
            artifact_id: Optional specific artifact ID
        """
        client = await get_client()
        path = await client.artifacts.download_infographic(
            notebook_id, output_path, artifact_id=artifact_id
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_report(
        notebook_id: str, output_path: str, artifact_id: str | None = None
    ) -> str:
        """Download generated report (Markdown).

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the report
            artifact_id: Optional specific artifact ID
        """
        client = await get_client()
        path = await client.artifacts.download_report(
            notebook_id, output_path, artifact_id=artifact_id
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_mind_map(
        notebook_id: str, output_path: str, artifact_id: str | None = None
    ) -> str:
        """Download mind map data.

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the mind map
            artifact_id: Optional specific artifact ID
        """
        client = await get_client()
        path = await client.artifacts.download_mind_map(
            notebook_id, output_path, artifact_id=artifact_id
        )
        return json.dumps({"saved_to": path})

    @mcp.tool()
    async def download_data_table(
        notebook_id: str, output_path: str, artifact_id: str | None = None
    ) -> str:
        """Download generated data table (CSV).

        Args:
            notebook_id: The notebook ID
            output_path: Path to save the data table
            artifact_id: Optional specific artifact ID
        """
        client = await get_client()
        path = await client.artifacts.download_data_table(
            notebook_id, output_path, artifact_id=artifact_id
        )
        return json.dumps({"saved_to": path})
