import asyncio
import sys

from rich.console import Console
from rich.markdown import Markdown

from src.my_agent.core.confing import get_settings
from src.my_agent.services.agent.agent_module import AgentModule


async def main():
    settings = get_settings()
    console = Console()
    agent = AgentModule(settings)

    try:
        while True:
            console.print("> ", end="")
            raw_bytes = await asyncio.to_thread(sys.stdin.buffer.readline)
            query = raw_bytes.decode(sys.stdout.encoding or 'utf-8', errors='ignore').strip()

            if not query:
                continue

            if query == "/exit":
                console.print("\n[bold red]Exiting...[/bold red]")
                break

            response = await agent.get_answer(query)
            console.print(Markdown(response))
            console.print()

    except (KeyboardInterrupt, asyncio.CancelledError):
        console.print("\n[bold red]Exiting...[/bold red]")
    except Exception as ex:
        console.print(f"[red]Ошибка: {ex}[/red]")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")