"""Version metadata, update checking and changelog access."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import config

CACHE_DIR = Path.home() / ".cache" / "kali-suite"
CACHE_FILE = CACHE_DIR / "update.json"
CACHE_TTL = 6 * 3600
RETRY_AFTER = 900
TIMEOUT = 5
CHANGELOG_FILE = Path(__file__).resolve().parent / "CHANGELOG.md"
TAG_PATTERN = re.compile(r"^v?\d+(\.\d+)*$")


@dataclass
class Update:
    latest: str
    url: str = ""
    notes: str = ""


def normalize(version: str) -> tuple[int, ...]:
    core = version.strip().lstrip("vV").split("-")[0].split("+")[0]
    parts: list[int] = []
    for chunk in core.split("."):
        match = re.match(r"\d+", chunk)
        parts.append(int(match.group()) if match else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def is_newer(remote: str, local: str = config.VERSION) -> bool:
    return normalize(remote) > normalize(local)


def display_version(version: str) -> str:
    return version.strip().lstrip("vV")


def _read_cache() -> dict:
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _write_cache(payload: dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(payload), encoding="utf-8")
    except OSError:
        pass


def _fetch_api() -> Update | None:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{config.APP_NAME}/{config.VERSION}",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        f"https://api.github.com/repos/{config.REPO}/releases/latest", headers=headers
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = json.load(response)
    except (urllib.error.URLError, ValueError, OSError, TimeoutError):
        return None

    tag = str(data.get("tag_name", "")).strip()
    if not tag:
        return None
    return Update(tag, data.get("html_url", ""), data.get("body", "") or "")


def _fetch_git() -> Update | None:
    repo_dir = Path(__file__).resolve().parent
    if shutil.which("git") is None or not (repo_dir / ".git").exists():
        return None

    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", "origin"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 3,
            env=env,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    tags = []
    for line in result.stdout.splitlines():
        _, _, ref = line.partition("\t")
        if ref.startswith("refs/tags/"):
            name = ref[len("refs/tags/") :]
            if TAG_PATTERN.match(name):
                tags.append(name)
    if not tags:
        return None

    latest = max(tags, key=normalize)
    return Update(latest, f"{config.GITHUB_URL}/releases/tag/{latest}")


def check_for_update(force: bool = False) -> Update | None:
    cache = _read_cache()
    now = time.time()

    if not force:
        if cache.get("failed_at") and now - cache["failed_at"] < RETRY_AFTER:
            return None
        if cache.get("checked_at") and now - cache["checked_at"] < CACHE_TTL and cache.get("latest"):
            return Update(cache["latest"], cache.get("url", ""), cache.get("notes", ""))

    remote = _fetch_api() or _fetch_git()
    if remote is None:
        cache["failed_at"] = now
        _write_cache(cache)
        return None

    _write_cache(
        {
            "checked_at": now,
            "latest": remote.latest,
            "url": remote.url,
            "notes": remote.notes,
        }
    )
    return remote


def has_update(force: bool = False) -> Update | None:
    remote = check_for_update(force=force)
    if remote is not None and is_newer(remote.latest):
        return remote
    return None


def changelog_text() -> str:
    try:
        return CHANGELOG_FILE.read_text(encoding="utf-8")
    except OSError:
        return (
            "# Changelog\n\n"
            f"## {config.VERSION}\n\n"
            "- Changelog file not found.\n"
        )


def update_command() -> str:
    return "git pull && python3 main.py"
