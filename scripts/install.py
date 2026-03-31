"""Windchill MCP Server Installer for Claude Desktop.

Run this script after extracting the zip:
    python scripts/install.py

It will:
1. Install the SDK and dependencies
2. Ask for your Windchill credentials
3. Configure Claude Desktop to use the Windchill MCP server
4. Create a local .env file (not shared)
"""

import json
import os
import subprocess
import sys
from getpass import getpass
from pathlib import Path


def get_claude_desktop_config_path() -> Path:
    """Get the Claude Desktop config file path."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def load_config(config_path: Path) -> dict:
    """Load existing Claude Desktop config or return empty."""
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {}


def save_config(config_path: Path, config: dict) -> None:
    """Save Claude Desktop config."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main():
    print("=" * 60)
    print("  Windchill MCP Server - Installer for Claude Desktop")
    print("=" * 60)
    print()

    # Step 1: Determine project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    run_mcp = project_root / "run_mcp.py"

    print(f"Project directory: {project_root}")
    print()

    # Step 2: Install dependencies
    print("[1/4] Installing SDK and dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", f"{project_root}[mcp]"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("  OK - SDK installed")
    except subprocess.CalledProcessError as e:
        print(f"  FAILED: {e.stderr[:200]}")
        print("  Try running manually: pip install -e .[mcp]")
        return 1

    # Step 3: Ask for credentials
    print()
    print("[2/4] Windchill credentials")
    print("  These are stored locally and never shared.")
    print()

    default_url = "https://plm.contiweb.com/Windchill/servlet/odata"
    base_url = input(f"  Windchill URL [{default_url}]: ").strip()
    if not base_url:
        base_url = default_url

    username = input("  Username: ").strip()
    if not username:
        print("  ERROR: Username is required")
        return 1

    password = getpass("  Password: ")
    if not password:
        print("  ERROR: Password is required")
        return 1

    # Step 4: Create run_mcp.py launcher
    print()
    print("[3/4] Creating MCP launcher...")

    launcher_content = f'''"""Launcher script for the Windchill MCP Server."""
import sys
sys.path.insert(0, r"{project_root / 'src'}")
from windchill_mcp.server import main
main()
'''
    run_mcp.write_text(launcher_content, encoding="utf-8")
    print(f"  OK - {run_mcp}")

    # Also create .env for CLI usage
    env_file = project_root / ".env"
    env_content = f"""# Windchill credentials (local only, not committed to git)
WINDCHILL_BASE_URL={base_url}
WINDCHILL_USERNAME={username}
WINDCHILL_PASSWORD={password}
WINDCHILL_VERIFY_SSL=false
WINDCHILL_API_VERSION=3
"""
    env_file.write_text(env_content, encoding="utf-8")
    print(f"  OK - {env_file}")

    # Step 5: Configure Claude Desktop
    print()
    print("[4/4] Configuring Claude Desktop...")

    config_path = get_claude_desktop_config_path()
    config = load_config(config_path)

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    python_path = sys.executable.replace("\\", "\\\\")
    run_mcp_path = str(run_mcp).replace("\\", "\\\\")

    config["mcpServers"]["windchill"] = {
        "command": python_path,
        "args": [str(run_mcp)],
        "env": {
            "WINDCHILL_BASE_URL": base_url,
            "WINDCHILL_USERNAME": username,
            "WINDCHILL_PASSWORD": password,
            "WINDCHILL_VERIFY_SSL": "false",
            "WINDCHILL_API_VERSION": "3",
        },
    }

    save_config(config_path, config)
    print(f"  OK - {config_path}")

    # Done
    print()
    print("=" * 60)
    print("  Installation complete!")
    print("=" * 60)
    print()
    print("  Next steps:")
    print("  1. Restart Claude Desktop")
    print("  2. Ask Claude: 'Welke containers zijn er in Windchill?'")
    print()
    print("  Available commands in Claude Desktop:")
    print("  - 'Zoek part WH806239'")
    print("  - 'Toon openstaande change requests'")
    print("  - 'Welke workflow taken staan open?'")
    print("  - 'Download het document van WH806239'")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
