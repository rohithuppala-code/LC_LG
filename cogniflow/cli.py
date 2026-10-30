"""Interactive CLI terminal for CogniFlow built with Rich."""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from cogniflow.config.settings import get_settings
from cogniflow.chains.structured_chain import create_research_chain, create_fact_check_chain
from cogniflow.chains.parallel_chain import create_parallel_analysis_chain
from cogniflow.agents.react_agent import create_react_agent
from cogniflow.memory.session import create_conversational_chain

console = Console()


def show_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                     🧠 COGNIFLOW WORKFLOW OS                     ║
    ║        Modular GenAI Engine powered by LangChain & LCEL          ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    console.print(f"[bold cyan]{banner}[/bold cyan]")


def show_status():
    settings = get_settings()
    table = Table(title="🔧 System Configuration Status", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="dim")
    table.add_column("Value")
    table.add_column("Status")

    table.add_row("Default Provider", settings.default_provider, "[green]Active[/green]")
    table.add_row(
        "Google Gemini Key",
        "Set" if settings.google_api_key else "Missing",
        "[green]Ready[/green]" if settings.google_api_key else "[yellow]Configure in .env[/yellow]",
    )
    table.add_row(
        "OpenAI Key",
        "Set" if settings.openai_api_key else "Missing",
        "[green]Ready[/green]" if settings.openai_api_key else "[dim]Optional[/dim]",
    )
    table.add_row(
        "Groq Key",
        "Set" if settings.groq_api_key else "Missing",
        "[green]Ready[/green]" if settings.groq_api_key else "[dim]Optional[/dim]",
    )
    console.print(table)


def run_research():
    topic = Prompt.ask("\n[bold yellow]Enter research topic[/bold yellow]")
    focus = Prompt.ask("[bold yellow]Enter focus areas (comma separated)[/bold yellow]", default="architecture, performance, adoption")
    depth = Prompt.ask("[bold yellow]Target depth[/bold yellow]", default="comprehensive technical")

    with console.status("[bold green]Synthesizing structured research report via LCEL...", spinner="dots"):
        try:
            chain = create_research_chain()
            report = chain.invoke({"topic": topic, "focus_areas": focus, "target_depth": depth})

            console.print(Panel(f"[bold green]Executive Summary[/bold green]\n\n{report.executive_summary}", title=f"📋 {report.topic}"))

            if report.key_insights:
                table = Table(title="💡 Key Insights", show_header=True, header_style="bold cyan")
                table.add_column("Category", style="cyan")
                table.add_column("Insight", style="white")
                table.add_column("Impact", style="yellow")
                table.add_column("Confidence", style="green")
                for item in report.key_insights:
                    table.add_row(item.category, item.summary, item.impact_level.upper(), f"{item.confidence_score * 100:.0f}%")
                console.print(table)

            if report.pros or report.cons:
                p_table = Table(title="⚖️ Trade-offs & Analysis", show_header=True)
                p_table.add_column("Pros / Opportunities", style="green")
                p_table.add_column("Risks / Drawbacks", style="red")
                max_len = max(len(report.pros), len(report.cons))
                for i in range(max_len):
                    pro = report.pros[i] if i < len(report.pros) else ""
                    con = report.cons[i] if i < len(report.cons) else ""
                    p_table.add_row(f"• {pro}" if pro else "", f"• {con}" if con else "")
                console.print(p_table)

            console.print(Panel(f"[bold yellow]Final Verdict:[/bold yellow] {report.verdict}", border_style="yellow"))
        except Exception as exc:
            console.print(f"[bold red]Error running research chain:[/bold red] {str(exc)}")


def run_parallel_analysis():
    topic = Prompt.ask("\n[bold yellow]Enter subject for dual-branch parallel analysis[/bold yellow]")
    with console.status("[bold blue]Executing simultaneous reasoning branches via RunnableParallel...", spinner="dots"):
        try:
            chain = create_parallel_analysis_chain()
            res = chain.invoke(topic)
            console.print(Panel(res["executive_summary"], title="⚡ Branch 1: Executive Brief", border_style="cyan"))
            console.print(Panel(res["pros_and_cons"], title="⚡ Branch 2: Strategic Trade-offs", border_style="magenta"))
        except Exception as exc:
            console.print(f"[bold red]Error running parallel chain:[/bold red] {str(exc)}")


def run_agent():
    query = Prompt.ask("\n[bold yellow]Enter task or question for ReAct Autonomous Agent[/bold yellow]")

    agent = create_react_agent()

    def on_thought(msg):
        console.print(f"[dim blue]{msg}[/dim blue]")

    def on_tool(name, args):
        console.print(f"[bold yellow]🛠️ Invoking Tool:[/bold yellow] [cyan]{name}[/cyan] with args [dim]{args}[/dim]")

    def on_result(name, result):
        snippet = result[:180] + ("..." if len(result) > 180 else "")
        console.print(f"[bold green]↳ Result from {name}:[/bold green] [dim]{snippet}[/dim]")

    with console.status("[bold green]Agent orchestrating reasoning loop...", spinner="line"):
        res = agent.run(query, on_thought=on_thought, on_tool_call=on_tool, on_tool_result=on_result)

    console.print(Panel(Markdown(res["answer"]), title="🎯 Agent Final Answer", border_style="green"))
    console.print(f"[dim]Total reasoning iterations: {res['iterations']}[/dim]")


def run_chat():
    session_id = Prompt.ask("[bold yellow]Enter session ID (e.g. 'dev-session')[/bold yellow]", default="dev-session")
    console.print("[dim cyan]Type 'exit' to return to menu.[/dim cyan]")
    chain = create_conversational_chain()

    while True:
        user_input = Prompt.ask("\n[bold green]You[/bold green]")
        if user_input.strip().lower() in ["exit", "quit", "q"]:
            break
        with console.status("[dim]Thinking...", spinner="dots"):
            response = chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
        console.print(f"[bold blue]AI:[/bold blue] {response}")


def main():
    show_banner()
    show_status()

    while True:
        console.print("\n[bold]Select an action:[/bold]")
        console.print("  [1] 📋 Structured Research Chain (Pydantic + LCEL)")
        console.print("  [2] ⚡ Parallel Dual-Branch Analysis (RunnableParallel)")
        console.print("  [3] 🤖 Autonomous ReAct Agent (Tool Calling + Live Search)")
        console.print("  [4] 💬 Conversational Chat (Memory & Session State)")
        console.print("  [5] 🔧 Show Configuration Status")
        console.print("  [0] 🚪 Exit")

        choice = Prompt.ask("[bold cyan]Option[/bold cyan]", choices=["1", "2", "3", "4", "5", "0"], default="1")

        if choice == "1":
            run_research()
        elif choice == "2":
            run_parallel_analysis()
        elif choice == "3":
            run_agent()
        elif choice == "4":
            run_chat()
        elif choice == "5":
            show_status()
        elif choice == "0":
            console.print("[green]Goodbye![/green]")
            sys.exit(0)


if __name__ == "__main__":
    main()
