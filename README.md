# sammx

**v1.0.0** · created by [S4rtx](https://github.com/S4rtx) · [github.com/S4rtx/sammx](https://github.com/S4rtx/sammx)

A Kali Linux terminal tool suite: an interactive `rich` TUI plus a headless CLI that
detects, installs, and launches **50 curated security tools** across 7 categories.

Release notes live in [CHANGELOG.md](CHANGELOG.md); the suite checks for new versions
every time it starts.

Built as a single-command replacement for "clone repo, apt install, go install, remember
where the binary landed". Every action checks what is already present before touching the
system, and returns to the menu when the launched tool exits.

## Features

- **50 tools, 7 categories** - recon, web, phishing, OSINT, password, network/wireless, exploitation.
- **Smart detection** - `shutil.which()` plus explicit path and clone-directory checks, with
  `~/.local/bin` and `~/go/bin` included so pipx/go installs are recognised immediately.
- **Five install backends** - `apt-get`, `go install`, `pipx`, `pip`, and `git` (with optional
  venv, requirements, and post-install steps). Gophish is fetched as a release tarball.
- **Safe by default** - skips what is installed, asks before bulk installs, handles sudo
  prompts, and reports a readable reason instead of crashing when a tool fails.
- **Per-tool actions** - launch now, or reinstall on demand.
- **Headless mode** - `--check`, `--install 1,4,12`, `--install-category N`, `--install-all`.
- **Update notifications** - checks GitHub for a newer release on startup and shows
  `update vX.Y.Z available` with the exact command to run.
- **Bundled changelog** - press `l` in the TUI (or use `--changelog`) to read release notes.
- **Status cache** - `~/.cache/kali-suite/installed.json` (1 hour TTL, refreshable from the menu).

## Requirements

| Requirement | Notes |
| --- | --- |
| Kali Linux (or Debian-based) | apt is required; other distros are not supported |
| Python 3.9+ | preinstalled on Kali |
| `sudo` | needed for apt installs and for launching privileged tools |
| `rich` | auto-installed via `python3-rich` (apt) or `pip --user` on first run |
| Internet access | required for every install step |

## Installation

```bash
git clone https://github.com/S4rtx/sammx.git
cd sammx
python3 main.py
```

Optional system-wide command:

```bash
chmod +x main.py
sudo ln -s "$PWD/main.py" /usr/local/bin/sammx
sammx
```

If `rich` is missing, `main.py` installs `python3-rich` through apt and re-executes itself.
You can also preinstall it:

```bash
sudo apt install python3-rich
```

## Usage

### Interactive menu

```
python3 main.py
```

| Key | Action |
| --- | --- |
| `1`-`7` | Open a category and pick a tool by its number |
| `b` | Browse all 50 tools (paged, `n`/`p` to flip pages) |
| `i` | Install every missing tool |
| `c` | Install one whole category |
| `x` | Custom install - comma separated numbers, e.g. `1,4,12` |
| `r` | Refresh installation status |
| `u` | Check for updates now |
| `l` | View the changelog |
| `a` | About: version, author, repository |
| `0` | Exit |

Inside a tool panel:

| Key | Action |
| --- | --- |
| `1` | Launch the tool (returns to the menu when it exits) |
| `2` | Install or reinstall |
| `0` | Back |

Tools that need arguments print their usage when launched bare; close them and you are back
in the suite. `Ctrl-C` inside a launched tool returns to the menu instead of killing the suite.

### Headless CLI

```bash
python3 main.py --check                      # status for all 50 tools
python3 main.py --install 1,4,12             # specific tools
python3 main.py --install-category 2         # one category
python3 main.py --install-all                # everything missing
python3 main.py --install-all --stop-on-error
python3 main.py --install 11 --force         # reinstall even if detected
python3 main.py --update-check               # is a newer release out?
python3 main.py --changelog                  # print release notes
python3 main.py --version                    # suite version, author, repo
```

Exit codes: `0` success, `1` one or more installs failed or the update check failed,
`2` unsupported environment or bad input.

### Staying up to date

Every start checks GitHub for a newer release and caches the answer for 6 hours, so the
suite stays usable offline. When a newer tag exists the banner shows
`update vX.Y.Z available` and a panel lists the command to run:

```bash
git pull && python3 main.py
```

Manual checks: press `u` in the menu or run `python3 main.py --update-check`. `l` opens the
bundled changelog, including the release notes of the pending update when available.

Because this repository is private, the GitHub API only answers when a token is present.
Set `GITHUB_TOKEN` (or `GH_TOKEN`) to enable it; otherwise the check falls back to
`git ls-remote origin` using your existing git credentials, and skips silently when neither
is available.

## Tools

### 1. Reconnaissance & Information Gathering (10)
Nmap, Masscan, RustScan, Subfinder, Amass, Assetfinder, Httpx, Naabu, Recon-ng, TheHarvester

### 2. Web Vulnerability Scanners & Fuzzers (12)
Nuclei, Nikto, Wapiti, SQLmap, Ffuf, Gobuster, Dirsearch, Feroxbuster, Dalfox, XSStrike, WPScan, WhatWeb

### 3. Phishing & Social Engineering (4)
Zphisher, Gophish, Social Engineer Toolkit (SET), Blackeye

### 4. OSINT (Open Source Intelligence) (5)
Sherlock, Photon, Holehe, SpiderFoot, Shodan CLI

### 5. Password Cracking & Bruteforce (6)
Hashcat, John the Ripper, Hydra, Medusa, Crowbar, CUPP

### 6. Network & Wireless Attacks (7)
Aircrack-ng, Wifite, Bettercap, Responder, Evilginx2, Macchanger, TShark

### 7. Exploitation & Post-Exploitation (6)
Metasploit Framework, Searchsploit, Commix, Netcat, Chisel, BeEF

## Where things land

| Source | Destination |
| --- | --- |
| `apt-get` | system paths (`/usr/bin`, `/usr/share`) |
| `go install` | `~/go/bin` |
| `pipx` | `~/.local/bin` |
| `git clone` | `~/tools/<name>` (Python tools get `~/tools/<name>/.venv`) |
| Gophish | `/opt/gophish` |
| Detection cache | `~/.cache/kali-suite/installed.json` |

No files are written outside those paths.

## Project layout

| File | Responsibility |
| --- | --- |
| `config.py` | The 50 tool definitions: category, description, check, install steps, run command. Declarative, JSON-like, no logic. |
| `installer.py` | Detection, prereqs, install backends, sudo handling, launch wrapper, status cache, headless CLI. |
| `menu.py` | Rich UI: banner, category/tool tables, pagination, prompts, install flows, update panel, changelog viewer. |
| `updater.py` | Version comparison, GitHub release lookup, update cache, changelog access. |
| `main.py` | Entry point: Python version gate, `rich` bootstrap, menu or headless dispatch. |
| `CHANGELOG.md` | Release history, kept in sync with `config.VERSION`. |

## Adding a tool

Append an entry to `TOOLS` in `config.py` (ids stay sequential), then run
`python3 config.py` to validate.

```python
{
    "id": 51,
    "name": "Example",
    "category": 1,
    "description": "What it does.",
    "check": {"kind": "which", "value": "example"},
    "install": [{"kind": "apt", "packages": ["example"]}],
    "run": {"cmd": ["example"], "sudo": False},
    "homepage": "https://example.org",
}
```

Check kinds: `which`, `go_bin`, `path`, `dir`.
Install kinds: `apt` (`packages`), `go` (`packages`), `pipx` (`packages`), `pip` (`packages`),
`git` (`url`, `dest`, optional `venv`, optional `post`), `shell` (`cmd`).
Placeholders `{tools_dir}` and `{tool_dir}` are expanded before execution, and
`prereqs` installs a missing dependency (e.g. Go or pipx) before the tool itself.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Tool installed but shows `missing` | Press `r` to refresh; confirm `~/go/bin` and `~/.local/bin` are on your `PATH`, or start a new shell |
| `permission denied` during install | Run `sudo -v` first, then retry |
| `unable to locate package` | The package is not in your configured apt sources - run `sudo apt update` and check the Kali mirror |
| `externally-managed-environment` | Only relevant to custom `pip` installs; bundled Python tools use venvs. Use a venv manually |
| A tool opens usage text and exits | That tool needs arguments (e.g. `masscan`, `hydra`); run it directly with your flags |
| `update check failed` | Offline, or the private repo needs credentials - export `GITHUB_TOKEN`, then press `u` |

## Disclaimer

These are third-party open-source tools installed from their official packages and
repositories; nothing is bundled here. Use them only on systems you own or are explicitly
authorized to test. The author accepts no liability for misuse or damage.
