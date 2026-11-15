"""Rich-powered terminal interface for the Kali tool suite."""

from __future__ import annotations

import sys

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

import config
import installer

console = Console()
PAGE_SIZE = 15
state: dict[int, bool] = {}


def _ask(prompt: str) -> str:
    try:
        return Prompt.ask(prompt).strip()
    except EOFError:
        raise SystemExit(0)


def _pause() -> None:
    try:
        console.input("\n[dim]Press Enter to return to the menu...[/]")
    except EOFError:
        raise SystemExit(0)


def _status(installed: bool) -> Text:
    if installed:
        return Text("installed", style="bold green")
    return Text("missing", style="bold red")


def banner() -> None:
    console.clear()
    art = Text()
    art.append(" KALI ", style="bold white on red")
    art.append(" TOOL SUITE ", style="bold white on black")
    art.append("\n", style="")
    art.append("50 security tools - install, launch, repeat", style="dim")
    console.print(Panel(art, box=box.HEAVY, border_style="red", padding=(0, 2)))
    total = len(config.TOOLS)
    ready = sum(1 for value in state.values() if value)
    console.print(
        f"[bold green]{ready}[/]/[bold]{total}[/] tools installed   "
        f"[dim]tools dir:[/] [cyan]{config.TOOLS_DIR}[/]\n"
    )


def category_table() -> Table:
    table = Table(box=box.SIMPLE, header_style="bold magenta", expand=True)
    table.add_column("#", justify="right", width=3)
    table.add_column("Category", style="bold white")
    table.add_column("Ready", justify="right", width=7)
    table.add_column("Total", justify="right", width=7)

    for cid, name in config.CATEGORIES.items():
        tools = config.tools_by_category(cid)
        ready = sum(1 for tool in tools if state.get(tool["id"]))
        table.add_row(
            str(cid),
            name,
            f"[green]{ready}[/]" if ready else "[dim]0[/]",
            str(len(tools)),
        )
    return table


def tool_table(tools: list[dict]) -> Table:
    table = Table(box=box.SIMPLE_HEAVY, header_style="bold cyan", expand=True)
    table.add_column("#", justify="right", width=3)
    table.add_column("Tool", style="bold white", no_wrap=True)
    table.add_column("Status", width=10)
    table.add_column("Description", overflow="fold", style="dim")
    for tool in tools:
        table.add_row(
            str(tool["id"]),
            tool["name"],
            _status(state.get(tool["id"], False)),
            tool["description"],
        )
    return table


def actions_table() -> Table:
    table = Table(box=box.SIMPLE, show_header=False, expand=False)
    table.add_column(style="bold cyan", width=4)
    table.add_column()
    for key, label in (
        ("b", "Browse all tools (paged)"),
        ("i", "Install all missing tools"),
        ("c", "Install a whole category"),
        ("x", "Custom install (comma separated numbers)"),
        ("r", "Refresh install status"),
        ("0", "Exit"),
    ):
        table.add_row(key, label)
    return table


def show_tool(tool: dict) -> None:
    site = tool.get("homepage", "")
    body = Text()
    body.append(f"{tool['description']}\n\n", style="white")
    body.append("Category  ", style="dim")
    body.append(f"{config.CATEGORIES[tool['category']]}\n", style="cyan")
    body.append("Location  ", style="dim")
    body.append(f"{installer.tool_location(tool) or 'not detected'}\n", style="cyan")
    body.append("Command   ", style="dim")
    body.append(" ".join(installer.run_command(tool)) + "\n", style="cyan")
    if site:
        body.append("Homepage  ", style="dim")
        body.append(site, style="blue underline")

    panel = Panel(
        body,
        title=f"[bold]{tool['name']}[/]  {_status(state.get(tool['id'], False))}",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)
    console.print(
        "[bold cyan]1[/] Launch   [bold cyan]2[/] Install / reinstall   [bold cyan]0[/] Back\n"
    )


def tool_actions(tool: dict) -> None:
    while True:
        console.clear()
        banner()
        show_tool(tool)
        choice = _ask("Selection")

        if choice == "0":
            return
        if choice == "1":
            if not state.get(tool["id"]):
                console.print("[red]Not installed yet - install it first.[/]")
                _pause()
                continue
            installer.launch_tool(tool)
            console.print(
                f"\n[green]Returned from {tool['name']}.[/] "
                "[dim]Any output above belongs to the tool.[/]"
            )
            _pause()
        elif choice == "2":
            force = state.get(tool["id"], False)
            if force and not Confirm.ask(
                f"{tool['name']} is already installed. Reinstall anyway?", default=False
            ):
                continue
            installer.install_tool(tool, force=force)
            state[tool["id"]] = installer.is_installed(tool)
            _pause()
            return
        else:
            console.print("[yellow]Pick 0, 1 or 2.[/]")


