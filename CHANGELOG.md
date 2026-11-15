# Changelog

All notable changes to **sammx** are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

Update with:

```bash
git pull && python3 main.py
```

## [1.0.0] - 2026-11-15

First public release.

### Added

- Interactive `rich` TUI for installing, checking and launching 50 security tools.
- Tool catalogue split across 7 categories: reconnaissance, web scanners, phishing,
  OSINT, password cracking, network/wireless, and exploitation.
- Smart dependency detection via `PATH`, explicit file paths, and cloned directories,
  including `~/.local/bin` and `~/go/bin` so pipx and Go installs are recognised.
- Install backends: `apt-get`, `go install`, `pipx`, `pip`, and `git clone` with optional
  virtualenv, requirements install, and post-install steps.
- Gophish support via its official release tarball (`/opt/gophish`).
- sudo handling that caches credentials, skips `sudo` when already root, and turns
  permission failures into readable messages instead of tracebacks.
- Per-tool panel: launch, install, or reinstall without leaving the menu; the suite
  returns to the menu when the launched tool exits.
- Custom install by comma-separated tool numbers (`1,4,12`).
- Paged browser for all 50 tools.
- Headless CLI: `--check`, `--install`, `--install-category`, `--install-all`,
  `--force`, `--stop-on-error`.
- Install-state cache in `~/.cache/kali-suite/installed.json` (1 hour TTL).
- Automatic update check against GitHub releases (6 hour cache, silent fallback to
  `git ls-remote` when the repo is private).
- Bundled changelog viewer (`l` in the TUI, `--changelog` on the CLI).
- About panel with version, author, repository link, and install paths.

### Notes

- Targets Kali Linux / Debian-based systems with `apt`; other distributions are
  not supported.
- `rich` is installed automatically via `python3-rich` when missing.
