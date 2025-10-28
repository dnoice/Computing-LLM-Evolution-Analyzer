"""Interactive CLI for Computing & LLM Evolution Analyzer."""

import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.layout import Layout
from rich.text import Text

from .hardware_analyzer import HardwareAnalyzer
from .llm_analyzer import LLMAnalyzer
from .moores_law import MooresLawAnalyzer
from .visualizations import Plotter
from .exports import Exporter


class CLI:
    """Interactive command-line interface."""

    def __init__(self):
        """Initialize CLI."""
        self.console = Console()
        self.hw_analyzer = None
        self.llm_analyzer = None
        self.moores_law = MooresLawAnalyzer()
        self.plotter = Plotter()
        self.exporter = Exporter()

    def show_banner(self):
        """Display application banner."""
        banner = Text()
        banner.append("Computing & LLM Evolution Analyzer\n", style="bold cyan")
        banner.append("Version 2.0.0\n", style="dim")
        banner.append("\nAnalyze hardware and LLM evolution over time", style="italic")

        panel = Panel(
            banner,
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(panel)
        self.console.print()

    def show_main_menu(self) -> str:
        """Display main menu and get user choice."""
        self.console.print("\n[bold cyan]Main Menu[/bold cyan]")
        self.console.print("[1] Hardware Analysis")
        self.console.print("[2] LLM Analysis")
        self.console.print("[3] Moore's Law Analysis")
        self.console.print("[4] Compare Hardware vs LLM Evolution")
        self.console.print("[5] Export Data")
        self.console.print("[6] Generate Visualizations")
        self.console.print("[0] Exit")
        self.console.print()

        choice = Prompt.ask(
            "Select an option",
            choices=["0", "1", "2", "3", "4", "5", "6"],
            default="1"
        )
        return choice

    def load_data(self):
        """Load hardware and LLM data."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task1 = progress.add_task("[cyan]Loading hardware data...", total=None)
            self.hw_analyzer = HardwareAnalyzer()
            progress.update(task1, completed=True)

            task2 = progress.add_task("[cyan]Loading LLM data...", total=None)
            self.llm_analyzer = LLMAnalyzer()
            progress.update(task2, completed=True)

        self.console.print("[green]Data loaded successfully![/green]\n")

    def hardware_analysis_menu(self):
        """Hardware analysis submenu."""
        while True:
            self.console.print("\n[bold cyan]Hardware Analysis Menu[/bold cyan]")
            self.console.print("[1] View All Systems")
            self.console.print("[2] Calculate CAGR for All Metrics")
            self.console.print("[3] View Specific Metric Growth")
            self.console.print("[4] Efficiency Trends")
            self.console.print("[5] Summary Statistics")
            self.console.print("[0] Back to Main Menu")
            self.console.print()

            choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5"])

            if choice == "0":
                break
            elif choice == "1":
                self.show_all_systems()
            elif choice == "2":
                self.show_hardware_cagr()
            elif choice == "3":
                self.show_metric_growth()
            elif choice == "4":
                self.show_efficiency_trends()
            elif choice == "5":
                self.show_hardware_summary()

    def show_all_systems(self):
        """Display all hardware systems."""
        table = Table(title="Hardware Systems", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Manufacturer")
        table.add_column("CPU", style="yellow")
        table.add_column("Transistors", justify="right")
        table.add_column("Clock (MHz)", justify="right")

        for system in self.hw_analyzer.systems:
            table.add_row(
                str(system.year),
                system.name,
                system.manufacturer,
                system.cpu_name,
                f"{system.cpu_transistors:,}",
                f"{system.cpu_clock_mhz:.2f}",
            )

        self.console.print(table)

    def show_hardware_cagr(self):
        """Display CAGR for all hardware metrics."""
        results = self.hw_analyzer.calculate_all_cagrs()

        table = Table(title="Hardware CAGR Analysis", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Start Value", justify="right")
        table.add_column("End Value", justify="right")
        table.add_column("Growth Factor", justify="right", style="yellow")
        table.add_column("CAGR %", justify="right", style="green")

        for metric_name, result in results.items():
            table.add_row(
                metric_name.replace('_', ' ').title(),
                f"{result.start_value:,.2f}",
                f"{result.end_value:,.2f}",
                f"{result.growth_factor:.2f}x",
                f"{result.cagr_percent:.2f}%",
            )

        self.console.print(table)

    def show_metric_growth(self):
        """Show growth for a specific metric."""
        metric = Prompt.ask(
            "Enter metric name",
            default="cpu_transistors"
        )

        try:
            result = self.hw_analyzer.analyze_metric_growth(metric)

            panel = Panel(
                f"[cyan]Metric:[/cyan] {result.metric_name}\n"
                f"[cyan]Period:[/cyan] {result.start_year} - {result.end_year}\n"
                f"[cyan]Start Value:[/cyan] {result.start_value:,.2f}\n"
                f"[cyan]End Value:[/cyan] {result.end_value:,.2f}\n"
                f"[yellow]Growth Factor:[/yellow] {result.growth_factor:.2f}x\n"
                f"[green]CAGR:[/green] {result.cagr_percent:.2f}%",
                title="Metric Growth Analysis",
                border_style="green",
            )
            self.console.print(panel)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def show_efficiency_trends(self):
        """Display efficiency trends."""
        trends = self.hw_analyzer.get_efficiency_trends()

        for metric_name, data in trends.items():
            if not data:
                continue

            table = Table(title=f"{metric_name.replace('_', ' ').title()}", box=box.SIMPLE)
            table.add_column("Year", style="cyan")
            table.add_column("System", style="green")
            table.add_column("Value", justify="right", style="yellow")

            for item in data[-10:]:  # Show last 10
                table.add_row(
                    str(item['year']),
                    item['name'][:30],
                    f"{item['value']:.4f}",
                )

            self.console.print(table)

    def show_hardware_summary(self):
        """Display hardware summary statistics."""
        summary = self.hw_analyzer.get_summary_statistics()

        panel = Panel(
            f"[cyan]Total Systems:[/cyan] {summary['total_systems']}\n"
            f"[cyan]Year Range:[/cyan] {summary['year_range']}\n"
            f"[cyan]Manufacturers:[/cyan] {len(summary['manufacturers'])}\n"
            f"[cyan]Architectures:[/cyan] {len(summary['architectures'])}\n"
            f"[cyan]Earliest:[/cyan] {summary['earliest_system']}\n"
            f"[cyan]Latest:[/cyan] {summary['latest_system']}",
            title="Hardware Summary",
            border_style="cyan",
        )
        self.console.print(panel)

    def llm_analysis_menu(self):
        """LLM analysis submenu."""
        while True:
            self.console.print("\n[bold cyan]LLM Analysis Menu[/bold cyan]")
            self.console.print("[1] View All Models")
            self.console.print("[2] Calculate CAGR for All Metrics")
            self.console.print("[3] Chinchilla Optimal Analysis")
            self.console.print("[4] Capability Comparison")
            self.console.print("[5] Cost Efficiency Analysis")
            self.console.print("[6] Summary Statistics")
            self.console.print("[0] Back to Main Menu")
            self.console.print()

            choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5", "6"])

            if choice == "0":
                break
            elif choice == "1":
                self.show_all_llms()
            elif choice == "2":
                self.show_llm_cagr()
            elif choice == "3":
                self.show_chinchilla_analysis()
            elif choice == "4":
                self.show_capability_comparison()
            elif choice == "5":
                self.show_cost_efficiency()
            elif choice == "6":
                self.show_llm_summary()

    def show_all_llms(self):
        """Display all LLM models."""
        table = Table(title="LLM Models", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Organization")
        table.add_column("Parameters (B)", justify="right")
        table.add_column("Context", justify="right")
        table.add_column("Open Source", justify="center")

        for model in self.llm_analyzer.models:
            table.add_row(
                str(model.year),
                model.name,
                model.organization,
                f"{model.parameters_billions:.1f}",
                f"{model.context_window:,}",
                "[green]Yes[/green]" if model.open_source else "[red]No[/red]",
            )

        self.console.print(table)

    def show_llm_cagr(self):
        """Display CAGR for LLM metrics."""
        results = self.llm_analyzer.calculate_all_cagrs()

        table = Table(title="LLM CAGR Analysis", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Start Value", justify="right")
        table.add_column("End Value", justify="right")
        table.add_column("Growth Factor", justify="right", style="yellow")
        table.add_column("CAGR %", justify="right", style="green")

        for metric_name, result in results.items():
            table.add_row(
                metric_name.replace('_', ' ').title(),
                f"{result.start_value:,.2f}",
                f"{result.end_value:,.2f}",
                f"{result.growth_factor:.2f}x",
                f"{result.cagr_percent:.2f}%",
            )

        self.console.print(table)

    def show_chinchilla_analysis(self):
        """Display Chinchilla optimal analysis."""
        results = self.llm_analyzer.analyze_chinchilla_optimal()

        table = Table(title="Chinchilla Optimal Analysis", box=box.ROUNDED)
        table.add_column("Model", style="green")
        table.add_column("Parameters (B)", justify="right")
        table.add_column("Training Tokens (B)", justify="right")
        table.add_column("Optimal Tokens (B)", justify="right")
        table.add_column("Status", justify="center")

        for result in results[-15:]:  # Show last 15
            status_color = "green" if result['status'] == "optimal" else "yellow" if result['status'] == "overtrained" else "red"

            table.add_row(
                result['name'],
                f"{result['parameters_billions']:.1f}",
                f"{result['training_tokens_billions']:.1f}",
                f"{result['optimal_tokens_billions']:.1f}",
                f"[{status_color}]{result['status']}[/{status_color}]",
            )

        self.console.print(table)

    def show_capability_comparison(self):
        """Display capability score comparison."""
        # Get latest models
        latest_models = sorted(self.llm_analyzer.models, key=lambda m: m.year, reverse=True)[:10]

        table = Table(title="LLM Capability Scores", box=box.ROUNDED)
        table.add_column("Model", style="green")
        table.add_column("Reasoning", justify="right")
        table.add_column("Coding", justify="right")
        table.add_column("Math", justify="right")
        table.add_column("Knowledge", justify="right")
        table.add_column("Multilingual", justify="right")
        table.add_column("Average", justify="right", style="yellow")

        for model in latest_models:
            avg = (model.capability_score_reasoning + model.capability_score_coding +
                   model.capability_score_math + model.capability_score_knowledge +
                   model.capability_score_multilingual) / 5

            table.add_row(
                model.name,
                f"{model.capability_score_reasoning:.1f}",
                f"{model.capability_score_coding:.1f}",
                f"{model.capability_score_math:.1f}",
                f"{model.capability_score_knowledge:.1f}",
                f"{model.capability_score_multilingual:.1f}",
                f"{avg:.1f}",
            )

        self.console.print(table)

    def show_cost_efficiency(self):
        """Display cost efficiency analysis."""
        results = self.llm_analyzer.analyze_cost_efficiency()

        table = Table(title="Cost Efficiency Analysis", box=box.ROUNDED)
        table.add_column("Model", style="green")
        table.add_column("Cost/1M In", justify="right")
        table.add_column("Avg Score", justify="right")
        table.add_column("Efficiency", justify="right", style="yellow")

        for result in results[:10]:  # Top 10
            table.add_row(
                result['name'],
                f"${result['cost_per_1m_input']:.2f}",
                f"{result['avg_capability_score']:.1f}",
                f"{result['cost_efficiency']:.2f}",
            )

        self.console.print(table)

    def show_llm_summary(self):
        """Display LLM summary statistics."""
        summary = self.llm_analyzer.get_summary_statistics()

        panel = Panel(
            f"[cyan]Total Models:[/cyan] {summary['total_models']}\n"
            f"[cyan]Year Range:[/cyan] {summary['year_range']}\n"
            f"[cyan]Organizations:[/cyan] {len(summary['organizations'])}\n"
            f"[cyan]Open Source:[/cyan] {summary['open_source_count']}\n"
            f"[cyan]Closed Source:[/cyan] {summary['closed_source_count']}\n"
            f"[cyan]Max Parameters:[/cyan] {summary['max_parameters']:.1f}B\n"
            f"[cyan]Max Context:[/cyan] {summary['max_context_window']:,}",
            title="LLM Summary",
            border_style="cyan",
        )
        self.console.print(panel)

    def run(self):
        """Run the CLI application."""
        try:
            self.show_banner()
            self.load_data()

            while True:
                choice = self.show_main_menu()

                if choice == "0":
                    self.console.print("\n[cyan]Thank you for using the analyzer![/cyan]")
                    break
                elif choice == "1":
                    self.hardware_analysis_menu()
                elif choice == "2":
                    self.llm_analysis_menu()
                elif choice == "3":
                    self.console.print("[yellow]Moore's Law analysis coming soon![/yellow]")
                elif choice == "4":
                    self.console.print("[yellow]Comparison coming soon![/yellow]")
                elif choice == "5":
                    self.console.print("[yellow]Export features coming soon![/yellow]")
                elif choice == "6":
                    self.console.print("[yellow]Visualizations coming soon![/yellow]")

        except KeyboardInterrupt:
            self.console.print("\n\n[yellow]Interrupted by user[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
