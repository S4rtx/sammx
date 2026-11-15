#!/usr/bin/env python3
"""Entry point for the Kali tool suite TUI."""

from __future__ import annotations

import os
import subprocess
import sys

MIN_PYTHON = (3, 9)


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_python() -> None:
    if sys.version_info < MIN_PYTHON:
        _fail(f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required, found {sys.version.split()[0]}")
    if not sys.platform.startswith("linux"):
        print(f"warning: built for Linux/Kali, running on {sys.platform}", file=sys.stderr)


def ensure_rich() -> None:
    try:
        import rich  # noqa: F401
        return
    except ImportError:
        pass

    print("'rich' is missing, attempting to install it...")
    apt_cmd = [
        "env",
        "DEBIAN_FRONTEND=noninteractive",
        "apt-get",
        "install",
        "-y",
        "python3-rich",
    ]
    if not (hasattr(os, "geteuid") and os.geteuid() == 0):
        apt_cmd = ["sudo", *apt_cmd]

    rc = subprocess.call(apt_cmd) if sys.platform.startswith("linux") else 1
    if rc != 0:
        print("apt install failed, trying pip --user")
        rc = subprocess.call([sys.executable, "-m", "pip", "install", "--user", "rich"])
    if rc != 0:
        _fail("could not install 'rich'; run: sudo apt install python3-rich")

    os.execv(sys.executable, [sys.executable, *sys.argv])


def main(argv: list[str]) -> int:
    ensure_python()

    import config
    import updater

    if argv and argv[0] in {"--version", "-V"}:
        print(f"{config.APP_NAME} v{config.VERSION} by {config.AUTHOR}")
        print(config.GITHUB_URL)
        return 0

    if argv and argv[0] == "--changelog":
        print(updater.changelog_text())
        return 0

    ensure_rich()

    import installer
    import menu

    if argv and argv[0] == "--update-check":
        remote = updater.check_for_update(force=True)
        if remote is None:
            print("update check failed (offline, or no access to the private repository)")
            return 1
        if updater.is_newer(remote.latest):
            print(
                f"update available: v{updater.display_version(remote.latest)} "
                f"(running v{config.VERSION})"
            )
            if remote.url:
                print(remote.url)
        else:
            print(f"up to date (v{config.VERSION})")
        return 0

    if argv:
        return installer.cli(argv)

    try:
        menu.main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
    except BrokenPipeError:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
