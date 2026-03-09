"""Sharing and permissions tools."""

import json
from mcp.server.fastmcp import FastMCP
from notebooklm_mcp.auth import get_client


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def sharing_get_status(notebook_id: str) -> str:
        """Get the sharing status of a notebook.

        Args:
            notebook_id: The notebook ID
        """
        client = await get_client()
        status = await client.sharing.get_status(notebook_id)
        return str(status)

    @mcp.tool()
    async def sharing_set_public(notebook_id: str, public: bool) -> str:
        """Make a notebook public or private.

        Args:
            notebook_id: The notebook ID
            public: True to make public, False for private
        """
        client = await get_client()
        status = await client.sharing.set_public(notebook_id, public)
        return str(status)

    @mcp.tool()
    async def sharing_add_user(
        notebook_id: str,
        email: str,
        permission: str = "viewer",
        notify: bool = True,
        welcome_message: str | None = None,
    ) -> str:
        """Share a notebook with a user.

        Args:
            notebook_id: The notebook ID
            email: User's email address
            permission: Permission level: viewer, editor (default: viewer)
            notify: Send email notification (default: True)
            welcome_message: Optional message to include in notification
        """
        from notebooklm import SharePermission

        perm_map = {
            "viewer": SharePermission.VIEWER,
            "editor": SharePermission.EDITOR,
        }
        client = await get_client()
        status = await client.sharing.add_user(
            notebook_id,
            email,
            perm_map.get(permission, SharePermission.VIEWER),
            notify=notify,
            welcome_message=welcome_message,
        )
        return str(status)

    @mcp.tool()
    async def sharing_remove_user(notebook_id: str, email: str) -> str:
        """Remove a user's access to a notebook.

        Args:
            notebook_id: The notebook ID
            email: User's email to remove
        """
        client = await get_client()
        status = await client.sharing.remove_user(notebook_id, email)
        return str(status)