def browse_category(cid: int) -> None:
    tools = config.tools_by_category(cid)
    while True:
        console.clear()
        banner()
        console.print(Panel(category_table(), title="Categories", border_style="magenta"))
        console.print(Panel(tool_table(tools), title=config.CATEGORIES[cid], border_style="cyan"))
        choice = _ask(f"Tool number 1-{tools[-1]['id']} or [bold]0[/] to go back")

        if choice == "0":
            return
        if not choice.isdigit():
            console.print("[yellow]Enter a number.[/]")
            continue
        tool = next((t for t in tools if t["id"] == int(choice)), None)
        if tool is None:
            console.print("[yellow]That tool is not in this category.[/]")
            _pause()
            continue
        tool_actions(tool)


def browse_all() -> None:
    tools = config.TOOLS
    pages = (len(tools) + PAGE_SIZE - 1) // PAGE_SIZE
    page = 0

    while True:
        chunk = tools[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]
        console.clear()
        banner()
        console.print(
            Panel(
                tool_table(chunk),
                title=f"All tools - page {page + 1}/{pages}",
                border_style="cyan",
            )
        )
        console.print(
            f"[bold cyan]n[/] next  [bold cyan]p[/] prev  [bold cyan]0[/] back  "
            f"[dim]or a tool number ({chunk[0]['id']}-{chunk[-1]['id']} on this page)[/]"
        )
        choice = _ask("Selection").lower()

        if choice == "0":
            return
        if choice == "n":
            page = min(page + 1, pages - 1)
            continue
        if choice == "p":
            page = max(page - 1, 0)
            continue
        if choice.isdigit():
            tool = next((t for t in chunk if t["id"] == int(choice)), None)
            if tool:
                tool_actions(tool)
            else:
                console.print("[yellow]Not on this page.[/]")
                _pause()
            continue
        console.print("[yellow]Use n, p, 0 or a number.[/]")


def do_install(tools: list[dict]) -> None:
    if not tools:
        console.print("[yellow]Nothing to install.[/]")
        _pause()
        return

    missing = [tool for tool in tools if not state.get(tool["id"])]
    already = len(tools) - len(missing)
    if not missing:
        console.print("[green]Everything selected is already installed.[/]")
        _pause()
        return

    console.print(f"\n[bold]{len(missing)}[/] tool(s) to install")
    if already:
        console.print(f"[dim]{already} already present and will be skipped[/]")
    if not Confirm.ask("Continue? sudo will be requested when needed", default=True):
        return

    results = []
    for index, tool in enumerate(missing, start=1):
        console.rule(f"[bold cyan]\\[{index}/{len(missing)}][/] {tool['name']}")
        results.append(installer.install_tool(tool))
        console.print(str(results[-1]))

    installed, skipped, failed = installer.summary(results)
    state.update(installer.check_all(refresh=True))

    console.rule("Summary")
    console.print(
        f"[green]installed {installed}[/]   [dim]skipped {skipped}[/]   "
        f"[red]failed {failed}[/]"
    )
    for result in results:
        if not result.ok:
            console.print(f"  [red]{result.name}[/] [dim]{result.message}[/]")
    _pause()


def install_all_flow() -> None:
    do_install(config.TOOLS)


def install_category_flow() -> None:
    console.clear()
    banner()
    console.print(Panel(category_table(), title="Install by category", border_style="magenta"))
    choice = _ask("Category number or [bold]0[/] to go back")
    if choice == "0":
        return
    if not choice.isdigit() or int(choice) not in config.CATEGORIES:
        console.print("[yellow]Unknown category.[/]")
        _pause()
        return
    do_install(config.tools_by_category(int(choice)))


def custom_install_flow() -> None:
    console.clear()
    banner()
    console.print(Panel(tool_table(config.TOOLS), title="Custom install", border_style="cyan"))
    raw = _ask("Tool numbers separated by commas (e.g. [bold]1,4,12[/]) or [bold]0[/] to go back")
    if raw == "0":
        return
    try:
        tools = installer.parse_ids(raw)
    except ValueError as exc:
        console.print(f"[red]{exc}[/]")
        _pause()
        return
    do_install(tools)


def refresh_status() -> None:
    with console.status("[cyan]Scanning installed tools..."):
        state.update(installer.check_all(refresh=True))
    console.print("[green]Status refreshed.[/]")


def main() -> None:
    global state

    for problem in installer.preflight():
        console.print(f"[yellow]warning:[/] {problem}")

    with console.status("[cyan]Detecting installed tools..."):
        state = installer.check_all(refresh=True)

    while True:
        banner()
        console.print(Panel(category_table(), title="Categories", border_style="magenta"))
        console.print(Panel(actions_table(), title="Actions", border_style="cyan"))
        choice = _ask("Selection").lower()

        if choice == "0":
            console.print("[dim]Goodbye.[/]")
            return
        if choice == "b":
            browse_all()
        elif choice == "i":
            install_all_flow()
        elif choice == "c":
            install_category_flow()
        elif choice == "x":
            custom_install_flow()
        elif choice == "r":
            refresh_status()
        elif choice.isdigit() and int(choice) in config.CATEGORIES:
            browse_category(int(choice))
        else:
            console.print("[yellow]Numbers open a category; letters pick an action.[/]")
            _pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted.[/]")
        sys.exit(130)
