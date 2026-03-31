"""Uninstall Windchill MCP Server from Claude Desktop.

Removes the windchill MCP server from Claude Desktop config.
Does not remove the SDK or files.
"""

import json
import os
import sys
from pathlib import Path


def get_claude_desktop_config_path() -> Path:
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def main():
    config_path = get_claude_desktop_config_path()

    if not config_path.exists():
        print("Claude Desktop config not found. Nothing to remove.")
        return 0

    config = json.loads(config_path.read_text(encoding="utf-8"))
    servers = config.get("mcpServers", {})

    if "windchill" not in servers:
        print("Windchill MCP server not found in Claude Desktop config.")
        return 0

    del servers["windchill"]
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Windchill MCP server removed from Claude Desktop.")
    print("Restart Claude Desktop to apply changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
