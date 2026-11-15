"""
Static configuration for the Kali TUI tool suite.

Every tool entry is a plain dict so it can be serialised to JSON and edited by
hand.  Placeholders ``{tools_dir}`` and ``{tool_dir}`` are expanded by
``installer.py`` (``{tool_dir}`` points at the tool's own cloned directory).
"""

from __future__ import annotations

from pathlib import Path

TOOLS_DIR = Path.home() / "tools"
GO_BIN = Path.home() / "go" / "bin"

CATEGORIES = {
    1: "Reconnaissance & Information Gathering",
    2: "Web Vulnerability Scanners & Fuzzers",
    3: "Phishing & Social Engineering",
    4: "OSINT (Open Source Intelligence)",
    5: "Password Cracking & Bruteforce",
    6: "Network & Wireless Attacks",
    7: "Exploitation & Post-Exploitation",
}

APT = {"kind": "apt"}
GIT = {"check": "git", "apt": ["git"]}
GO = {"check": "go", "apt": ["golang", "golang-go"]}
PIPX = {"check": "pipx", "apt": ["pipx"]}


TOOLS: list[dict] = [
    # ---------------------------------------------------------------- category 1
    {
        "id": 1,
        "name": "Nmap",
        "category": 1,
        "description": "Network discovery, port scanning, service and OS fingerprinting.",
        "check": {"kind": "which", "value": "nmap"},
        "install": [{"kind": "apt", "packages": ["nmap"]}],
        "run": {"cmd": ["nmap"], "sudo": False},
        "homepage": "https://nmap.org",
    },
    {
        "id": 2,
        "name": "Masscan",
        "category": 1,
        "description": "Extremely fast TCP port scanner for internet-wide sweeps.",
        "check": {"kind": "which", "value": "masscan"},
        "install": [{"kind": "apt", "packages": ["masscan"]}],
        "run": {"cmd": ["masscan"], "sudo": True},
        "homepage": "https://github.com/robertdavidgraham/masscan",
    },
    {
        "id": 3,
        "name": "RustScan",
        "category": 1,
        "description": "Modern port scanner that hands open ports to Nmap.",
        "check": {"kind": "which", "value": "rustscan"},
        "install": [{"kind": "apt", "packages": ["rustscan"]}],
        "run": {"cmd": ["rustscan"], "sudo": False},
        "homepage": "https://github.com/RustScan/RustScan",
    },
    {
        "id": 4,
        "name": "Subfinder",
        "category": 1,
        "description": "Passive subdomain enumeration from dozens of sources.",
        "check": {"kind": "go_bin", "value": "subfinder"},
        "prereqs": [GO],
        "install": [
            {
                "kind": "go",
                "packages": ["github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"],
            }
        ],
        "run": {"cmd": ["subfinder"], "sudo": False},
        "homepage": "https://github.com/projectdiscovery/subfinder",
    },
    {
        "id": 5,
        "name": "Amass",
        "category": 1,
        "description": "In-depth attack surface mapping and asset discovery.",
        "check": {"kind": "which", "value": "amass"},
        "install": [{"kind": "apt", "packages": ["amass"]}],
        "run": {"cmd": ["amass"], "sudo": False},
        "homepage": "https://github.com/owasp-amass/amass",
    },
    {
        "id": 6,
        "name": "Assetfinder",
        "category": 1,
        "description": "Find domains and subdomains related to a given domain.",
        "check": {"kind": "go_bin", "value": "assetfinder"},
        "prereqs": [GO],
        "install": [
            {"kind": "go", "packages": ["github.com/tomnomnom/assetfinder@latest"]}
        ],
        "run": {"cmd": ["assetfinder"], "sudo": False},
        "homepage": "https://github.com/tomnomnom/assetfinder",
    },
    {
        "id": 7,
        "name": "Httpx",
        "category": 1,
        "description": "Fast multi-purpose HTTP probing toolkit.",
        "check": {"kind": "which", "value": "httpx"},
        "install": [{"kind": "apt", "packages": ["httpx-toolkit"]}],
        "run": {"cmd": ["httpx"], "sudo": False},
        "homepage": "https://github.com/projectdiscovery/httpx",
    },
    {
        "id": 8,
        "name": "Naabu",
        "category": 1,
        "description": "Fast port scanner focused on reliable SYN/CONNECT sweeps.",
        "check": {"kind": "which", "value": "naabu"},
        "install": [{"kind": "apt", "packages": ["naabu"]}],
        "run": {"cmd": ["naabu"], "sudo": False},
        "homepage": "https://github.com/projectdiscovery/naabu",
    },
    {
        "id": 9,
        "name": "Recon-ng",
        "category": 1,
        "description": "Full-featured web reconnaissance framework with modules.",
        "check": {"kind": "which", "value": "recon-ng"},
        "install": [{"kind": "apt", "packages": ["recon-ng"]}],
        "run": {"cmd": ["recon-ng"], "sudo": False},
        "homepage": "https://github.com/lanmaster53/recon-ng",
    },
    {
        "id": 10,
        "name": "TheHarvester",
        "category": 1,
        "description": "Gather emails, hosts, subdomains and names from public sources.",
        "check": {"kind": "which", "value": "theharvester"},
        "install": [{"kind": "apt", "packages": ["theharvester"]}],
        "run": {"cmd": ["theharvester"], "sudo": False},
        "homepage": "https://github.com/laramies/theHarvester",
    },
    # ---------------------------------------------------------------- category 2
    {
        "id": 11,
        "name": "Nuclei",
        "category": 2,
        "description": "Template-driven vulnerability scanner.",
        "check": {"kind": "which", "value": "nuclei"},
        "install": [{"kind": "apt", "packages": ["nuclei"]}],
        "run": {"cmd": ["nuclei"], "sudo": False},
        "homepage": "https://github.com/projectdiscovery/nuclei",
    },
    {
        "id": 12,
        "name": "Nikto",
        "category": 2,
        "description": "Classic web server scanner for dangerous files and misconfigs.",
        "check": {"kind": "which", "value": "nikto"},
        "install": [{"kind": "apt", "packages": ["nikto"]}],
        "run": {"cmd": ["nikto"], "sudo": False},
        "homepage": "https://github.com/sullo/nikto",
    },
    {
        "id": 13,
        "name": "Wapiti",
        "category": 2,
        "description": "Black-box web application vulnerability scanner.",
        "check": {"kind": "which", "value": "wapiti"},
        "install": [{"kind": "apt", "packages": ["wapiti"]}],
        "run": {"cmd": ["wapiti"], "sudo": False},
        "homepage": "https://github.com/wapiti-scanner/wapiti",
    },
    {
        "id": 14,
        "name": "SQLmap",
        "category": 2,
        "description": "Automatic SQL injection detection and exploitation.",
        "check": {"kind": "which", "value": "sqlmap"},
        "install": [{"kind": "apt", "packages": ["sqlmap"]}],
        "run": {"cmd": ["sqlmap"], "sudo": False},
        "homepage": "https://sqlmap.org",
    },
    {
        "id": 15,
        "name": "Ffuf",
        "category": 2,
        "description": "Fast web fuzzer for directories, parameters and vhosts.",
        "check": {"kind": "which", "value": "ffuf"},
        "install": [{"kind": "apt", "packages": ["ffuf"]}],
        "run": {"cmd": ["ffuf"], "sudo": False},
        "homepage": "https://github.com/ffuf/ffuf",
    },
    {
        "id": 16,
        "name": "Gobuster",
        "category": 2,
        "description": "Directory, DNS and vhost brute forcing.",
        "check": {"kind": "which", "value": "gobuster"},
        "install": [{"kind": "apt", "packages": ["gobuster"]}],
        "run": {"cmd": ["gobuster"], "sudo": False},
        "homepage": "https://github.com/OJ/gobuster",
    },
    {
        "id": 17,
        "name": "Dirsearch",
        "category": 2,
        "description": "Web path brute forcer with a large bundled wordlist.",
        "check": {"kind": "which", "value": "dirsearch"},
        "install": [{"kind": "apt", "packages": ["dirsearch"]}],
        "run": {"cmd": ["dirsearch"], "sudo": False},
        "homepage": "https://github.com/maurosoria/dirsearch",
    },
    {
        "id": 18,
        "name": "Feroxbuster",
        "category": 2,
        "description": "Recursive content discovery written in Rust.",
        "check": {"kind": "which", "value": "feroxbuster"},
        "install": [{"kind": "apt", "packages": ["feroxbuster"]}],
        "run": {"cmd": ["feroxbuster"], "sudo": False},
        "homepage": "https://github.com/epi052/feroxbuster",
    },
    {
        "id": 19,
        "name": "Dalfox",
        "category": 2,
        "description": "Parameter analysis and XSS scanning tool.",
        "check": {"kind": "go_bin", "value": "dalfox"},
        "prereqs": [GO],
        "install": [
            {"kind": "go", "packages": ["github.com/hahwul/dalfox/v2@latest"]}
        ],
        "run": {"cmd": ["dalfox"], "sudo": False},
        "homepage": "https://github.com/hahwul/dalfox",
    },
    {
        "id": 20,
        "name": "XSStrike",
        "category": 2,
        "description": "Advanced XSS detection and payload generation suite.",
        "check": {"kind": "dir", "value": "XSStrike"},
        "prereqs": [GIT],
        "install": [
            {
                "kind": "git",
                "url": "https://github.com/s0md3v/XSStrike.git",
                "dest": "XSStrike",
                "venv": "requirements.txt",
            }
        ],
        "run": {"cmd": ["{tool_dir}/.venv/bin/python", "{tool_dir}/xsstrike.py"], "sudo": False},
        "homepage": "https://github.com/s0md3v/XSStrike",
    },
    {
        "id": 21,
        "name": "WPScan",
        "category": 2,
        "description": "WordPress vulnerability scanner with CVE database.",
        "check": {"kind": "which", "value": "wpscan"},
        "install": [{"kind": "apt", "packages": ["wpscan"]}],
        "run": {"cmd": ["wpscan"], "sudo": False},
        "homepage": "https://github.com/wpscanteam/wpscan",
    },
    {
        "id": 22,
        "name": "WhatWeb",
        "category": 2,
        "description": "Web technology fingerprinting and version detection.",
        "check": {"kind": "which", "value": "whatweb"},
        "install": [{"kind": "apt", "packages": ["whatweb"]}],
        "run": {"cmd": ["whatweb"], "sudo": False},
        "homepage": "https://github.com/urbanadventurer/WhatWeb",
    },
    # ---------------------------------------------------------------- category 3
    {
        "id": 23,
        "name": "Zphisher",
        "category": 3,
        "description": "Automated phishing page generator with 30+ templates.",
        "check": {"kind": "dir", "value": "zphisher"},
        "prereqs": [GIT],
        "install": [
            {
                "kind": "git",
                "url": "https://github.com/htr-tech/zphisher.git",
                "dest": "zphisher",
                "post": [["chmod", "+x", "zphisher.sh"]],
            }
        ],
        "run": {"cmd": ["bash", "{tool_dir}/zphisher.sh"], "sudo": False},
        "homepage": "https://github.com/htr-tech/zphisher",
    },
    {
        "id": 24,
        "name": "Gophish",
        "category": 3,
        "description": "Open-source phishing campaign and training framework.",
        "check": {"kind": "path", "value": "/opt/gophish/gophish"},
        "prereqs": [
            {"check": "curl", "apt": ["curl"]},
            {"check": "unzip", "apt": ["unzip"]},
        ],
        "install": [
            {
                "kind": "shell",
                "cmd": [
                    "bash",
                    "-c",
                    "set -e; V=$(curl -fsSL https://api.github.com/repos/gophish/gophish/releases/latest"
                    " | sed -n 's/.*\"tag_name\": \"v\\([^\"]*\\)\".*/\\1/p' | head -n1);"
                    " curl -fsSL -o /tmp/gophish.zip"
                    " \"https://github.com/gophish/gophish/releases/latest/download/gophish-v${V}-linux-64bit.zip\";"
                    " sudo mkdir -p /opt/gophish;"
                    " sudo unzip -o /tmp/gophish.zip -d /opt/gophish;"
                    " sudo chmod +x /opt/gophish/gophish",
                ],
            }
        ],
        "run": {"cmd": ["/opt/gophish/gophish"], "sudo": True},
        "homepage": "https://github.com/gophish/gophish",
    },
    {
        "id": 25,
        "name": "Social Engineer Toolkit (SET)",
        "category": 3,
        "description": "Menu-driven social engineering attack framework.",
        "check": {"kind": "which", "value": "setoolkit"},
        "install": [{"kind": "apt", "packages": ["set"]}],
        "run": {"cmd": ["setoolkit"], "sudo": True},
        "homepage": "https://github.com/trustedsec/social-engineer-toolkit",
    },
    {
        "id": 26,
        "name": "Blackeye",
        "category": 3,
        "description": "Phishing tool with 38 ready-made site templates.",
        "check": {"kind": "dir", "value": "blackeye"},
        "prereqs": [GIT],
        "install": [
            {
                "kind": "git",
                "url": "https://github.com/An0nUD4Y/blackeye.git",
                "dest": "blackeye",
                "post": [
                    ["chmod", "+x", "blackeye.sh"],
                    ["sudo", "apt-get", "install", "-y", "php", "curl", "unzip"],
                ],
            }
        ],
        "run": {"cmd": ["bash", "{tool_dir}/blackeye.sh"], "sudo": True},
        "homepage": "https://github.com/An0nUD4Y/blackeye",
    },
    # ---------------------------------------------------------------- category 4
    {
        "id": 27,
        "name": "Sherlock",
        "category": 4,
        "description": "Hunt down social media accounts by username.",
        "check": {"kind": "which", "value": "sherlock"},
        "prereqs": [PIPX],
        "install": [{"kind": "pipx", "packages": ["sherlock-project"]}],
        "run": {"cmd": ["sherlock", "--help"], "sudo": False},
        "homepage": "https://github.com/sherlock-project/sherlock",
    },
    {
        "id": 28,
        "name": "Photon",
        "category": 4,
        "description": "Fast OSINT web crawler that extracts emails, keys and URLs.",
        "check": {"kind": "dir", "value": "Photon"},
        "prereqs": [GIT],
        "install": [
            {
                "kind": "git",
                "url": "https://github.com/s0md3v/Photon.git",
                "dest": "Photon",
                "venv": "requirements.txt",
            }
        ],
        "run": {"cmd": ["{tool_dir}/.venv/bin/python", "{tool_dir}/photon.py"], "sudo": False},
        "homepage": "https://github.com/s0md3v/Photon",
    },
    {
        "id": 29,
        "name": "Holehe",
        "category": 4,
        "description": "Check whether an email is registered on 120+ sites.",
        "check": {"kind": "which", "value": "holehe"},
        "prereqs": [PIPX],
        "install": [{"kind": "pipx", "packages": ["holehe"]}],
        "run": {"cmd": ["holehe", "--help"], "sudo": False},
        "homepage": "https://github.com/megadose/holehe",
    },
    {
        "id": 30,
        "name": "SpiderFoot",
        "category": 4,
        "description": "Automated OSINT reconnaissance with 200+ modules and web UI.",
        "check": {"kind": "dir", "value": "spiderfoot"},
        "prereqs": [GIT],
        "install": [
            {
                "kind": "git",
                "url": "https://github.com/smicallef/spiderfoot.git",
                "dest": "spiderfoot",
                "venv": "requirements.txt",
            }
        ],
        "run": {
            "cmd": ["{tool_dir}/.venv/bin/python", "{tool_dir}/sf.py", "-l", "127.0.0.1:5001"],
            "sudo": False,
        },
        "homepage": "https://github.com/smicallef/spiderfoot",
    },
    {
        "id": 31,
        "name": "Shodan CLI",
        "category": 4,
        "description": "Command-line client for the Shodan internet device search engine.",
        "check": {"kind": "which", "value": "shodan"},
        "prereqs": [PIPX],
        "install": [{"kind": "pipx", "packages": ["shodan"]}],
        "run": {"cmd": ["shodan", "--help"], "sudo": False},
        "homepage": "https://cli.shodan.io",
    },
    # ---------------------------------------------------------------- category 5
    {
        "id": 32,
        "name": "Hashcat",
        "category": 5,
        "description": "GPU-accelerated password recovery and hash cracking.",
        "check": {"kind": "which", "value": "hashcat"},
        "install": [{"kind": "apt", "packages": ["hashcat"]}],
        "run": {"cmd": ["hashcat", "--help"], "sudo": False},
        "homepage": "https://hashcat.net/hashcat",
    },
    {
        "id": 33,
        "name": "John the Ripper",
        "category": 5,
        "description": "Versatile CPU/GPU password cracker with many hash formats.",
        "check": {"kind": "which", "value": "john"},
        "install": [{"kind": "apt", "packages": ["john"]}],
        "run": {"cmd": ["john"], "sudo": False},
        "homepage": "https://www.openwall.com/john",
    },
    {
        "id": 34,
        "name": "Hydra",
        "category": 5,
        "description": "Fast network login brute forcer for 50+ protocols.",
        "check": {"kind": "which", "value": "hydra"},
        "install": [{"kind": "apt", "packages": ["hydra"]}],
        "run": {"cmd": ["hydra"], "sudo": False},
        "homepage": "https://github.com/vanhauser-thc/thc-hydra",
    },
    {
        "id": 35,
        "name": "Medusa",
        "category": 5,
        "description": "Parallel, modular network authentication brute forcer.",
        "check": {"kind": "which", "value": "medusa"},
        "install": [{"kind": "apt", "packages": ["medusa"]}],
        "run": {"cmd": ["medusa"], "sudo": False},
        "homepage": "https://github.com/jmk-foofus/medusa",
    },
    {
        "id": 36,
        "name": "Crowbar",
        "category": 5,
        "description": "Brute force tool for RDP, SSH keys, VNC and OpenVPN.",
        "check": {"kind": "which", "value": "crowbar"},
        "install": [{"kind": "apt", "packages": ["crowbar"]}],
        "run": {"cmd": ["crowbar", "--help"], "sudo": False},
        "homepage": "https://github.com/galkan/crowbar",
    },
    {
        "id": 37,
        "name": "CUPP",
        "category": 5,
        "description": "Common User Passwords Profiler for targeted wordlists.",
        "check": {"kind": "which", "value": "cupp"},
        "install": [{"kind": "apt", "packages": ["cupp"]}],
        "run": {"cmd": ["cupp"], "sudo": False},
        "homepage": "https://github.com/Mebus/cupp",
    },
    # ---------------------------------------------------------------- category 6
    {
        "id": 38,
        "name": "Aircrack-ng",
        "category": 6,
        "description": "Wi-Fi auditing suite for capture, injection and cracking.",
        "check": {"kind": "which", "value": "aircrack-ng"},
        "install": [{"kind": "apt", "packages": ["aircrack-ng"]}],
        "run": {"cmd": ["aircrack-ng"], "sudo": False},
        "homepage": "https://www.aircrack-ng.org",
    },
    {
        "id": 39,
        "name": "Wifite",
        "category": 6,
        "description": "Automated wireless attack tool wrapping aircrack and friends.",
        "check": {"kind": "which", "value": "wifite"},
        "install": [{"kind": "apt", "packages": ["wifite"]}],
        "run": {"cmd": ["wifite", "--help"], "sudo": True},
        "homepage": "https://github.com/derv82/wifite2",
    },
    {
        "id": 40,
        "name": "Bettercap",
        "category": 6,
        "description": "Swiss-army knife for MITM, sniffing and network recon.",
        "check": {"kind": "which", "value": "bettercap"},
        "install": [{"kind": "apt", "packages": ["bettercap"]}],
        "run": {"cmd": ["bettercap"], "sudo": True},
        "homepage": "https://www.bettercap.org",
    },
    {
        "id": 41,
        "name": "Responder",
        "category": 6,
        "description": "LLMNR/NBT-NS/mDNS poisoner and credential harvester.",
        "check": {"kind": "which", "value": "responder"},
        "install": [{"kind": "apt", "packages": ["responder"]}],
        "run": {"cmd": ["responder", "-h"], "sudo": True},
        "homepage": "https://github.com/lgandx/Responder",
    },
    {
        "id": 42,
        "name": "Evilginx2",
        "category": 6,
        "description": "MITM phishing framework that bypasses 2FA by proxying sessions.",
        "check": {"kind": "go_bin", "value": "evilginx2"},
        "prereqs": [GO],
        "install": [
            {"kind": "go", "packages": ["github.com/kgretzky/evilginx2@latest"]}
        ],
        "run": {"cmd": ["evilginx2"], "sudo": True},
        "homepage": "https://github.com/kgretzky/evilginx2",
    },
    {
        "id": 43,
        "name": "Macchanger",
        "category": 6,
        "description": "View and change MAC addresses of network interfaces.",
        "check": {"kind": "which", "value": "macchanger"},
        "install": [{"kind": "apt", "packages": ["macchanger"]}],
        "run": {"cmd": ["macchanger"], "sudo": False},
        "homepage": "https://github.com/alobbs/macchanger",
    },
    {
        "id": 44,
        "name": "TShark",
        "category": 6,
        "description": "Command-line network protocol analyser (Wireshark engine).",
        "check": {"kind": "which", "value": "tshark"},
        "install": [{"kind": "apt", "packages": ["tshark"]}],
        "run": {"cmd": ["tshark", "-h"], "sudo": False},
        "homepage": "https://www.wireshark.org",
    },
    # ---------------------------------------------------------------- category 7
    {
        "id": 45,
        "name": "Metasploit Framework",
        "category": 7,
        "description": "Exploit development and delivery framework with msfconsole.",
        "check": {"kind": "which", "value": "msfconsole"},
        "install": [{"kind": "apt", "packages": ["metasploit-framework"]}],
        "run": {"cmd": ["msfconsole"], "sudo": False},
        "homepage": "https://www.metasploit.com",
    },
    {
        "id": 46,
        "name": "Searchsploit",
        "category": 7,
        "description": "Offline search of the Exploit-DB archive.",
        "check": {"kind": "which", "value": "searchsploit"},
        "install": [{"kind": "apt", "packages": ["exploitdb"]}],
        "run": {"cmd": ["searchsploit"], "sudo": False},
        "homepage": "https://www.exploit-db.com/searchsploit",
    },
    {
        "id": 47,
        "name": "Commix",
        "category": 7,
        "description": "Automated OS command injection exploitation.",
        "check": {"kind": "which", "value": "commix"},
        "install": [{"kind": "apt", "packages": ["commix"]}],
        "run": {"cmd": ["commix"], "sudo": False},
        "homepage": "https://github.com/commixproject/commix",
    },
    {
        "id": 48,
        "name": "Netcat",
        "category": 7,
        "description": "TCP/IP swiss-army knife for shells, relays and port checks.",
        "check": {"kind": "which", "value": "nc"},
        "install": [{"kind": "apt", "packages": ["netcat-traditional"]}],
        "run": {"cmd": ["nc", "-h"], "sudo": False},
        "homepage": "http://nc110.sourceforge.net",
    },
    {
        "id": 49,
        "name": "Chisel",
        "category": 7,
        "description": "Fast TCP/UDP tunnel over HTTP with SSH transport.",
        "check": {"kind": "go_bin", "value": "chisel"},
        "prereqs": [GO],
        "install": [
            {"kind": "go", "packages": ["github.com/jpillora/chisel@latest"]}
        ],
        "run": {"cmd": ["chisel", "--help"], "sudo": False},
        "homepage": "https://github.com/jpillora/chisel",
    },
    {
        "id": 50,
        "name": "BeEF",
        "category": 7,
        "description": "Browser Exploitation Framework for hooked web browsers.",
        "check": {"kind": "which", "value": "beef-xss"},
        "install": [{"kind": "apt", "packages": ["beef-xss"]}],
        "run": {"cmd": ["beef-xss"], "sudo": True},
        "homepage": "https://beefproject.com",
    },
]


