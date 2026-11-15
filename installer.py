"""Dependency detection, installation and process launching."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import config

LOCAL_BIN = Path.home() / ".local" / "bin"
CACHE_DIR = Path.home() / ".cache" / "kali-suite"
CACHE_FILE = CACHE_DIR / "installed.json"
CACHE_TTL = 3600
TAIL_LINES = 20


@dataclass
class Result:
    tool_id: int
    name: str
    ok: bool
    skipped: bool = False
    message: str = ""

    def __str__(self) -> str:
        status = "ok" if self.ok else "FAIL"
        if self.skipped:
            status = "skip"
        return f"[{status}] {self.name}: {self.message}"


class InstallError(RuntimeError):
    pass


_session_sudo = False
_apt_updated = False


def _is_root() -> bool:
    return hasattr(os, "geteuid") and os.geteuid() == 0


def _which(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for directory in (LOCAL_BIN, config.GO_BIN):
        candidate = directory / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def _expand(text: str, tool: dict) -> str:
    return text.replace("{tools_dir}", str(config.TOOLS_DIR)).replace(
        "{tool_dir}", str(config.tool_dir(tool))
    )


def _exec(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd) if cwd else None,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            bufsize=1,
        )
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except PermissionError as exc:
        return 126, str(exc)

    tail: list[str] = []
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        tail.append(line.rstrip())
        if len(tail) > TAIL_LINES:
            tail.pop(0)
    return proc.wait(), "\n".join(tail)


def _sudo(cmd: list[str]) -> list[str]:
    if _is_root() or cmd[0] == "sudo":
        return cmd
    return ["sudo"] + cmd


def ensure_sudo() -> bool:
    global _session_sudo
    if _is_root():
        return True
    if shutil.which("sudo") is None:
        return False
    if _session_sudo:
        return True
    if subprocess.run(["sudo", "-n", "true"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        _session_sudo = True
        return True
    print("sudo password required:")
    if subprocess.call(["sudo", "-v"]) != 0:
        return False
    _session_sudo = True
    return True


def _explain(rc: int, output: str) -> str:
    text = output.lower()
    if "a password is required" in text or "must be run as root" in text or "permission denied" in text:
        return f"permission denied (exit {rc}) - unlock sudo with 'sudo -v' and retry"
    if "unable to locate package" in text:
        return f"package not found in configured apt sources (exit {rc})"
    if "could not resolve" in text or "temporary failure resolving" in text:
        return f"network/DNS failure (exit {rc})"
    if "externally-managed-environment" in text:
        return f"PEP 668 blocked the pip install (exit {rc}) - use pipx or a venv"
    if rc == 127:
        return f"missing command (exit {rc}): {output.strip().splitlines()[-1] if output.strip() else 'unknown'}"
    return f"exit {rc}: {output.strip().splitlines()[-1] if output.strip() else 'no output'}"


def is_installed(tool: dict) -> bool:
    check = tool["check"]
    kind = check["kind"]
    value = check["value"]

    if kind == "which":
        return _which(value) is not None
    if kind == "go_bin":
        return _which(value) is not None
    if kind == "path":
        return Path(value).exists()
    if kind == "dir":
        return (config.TOOLS_DIR / value).is_dir()
    raise InstallError(f"unknown check kind '{kind}'")


def run_command(tool: dict) -> list[str]:
    return [_expand(part, tool) for part in tool["run"]["cmd"]]


def tool_location(tool: dict) -> str | None:
    check = tool["check"]
    kind, value = check["kind"], check["value"]
    if kind in {"which", "go_bin"}:
        return _which(value)
    if kind == "path":
        return value if Path(value).exists() else None
    if kind == "dir":
        path = config.TOOLS_DIR / value
        return str(path) if path.is_dir() else None
    return None


def _apt(packages: list[str]) -> None:
    global _apt_updated
    if shutil.which("apt-get") is None:
        raise InstallError("apt-get not found (this installer targets Debian/Kali)")
    if not ensure_sudo():
        raise InstallError("sudo privileges required for apt installs")

    if not _apt_updated:
        print("Refreshing apt package lists...")
        rc, _ = _exec(_sudo(["apt-get", "update", "-qq"]))
        _apt_updated = True
        if rc != 0:
            print("warning: apt-get update failed, continuing with cached lists")

    cmd = _sudo(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y", *packages])
    rc, output = _exec(cmd)
    if rc != 0:
        raise InstallError(_explain(rc, output))


def _tool_env() -> dict:
    env = os.environ.copy()
    extra = [str(config.GO_BIN), str(LOCAL_BIN)]
    path = env.get("PATH", "")
    missing = [entry for entry in extra if entry not in path.split(os.pathsep)]
    if missing:
        env["PATH"] = os.pathsep.join([*missing, path])
    return env


def _go(packages: list[str]) -> None:
    if shutil.which("go") is None:
        raise InstallError("go toolchain not found")
    for package in packages:
        print(f"go install {package}")
        rc, output = _exec(["go", "install", package], env=_tool_env())
        if rc != 0:
            raise InstallError(_explain(rc, output))


def _pipx(packages: list[str]) -> None:
    if shutil.which("pipx") is None:
        raise InstallError("pipx not found")
    rc, output = _exec(["pipx", "install", "--force", *packages], env=_tool_env())
    if rc != 0:
        raise InstallError(_explain(rc, output))


def _pip(packages: list[str]) -> None:
    rc, output = _exec([sys.executable or "python3", "-m", "pip", "install", "--upgrade", *packages])
    if rc != 0:
        raise InstallError(_explain(rc, output))


def _git(step: dict, tool: dict) -> None:
    dest = config.TOOLS_DIR / step["dest"]
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise InstallError(f"cannot create {dest.parent}: {exc}") from exc

    if dest.is_dir() and any(dest.iterdir()):
        print(f"{dest} already exists, reusing")
    else:
        rc, output = _exec(["git", "clone", "--depth", "1", step["url"], str(dest)])
        if rc != 0:
            raise InstallError(_explain(rc, output))

    if step.get("venv"):
        venv = dest / ".venv"
        if not (venv / "bin" / "python").exists():
            rc, output = _exec(["python3", "-m", "venv", str(venv)], cwd=dest)
            if rc != 0:
                print("python3-venv missing, installing it")
                _apt(["python3-venv"])
                rc, output = _exec(["python3", "-m", "venv", str(venv)], cwd=dest)
                if rc != 0:
                    raise InstallError(_explain(rc, output))
        pip = venv / "bin" / "pip"
        rc, output = _exec([str(pip), "install", "-q", "--upgrade", "pip"], cwd=dest)
        if rc != 0:
            raise InstallError(_explain(rc, output))
        rc, output = _exec([str(pip), "install", "-q", "-r", step["venv"]], cwd=dest)
        if rc != 0:
            raise InstallError(_explain(rc, output))

    for post in step.get("post", []):
        rc, output = _exec([_expand(part, tool) for part in post], cwd=dest)
        if rc != 0:
            raise InstallError(_explain(rc, output))


def _shell(step: dict, tool: dict) -> None:
    rc, output = _exec([_expand(part, tool) for part in step["cmd"]])
    if rc != 0:
        raise InstallError(_explain(rc, output))


def _install_prereq(prereq: dict) -> None:
    if _which(prereq["check"]) is not None:
        return
    print(f"Installing prerequisite: {prereq['check']}")
    _apt(prereq["apt"])


def _run_step(step: dict, tool: dict) -> None:
    kind = step["kind"]
    if kind == "apt":
        _apt(step["packages"])
    elif kind == "go":
        _go(step["packages"])
    elif kind == "pipx":
        _pipx(step["packages"])
    elif kind == "pip":
        _pip(step["packages"])
    elif kind == "git":
        _git(step, tool)
    elif kind == "shell":
        _shell(step, tool)
    else:
        raise InstallError(f"unknown install kind '{kind}'")


def install_tool(tool: dict, force: bool = False) -> Result:
    if not force and is_installed(tool):
        return Result(tool["id"], tool["name"], True, skipped=True, message="already installed")

    print(f"\n=== {tool['name']} ({tool['description']}) ===")
    try:
        for prereq in tool.get("prereqs", []):
            _install_prereq(prereq)
        for step in tool["install"]:
            _run_step(step, tool)
    except InstallError as exc:
        return Result(tool["id"], tool["name"], False, message=str(exc))
    except KeyboardInterrupt:
        return Result(tool["id"], tool["name"], False, message="interrupted by user")

    if not is_installed(tool):
        return Result(
            tool["id"],
            tool["name"],
            False,
            message=f"installer finished but check '{tool['check']['value']}' is still missing",
        )
    return Result(tool["id"], tool["name"], True, message="installed")


def install_many(tools: list[dict], force: bool = False, stop_on_error: bool = False) -> list[Result]:
    results: list[Result] = []
    total = len(tools)
    for index, tool in enumerate(tools, start=1):
        print(f"\n[{index}/{total}] {tool['name']}")
        result = install_tool(tool, force=force)
        results.append(result)
        print(result)
        if not result.ok and stop_on_error:
            print("Stopping after first failure")
            break
    return results


def summary(results: list[Result]) -> tuple[int, int, int]:
    installed = sum(1 for r in results if r.ok and not r.skipped)
    skipped = sum(1 for r in results if r.skipped)
    failed = sum(1 for r in results if not r.ok)
    return installed, skipped, failed


def _load_cache() -> dict:
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        if time.time() - data.get("timestamp", 0) > CACHE_TTL:
            return {}
        return data.get("tools", {})
    except (OSError, ValueError):
        return {}


def _save_cache(tools: dict[int, bool]) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {"timestamp": time.time(), "tools": {str(k): v for k, v in tools.items()}}
        CACHE_FILE.write_text(json.dumps(payload), encoding="utf-8")
    except OSError:
        pass


def check_all(refresh: bool = True) -> dict[int, bool]:
    cache = {} if refresh else _load_cache()
    state: dict[int, bool] = {}
    for tool in config.TOOLS:
        cached = cache.get(str(tool["id"]))
        state[tool["id"]] = bool(cached) if cached is not None else is_installed(tool)
    _save_cache(state)
    return state


def launch_tool(tool: dict) -> int:
    run = tool["run"]
    cmd = run_command(tool)

    if run.get("sudo") and not _is_root():
        if not ensure_sudo():
            print("Cannot launch: sudo unavailable.")
            return 1
        cmd = _sudo(cmd)

    workdir = config.tool_dir(tool)
    cwd = workdir if workdir.is_dir() else None

    print(f"\nLaunching {tool['name']} - close it to return to the menu.\n")
    try:
        return subprocess.call(cmd, cwd=str(cwd) if cwd else None, env=_tool_env())
    except FileNotFoundError:
        print(f"{cmd[0]} not found on PATH.")
        return 127
    except KeyboardInterrupt:
        return 130
    except PermissionError as exc:
        print(f"Permission denied: {exc}")
        return 126


def preflight() -> list[str]:
    issues: list[str] = []
    if sys.platform != "linux":
        issues.append("this tool suite targets Linux (Kali); current platform: " + sys.platform)
    if shutil.which("apt-get") is None:
        issues.append("apt-get not found - Debian/Kali base system required")
    if not _is_root() and shutil.which("sudo") is None:
        issues.append("sudo not found and not running as root")
    return issues


def parse_ids(raw: str) -> list[dict]:
    tools: list[dict] = []
    for chunk in raw.replace(" ", "").split(","):
        if not chunk:
            continue
        if not chunk.isdigit():
            raise ValueError(f"'{chunk}' is not a tool number")
        tool = config.get_tool(int(chunk))
        if tool is None:
            raise ValueError(f"no tool with number {chunk}")
        if tool not in tools:
            tools.append(tool)
    return tools


def cli(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Kali suite installer (headless mode)")
    parser.add_argument("--check", action="store_true", help="print installation status")
    parser.add_argument("--install", metavar="IDS", help="comma separated tool ids")
    parser.add_argument("--install-category", type=int, metavar="N", help="install one category")
    parser.add_argument("--install-all", action="store_true", help="install every missing tool")
    parser.add_argument("--force", action="store_true", help="reinstall even if detected")
    parser.add_argument("--stop-on-error", action="store_true")
    args = parser.parse_args(argv)

    problems = preflight()
    for problem in problems:
        print(f"warning: {problem}")
    if any("apt-get not found" in problem for problem in problems):
        return 2

    if args.check:
        state = check_all(refresh=True)
        for tool in config.TOOLS:
            mark = "OK  " if state[tool["id"]] else "MISS"
            print(f"{mark} {tool['id']:>2}. {tool['name']}")
        missing = sum(1 for value in state.values() if not value)
        print(f"\n{len(state) - missing} installed, {missing} missing")

    if args.install:
        try:
            targets = parse_ids(args.install)
        except ValueError as exc:
            print(f"error: {exc}")
            return 2
    elif args.install_category:
        targets = config.tools_by_category(args.install_category)
        if not targets:
            print(f"error: no category {args.install_category}")
            return 2
    elif args.install_all:
        targets = [t for t in config.TOOLS if args.force or not is_installed(t)]
    else:
        targets = []

    if targets:
        results = install_many(targets, force=args.force, stop_on_error=args.stop_on_error)
        installed, skipped, failed = summary(results)
        print(f"\ninstalled={installed} skipped={skipped} failed={failed}")
        for result in results:
            if not result.ok:
                print(result)
        return 1 if failed else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
