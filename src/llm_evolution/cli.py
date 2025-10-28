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
from .gpu_analyzer import GPUAnalyzer
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
        self.gpu_analyzer = None
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
        self.console.print("[3] GPU Analysis")
        self.console.print("[4] Moore's Law Analysis")
        self.console.print("[5] Compare Hardware vs LLM vs GPU Evolution")
        self.console.print("[6] Export Data")
        self.console.print("[7] Generate Visualizations")
        self.console.print("[0] Exit")
        self.console.print()

        choice = Prompt.ask(
            "Select an option",
            choices=["0", "1", "2", "3", "4", "5", "6", "7"],
            default="1"
        )
        return choice

    def load_data(self):
        """Load hardware, LLM, and GPU data."""
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

            task3 = progress.add_task("[cyan]Loading GPU data...", total=None)
            self.gpu_analyzer = GPUAnalyzer()
            progress.update(task3, completed=True)

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

    def gpu_analysis_menu(self):
        """GPU analysis submenu."""
        while True:
            self.console.print("\n[bold cyan]GPU Analysis Menu[/bold cyan]")
            self.console.print("[1] View All GPUs")
            self.console.print("[2] Calculate CAGR for All Metrics")
            self.console.print("[3] Manufacturer Comparison")
            self.console.print("[4] Performance Evolution")
            self.console.print("[5] Memory Evolution")
            self.console.print("[6] Efficiency Trends")
            self.console.print("[7] Architectural Milestones")
            self.console.print("[8] Summary Statistics")
            self.console.print("[0] Back to Main Menu")
            self.console.print()

            choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"])

            if choice == "0":
                break
            elif choice == "1":
                self.show_all_gpus()
            elif choice == "2":
                self.show_gpu_cagr()
            elif choice == "3":
                self.show_gpu_manufacturer_comparison()
            elif choice == "4":
                self.show_gpu_performance_evolution()
            elif choice == "5":
                self.show_gpu_memory_evolution()
            elif choice == "6":
                self.show_gpu_efficiency_trends()
            elif choice == "7":
                self.show_gpu_milestones()
            elif choice == "8":
                self.show_gpu_summary()

    def show_all_gpus(self):
        """Display all GPU models."""
        table = Table(title="GPU Models", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Manufacturer")
        table.add_column("TFLOPS", justify="right", style="yellow")
        table.add_column("VRAM", justify="right")
        table.add_column("TDP (W)", justify="right")

        for gpu in self.gpu_analyzer.gpus:
            table.add_row(
                str(gpu.year),
                gpu.name[:35],
                gpu.manufacturer,
                f"{gpu.tflops_fp32:.2f}",
                f"{gpu.vram_mb // 1024}GB",
                f"{gpu.tdp_watts}W",
            )

        self.console.print(table)

    def show_gpu_cagr(self):
        """Display CAGR for GPU metrics."""
        results = self.gpu_analyzer.calculate_all_cagrs()

        table = Table(title="GPU CAGR Analysis", box=box.ROUNDED)
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

    def show_gpu_manufacturer_comparison(self):
        """Display manufacturer comparison."""
        comparison = self.gpu_analyzer.get_manufacturer_comparison()

        table = Table(title="GPU Manufacturer Comparison", box=box.ROUNDED)
        table.add_column("Manufacturer", style="cyan")
        table.add_column("GPU Count", justify="right")
        table.add_column("Avg TFLOPS", justify="right", style="yellow")
        table.add_column("Avg VRAM (GB)", justify="right")
        table.add_column("Avg TDP (W)", justify="right")
        table.add_column("Ray Tracing GPUs", justify="right", style="green")

        for mfr, stats in comparison.items():
            table.add_row(
                mfr,
                str(stats['count']),
                f"{stats['avg_tflops_fp32']:.2f}",
                f"{stats['avg_vram_mb'] / 1024:.1f}",
                f"{stats['avg_tdp_watts']:.0f}",
                str(stats['ray_tracing_count']),
            )

        self.console.print(table)

    def show_gpu_performance_evolution(self):
        """Display GPU performance evolution."""
        evolution = self.gpu_analyzer.get_performance_evolution()

        table = Table(title="GPU Performance Evolution (Max per Year)", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("GPU", style="green")
        table.add_column("Manufacturer")
        table.add_column("TFLOPS", justify="right", style="yellow")

        for item in evolution:
            table.add_row(
                str(item['year']),
                item['gpu_name'][:40],
                item['manufacturer'],
                f"{item['tflops']:.2f}",
            )

        self.console.print(table)

    def show_gpu_memory_evolution(self):
        """Display GPU memory evolution."""
        evolution = self.gpu_analyzer.get_memory_evolution()

        table = Table(title="GPU Memory Evolution (Max per Year)", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("GPU", style="green")
        table.add_column("Manufacturer")
        table.add_column("VRAM", justify="right", style="yellow")

        for item in evolution:
            table.add_row(
                str(item['year']),
                item['gpu_name'][:40],
                item['manufacturer'],
                f"{item['vram_gb']:.1f} GB",
            )

        self.console.print(table)

    def show_gpu_efficiency_trends(self):
        """Display GPU efficiency trends."""
        trends = self.gpu_analyzer.get_efficiency_trends()

        for metric_name, data in trends.items():
            if not data:
                continue

            table = Table(title=f"{metric_name.replace('_', ' ').title()}", box=box.SIMPLE)
            table.add_column("Year", style="cyan")
            table.add_column("GPU", style="green")
            table.add_column("Manufacturer")
            table.add_column("Value", justify="right", style="yellow")

            for item in data[-10:]:  # Show last 10
                table.add_row(
                    str(item['year']),
                    item['name'][:35],
                    item['manufacturer'],
                    f"{item['value']:.4f}",
                )

            self.console.print(table)

    def show_gpu_milestones(self):
        """Display architectural milestones."""
        milestones = self.gpu_analyzer.get_architectural_milestones()

        table = Table(title="GPU Architectural Milestones", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("GPU", style="green")
        table.add_column("Manufacturer")
        table.add_column("Architecture")
        table.add_column("Milestone", style="yellow")

        for m in milestones:
            table.add_row(
                str(m['year']),
                m['name'][:35],
                m['manufacturer'],
                m['architecture'],
                m['reasons'][0][:40],
            )

        self.console.print(table)

    def show_gpu_summary(self):
        """Display GPU summary statistics."""
        summary = self.gpu_analyzer.get_summary_statistics()

        panel = Panel(
            f"[cyan]Total GPUs:[/cyan] {summary['total_gpus']}\n"
            f"[cyan]Year Range:[/cyan] {summary['year_range']}\n"
            f"[cyan]Manufacturers:[/cyan] {', '.join(summary['manufacturers'])}\n"
            f"[cyan]NVIDIA:[/cyan] {summary['manufacturer_count'].get('NVIDIA', 0)} GPUs\n"
            f"[cyan]AMD:[/cyan] {summary['manufacturer_count'].get('AMD', 0)} GPUs\n"
            f"[cyan]Intel:[/cyan] {summary['manufacturer_count'].get('Intel', 0)} GPUs\n"
            f"[cyan]Max TFLOPS:[/cyan] {summary['max_tflops']:.2f}\n"
            f"[cyan]Max VRAM:[/cyan] {summary['max_vram_gb']:.1f} GB\n"
            f"[cyan]Ray Tracing GPUs:[/cyan] {summary['ray_tracing_count']}",
            title="GPU Summary",
            border_style="cyan",
        )
        self.console.print(panel)

    def moores_law_menu(self):
        """Moore's Law analysis submenu."""
        while True:
            self.console.print("\n[bold cyan]Moore's Law Analysis Menu[/bold cyan]")
            self.console.print("[1] Historical Adherence Analysis")
            self.console.print("[2] Era Trends (5-year periods)")
            self.console.print("[3] Future Predictions")
            self.console.print("[4] Specific Year Comparison")
            self.console.print("[0] Back to Main Menu")
            self.console.print()

            choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4"])

            if choice == "0":
                break
            elif choice == "1":
                self.show_moores_law_adherence()
            elif choice == "2":
                self.show_moores_law_eras()
            elif choice == "3":
                self.show_moores_law_predictions()
            elif choice == "4":
                self.show_moores_law_year_comparison()

    def show_moores_law_adherence(self):
        """Display Moore's Law historical adherence."""
        results = self.moores_law.analyze_historical_adherence(self.hw_analyzer.systems)

        table = Table(title="Moore's Law Historical Adherence", box=box.ROUNDED)
        table.add_column("System", style="green")
        table.add_column("Year", style="cyan")
        table.add_column("Actual", justify="right")
        table.add_column("Predicted", justify="right")
        table.add_column("Accuracy %", justify="right", style="yellow")
        table.add_column("Status", justify="center")

        for result in results[-15:]:  # Show last 15
            status_color = "green" if result['ahead_behind'] == "on_track" else "yellow" if result['ahead_behind'] == "ahead" else "red"

            table.add_row(
                result['system_name'][:30],
                str(result['year']),
                f"{result['actual_transistors']:,.0f}",
                f"{result['predicted_transistors']:,.0f}",
                f"{result['accuracy_percent']:.1f}%",
                f"[{status_color}]{result['ahead_behind']}[/{status_color}]",
            )

        self.console.print(table)

    def show_moores_law_eras(self):
        """Display Moore's Law era analysis."""
        results = self.moores_law.analyze_era_trends(self.hw_analyzer.systems, era_length=5)

        table = Table(title="Moore's Law Era Analysis (5-year periods)", box=box.ROUNDED)
        table.add_column("Era", style="cyan")
        table.add_column("Systems", justify="right")
        table.add_column("Doubling Period", justify="right", style="yellow")
        table.add_column("Growth Rate %", justify="right")
        table.add_column("Adherence", justify="center")

        for result in results:
            adherence_color = "green" if result['moores_law_adherence'] == "strong" else "yellow" if result['moores_law_adherence'] == "moderate" else "red"

            table.add_row(
                result['era_label'],
                str(result['system_count']),
                f"{result['doubling_period']:.2f} yrs",
                f"{result['annual_growth_rate_percent']:.1f}%",
                f"[{adherence_color}]{result['moores_law_adherence']}[/{adherence_color}]",
            )

        self.console.print(table)

    def show_moores_law_predictions(self):
        """Display Moore's Law future predictions."""
        years_ahead = IntPrompt.ask("How many years ahead to predict?", default=10)

        # Use latest system as base
        base_system = self.hw_analyzer.systems[-1]
        predictions = self.moores_law.predict_future(base_system, years_ahead)

        table = Table(title=f"Moore's Law Predictions from {base_system.year}", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("Years Ahead", justify="right")
        table.add_column("Predicted Transistors", justify="right", style="yellow")
        table.add_column("Predicted Process (nm)", justify="right")
        table.add_column("Doublings", justify="right")

        for pred in predictions:
            table.add_row(
                str(pred['year']),
                str(pred['years_from_base']),
                f"{pred['predicted_transistors']:,}",
                f"{pred['predicted_process_nm']:.1f}",
                f"{pred['doublings_from_base']:.2f}",
            )

        self.console.print(table)

    def show_moores_law_year_comparison(self):
        """Display Moore's Law prediction vs reality for a specific year."""
        year = IntPrompt.ask("Enter year to analyze", default=2020)

        result = self.moores_law.compare_predictions_vs_reality(self.hw_analyzer.systems, year)

        if result:
            panel = Panel(
                f"[cyan]Prediction Year:[/cyan] {result['prediction_year']}\n"
                f"[cyan]Base System:[/cyan] {result['base_system']} ({result['base_year']})\n"
                f"[cyan]Base Transistors:[/cyan] {result['base_transistors']:,}\n"
                f"[cyan]Target System:[/cyan] {result['target_system']}\n"
                f"[cyan]Actual Transistors:[/cyan] {result['actual_transistors']:,}\n"
                f"[yellow]Predicted Transistors:[/yellow] {result['predicted_transistors']:,.0f}\n"
                f"[green]Accuracy:[/green] {result['accuracy_percent']:.1f}%\n"
                f"[cyan]Years Predicted:[/cyan] {result['years_predicted']}",
                title="Moore's Law Comparison",
                border_style="green",
            )
            self.console.print(panel)
        else:
            self.console.print(f"[red]No data available for year {year}[/red]")

    def export_menu(self):
        """Export data submenu."""
        while True:
            self.console.print("\n[bold cyan]Export Menu[/bold cyan]")
            self.console.print("[1] Export Hardware Data")
            self.console.print("[2] Export LLM Data")
            self.console.print("[3] Export GPU Data")
            self.console.print("[4] Export CAGR Analysis")
            self.console.print("[5] Export Complete Analysis Report")
            self.console.print("[0] Back to Main Menu")
            self.console.print()

            choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5"])

            if choice == "0":
                break
            elif choice == "1":
                self.export_hardware_data()
            elif choice == "2":
                self.export_llm_data()
            elif choice == "3":
                self.export_gpu_data()
            elif choice == "4":
                self.export_cagr_analysis()
            elif choice == "5":
                self.export_complete_report()

    def export_hardware_data(self):
        """Export hardware data to file."""
        format_choice = Prompt.ask(
            "Select format",
            choices=["json", "csv", "markdown", "text"],
            default="json"
        )

        data = self.hw_analyzer.to_dict()

        try:
            if format_choice == "json":
                path = self.exporter.export_json(data, "hardware_systems.json")
            elif format_choice == "csv":
                path = self.exporter.export_csv(data, "hardware_systems.csv")
            elif format_choice == "markdown":
                path = self.exporter.export_markdown(data, "hardware_systems.md", "Hardware Systems")
            elif format_choice == "text":
                path = self.exporter.export_text(data, "hardware_systems.txt", "Hardware Systems")

            self.console.print(f"[green]✓ Exported to {path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting: {e}[/red]")

    def export_llm_data(self):
        """Export LLM data to file."""
        format_choice = Prompt.ask(
            "Select format",
            choices=["json", "csv", "markdown", "text"],
            default="json"
        )

        data = self.llm_analyzer.to_dict()

        try:
            if format_choice == "json":
                path = self.exporter.export_json(data, "llm_models.json")
            elif format_choice == "csv":
                path = self.exporter.export_csv(data, "llm_models.csv")
            elif format_choice == "markdown":
                path = self.exporter.export_markdown(data, "llm_models.md", "LLM Models")
            elif format_choice == "text":
                path = self.exporter.export_text(data, "llm_models.txt", "LLM Models")

            self.console.print(f"[green]✓ Exported to {path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting: {e}[/red]")

    def export_gpu_data(self):
        """Export GPU data to file."""
        format_choice = Prompt.ask(
            "Select format",
            choices=["json", "csv", "markdown", "text"],
            default="json"
        )

        data = self.gpu_analyzer.to_dict()

        try:
            if format_choice == "json":
                path = self.exporter.export_json(data, "gpu_models.json")
            elif format_choice == "csv":
                path = self.exporter.export_csv(data, "gpu_models.csv")
            elif format_choice == "markdown":
                path = self.exporter.export_markdown(data, "gpu_models.md", "GPU Models")
            elif format_choice == "text":
                path = self.exporter.export_text(data, "gpu_models.txt", "GPU Models")

            self.console.print(f"[green]✓ Exported to {path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting: {e}[/red]")

    def export_cagr_analysis(self):
        """Export CAGR analysis."""
        hw_cagr = self.hw_analyzer.calculate_all_cagrs()
        llm_cagr = self.llm_analyzer.calculate_all_cagrs()
        gpu_cagr = self.gpu_analyzer.calculate_all_cagrs()

        analysis_data = {
            "title": "CAGR Analysis Report",
            "hardware_cagr": {k: v.to_dict() for k, v in hw_cagr.items()},
            "gpu_cagr": {k: v.to_dict() for k, v in gpu_cagr.items()},
            "llm_cagr": {k: v.to_dict() for k, v in llm_cagr.items()},
        }

        try:
            paths = self.exporter.export_analysis_report(
                analysis_data,
                "cagr_analysis",
                ["json", "markdown", "text"]
            )

            for fmt, path in paths.items():
                self.console.print(f"[green]✓ Exported {fmt}: {path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting: {e}[/red]")

    def export_complete_report(self):
        """Export complete analysis report."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("[cyan]Generating complete report...", total=None)

            hw_cagr = self.hw_analyzer.calculate_all_cagrs()
            llm_cagr = self.llm_analyzer.calculate_all_cagrs()
            gpu_cagr = self.gpu_analyzer.calculate_all_cagrs()
            hw_summary = self.hw_analyzer.get_summary_statistics()
            llm_summary = self.llm_analyzer.get_summary_statistics()
            gpu_summary = self.gpu_analyzer.get_summary_statistics()
            chinchilla = self.llm_analyzer.analyze_chinchilla_optimal()
            moores_eras = self.moores_law.analyze_era_trends(self.hw_analyzer.systems)

            analysis_data = {
                "title": "Complete Computing & LLM Evolution Analysis",
                "date_range": f"{self.hw_analyzer.systems[0].year}-{self.hw_analyzer.systems[-1].year}",
                "hardware_summary": hw_summary,
                "llm_summary": llm_summary,
                "gpu_summary": gpu_summary,
                "hardware_cagr": {k: v.to_dict() for k, v in hw_cagr.items()},
                "llm_cagr": {k: v.to_dict() for k, v in llm_cagr.items()},
                "gpu_cagr": {k: v.to_dict() for k, v in gpu_cagr.items()},
                "chinchilla_analysis": chinchilla,
                "moores_law_eras": moores_eras,
            }

            progress.update(task, completed=True)

        try:
            paths = self.exporter.export_analysis_report(
                analysis_data,
                "complete_analysis_report",
                ["json", "markdown", "text"]
            )

            self.console.print("\n[bold green]Complete Report Exported![/bold green]")
            for fmt, path in paths.items():
                self.console.print(f"  [{fmt}]: {path}")
        except Exception as e:
            self.console.print(f"[red]Error exporting: {e}[/red]")

    def visualizations_menu(self):
        """Visualizations submenu."""
        while True:
            self.console.print("\n[bold cyan]Visualizations Menu[/bold cyan]")
            self.console.print("[1] Hardware Transistor Evolution")
            self.console.print("[2] Moore's Law Comparison")
            self.console.print("[3] CAGR Heatmap")
            self.console.print("[4] LLM Parameter Scaling")
            self.console.print("[5] LLM Context Window Evolution")
            self.console.print("[6] LLM Capability Radar Chart")
            self.console.print("[7] Hardware Growth Factors")
            self.console.print("[8] GPU Performance Evolution")
            self.console.print("[9] GPU Memory Evolution")
            self.console.print("[10] GPU Efficiency Trends")
            self.console.print("[11] GPU Manufacturer Comparison")
            self.console.print("[12] GPU Price vs Performance")
            self.console.print("[0] Back to Main Menu")
            self.console.print()

            choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])

            if choice == "0":
                break
            elif choice == "1":
                self.plot_hardware_evolution()
            elif choice == "2":
                self.plot_moores_law_comparison()
            elif choice == "3":
                self.plot_cagr_heatmap()
            elif choice == "4":
                self.plot_llm_parameters()
            elif choice == "5":
                self.plot_context_window()
            elif choice == "6":
                self.plot_llm_capabilities()
            elif choice == "7":
                self.plot_growth_factors()
            elif choice == "8":
                self.plot_gpu_performance()
            elif choice == "9":
                self.plot_gpu_memory()
            elif choice == "10":
                self.plot_gpu_efficiency()
            elif choice == "11":
                self.plot_gpu_manufacturer_comp()
            elif choice == "12":
                self.plot_gpu_price_performance()

    def plot_hardware_evolution(self):
        """Plot hardware metric evolution."""
        metric = Prompt.ask(
            "Enter metric to plot",
            choices=["cpu_transistors", "cpu_clock_mhz", "ram_mb", "storage_mb", "performance_mips"],
            default="cpu_transistors"
        )

        output_path = Path("output") / f"hardware_{metric}_evolution.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_hardware_evolution(
                self.hw_analyzer.systems,
                metric,
                output_path,
                log_scale=True
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_moores_law_comparison(self):
        """Plot Moore's Law prediction vs actual."""
        # Generate predictions for all years
        base_system = self.hw_analyzer.systems[0]
        predictions = []

        for system in self.hw_analyzer.systems:
            pred = self.moores_law.predict_transistors(
                base_system.cpu_transistors,
                base_system.year,
                system.year
            )
            predictions.append(pred)

        output_path = Path("output") / "moores_law_comparison.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_moores_law_comparison(
                self.hw_analyzer.systems,
                predictions,
                output_path
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_cagr_heatmap(self):
        """Plot CAGR heatmap."""
        results = self.hw_analyzer.calculate_all_cagrs()
        cagr_data = {k: v.cagr_percent for k, v in results.items()}

        output_path = Path("output") / "cagr_heatmap.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_cagr_heatmap(cagr_data, output_path)
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_llm_parameters(self):
        """Plot LLM parameter scaling."""
        output_path = Path("output") / "llm_parameter_scaling.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_llm_parameter_scaling(
                self.llm_analyzer.models,
                output_path
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_context_window(self):
        """Plot context window evolution."""
        output_path = Path("output") / "context_window_evolution.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_context_window_evolution(
                self.llm_analyzer.models,
                output_path
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_llm_capabilities(self):
        """Plot LLM capability radar chart."""
        # Get latest 5 models
        latest_models = sorted(self.llm_analyzer.models, key=lambda m: m.year, reverse=True)[:5]

        output_path = Path("output") / "llm_capabilities_radar.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_llm_capability_radar(latest_models, output_path)
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_growth_factors(self):
        """Plot hardware growth factors."""
        results = self.hw_analyzer.calculate_all_cagrs()

        output_path = Path("output") / "growth_factors.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_growth_factors(results, output_path)
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_gpu_performance(self):
        """Plot GPU performance evolution."""
        output_path = Path("output") / "gpu_performance_evolution.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_gpu_performance_evolution(
                self.gpu_analyzer.gpus,
                output_path
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_gpu_memory(self):
        """Plot GPU memory evolution."""
        output_path = Path("output") / "gpu_memory_evolution.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_gpu_memory_evolution(
                self.gpu_analyzer.gpus,
                output_path
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_gpu_efficiency(self):
        """Plot GPU efficiency trends."""
        output_path = Path("output") / "gpu_efficiency.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_gpu_efficiency(
                self.gpu_analyzer.gpus,
                output_path
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_gpu_manufacturer_comp(self):
        """Plot GPU manufacturer comparison."""
        comparison = self.gpu_analyzer.get_manufacturer_comparison()
        output_path = Path("output") / "gpu_manufacturer_comparison.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_gpu_manufacturer_comparison(comparison, output_path)
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def plot_gpu_price_performance(self):
        """Plot GPU price vs performance."""
        output_path = Path("output") / "gpu_price_performance.png"
        output_path.parent.mkdir(exist_ok=True)

        try:
            self.plotter.plot_gpu_price_performance(
                self.gpu_analyzer.gpus,
                output_path
            )
            self.console.print(f"[green]✓ Plot saved to {output_path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error creating plot: {e}[/red]")

    def comparison_menu(self):
        """Hardware vs LLM vs GPU comparison submenu."""
        self.console.print("\n[bold cyan]Hardware vs LLM vs GPU Evolution Comparison[/bold cyan]\n")

        hw_cagr = self.hw_analyzer.calculate_all_cagrs()
        llm_cagr = self.llm_analyzer.calculate_all_cagrs()
        gpu_cagr = self.gpu_analyzer.calculate_all_cagrs()

        # Hardware summary
        self.console.print("[yellow]Hardware Evolution (1965-2024)[/yellow]")
        hw_table = Table(box=box.SIMPLE)
        hw_table.add_column("Metric", style="cyan")
        hw_table.add_column("CAGR %", justify="right", style="green")

        for metric, result in hw_cagr.items():
            hw_table.add_row(
                metric.replace('_', ' ').title(),
                f"{result.cagr_percent:.2f}%"
            )

        self.console.print(hw_table)
        self.console.print()

        # GPU summary
        self.console.print("[yellow]GPU Evolution (1999-2024)[/yellow]")
        gpu_table = Table(box=box.SIMPLE)
        gpu_table.add_column("Metric", style="cyan")
        gpu_table.add_column("CAGR %", justify="right", style="green")

        for metric, result in gpu_cagr.items():
            gpu_table.add_row(
                metric.replace('_', ' ').title(),
                f"{result.cagr_percent:.2f}%"
            )

        self.console.print(gpu_table)
        self.console.print()

        # LLM summary
        self.console.print("[yellow]LLM Evolution (2018-2024)[/yellow]")
        llm_table = Table(box=box.SIMPLE)
        llm_table.add_column("Metric", style="cyan")
        llm_table.add_column("CAGR %", justify="right", style="green")

        for metric, result in llm_cagr.items():
            llm_table.add_row(
                metric.replace('_', ' ').title(),
                f"{result.cagr_percent:.2f}%"
            )

        self.console.print(llm_table)
        self.console.print()

        # Key insights
        panel = Panel(
            "[cyan]Key Insights:[/cyan]\n"
            f"• CPU transistors grew {hw_cagr['cpu_transistors'].growth_factor:.1f}x over 59 years ({hw_cagr['cpu_transistors'].cagr_percent:.1f}% CAGR)\n"
            f"• GPU TFLOPS grew {gpu_cagr['tflops_fp32'].growth_factor:.1f}x over 25 years ({gpu_cagr['tflops_fp32'].cagr_percent:.1f}% CAGR)\n"
            f"• GPU VRAM grew {gpu_cagr['vram_mb'].growth_factor:.0f}x over 25 years ({gpu_cagr['vram_mb'].cagr_percent:.1f}% CAGR)\n"
            f"• LLM parameters grew {llm_cagr['parameters_billions'].growth_factor:.1f}x in just 6 years ({llm_cagr['parameters_billions'].cagr_percent:.1f}% CAGR)\n"
            f"• LLM scaling is {llm_cagr['parameters_billions'].cagr_percent / hw_cagr['cpu_transistors'].cagr_percent:.1f}x faster than CPU transistor scaling\n"
            f"• GPU performance scaling is {gpu_cagr['tflops_fp32'].cagr_percent / hw_cagr['cpu_transistors'].cagr_percent:.1f}x faster than CPU transistor scaling",
            title="Comparison Summary",
            border_style="yellow",
        )
        self.console.print(panel)

        Prompt.ask("\nPress Enter to continue", default="")

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
                    self.gpu_analysis_menu()
                elif choice == "4":
                    self.moores_law_menu()
                elif choice == "5":
                    self.comparison_menu()
                elif choice == "6":
                    self.export_menu()
                elif choice == "7":
                    self.visualizations_menu()

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