def get_tool(tool_id: int) -> dict | None:
    for tool in TOOLS:
        if tool["id"] == tool_id:
            return tool
    return None


def tools_by_category(category_id: int) -> list[dict]:
    return [tool for tool in TOOLS if tool["category"] == category_id]


def all_tool_ids() -> list[int]:
    return [tool["id"] for tool in TOOLS]


def tool_dir(tool: dict) -> Path:
    step = next((s for s in tool["install"] if s["kind"] == "git"), None)
    return TOOLS_DIR / (step["dest"] if step else tool["name"].lower().replace(" ", "-"))


def validate() -> list[str]:
    problems: list[str] = []
    ids = all_tool_ids()

    if len(TOOLS) != 50:
        problems.append(f"expected 50 tools, found {len(TOOLS)}")
    if len(set(ids)) != len(ids):
        problems.append("duplicate tool ids detected")
    if ids != list(range(1, len(TOOLS) + 1)):
        problems.append("tool ids are not sequential from 1")

    for tool in TOOLS:
        if tool["category"] not in CATEGORIES:
            problems.append(f"{tool['name']}: unknown category {tool['category']}")
        if not tool.get("install"):
            problems.append(f"{tool['name']}: no install steps")
        if not tool.get("run", {}).get("cmd"):
            problems.append(f"{tool['name']}: no run command")

    return problems


if __name__ == "__main__":
    issues = validate()
    print(f"{len(TOOLS)} tools across {len(CATEGORIES)} categories")
    for cid, cname in CATEGORIES.items():
        print(f"  [{cid}] {cname}: {len(tools_by_category(cid))} tools")
    print("validation: OK" if not issues else "validation failed:\n  " + "\n  ".join(issues))
