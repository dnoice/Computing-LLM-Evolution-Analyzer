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
from .cloud_cost_analyzer import CloudCostAnalyzer
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
        self.cloud_cost_analyzer = None
        self.moores_law = MooresLawAnalyzer()
        self.plotter = Plotter()
        self.exporter = Exporter()

    def show_banner(self):
        """Display application banner."""
        banner = Text()
        banner.append("Computing & LLM Evolution Analyzer\n", style="bold cyan")
        banner.append("Version 2.1.0\n", style="dim")
        banner.append("\nAnalyze hardware, LLM evolution, and cloud costs", style="italic")

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
        self.console.print("[8] Cloud Cost Analysis")
        self.console.print("[0] Exit")
        self.console.print()

        choice = Prompt.ask(
            "Select an option",
            choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"],
            default="1"
        )
        return choice

    def load_data(self):
        """Load hardware, LLM, GPU, and cloud cost data."""
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

            task4 = progress.add_task("[cyan]Loading cloud cost data...", total=None)
            self.cloud_cost_analyzer = CloudCostAnalyzer()
            progress.update(task4, completed=True)

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

    def cloud_cost_analysis_menu(self):
        """Cloud cost analysis submenu."""
        while True:
            self.console.print("\n[bold cyan]Cloud Cost Analysis Menu[/bold cyan]")
            self.console.print("[1] View All Cloud Instances")
            self.console.print("[2] Compare Providers for Training")
            self.console.print("[3] Compare Providers for Inference")
            self.console.print("[4] Cost Efficiency Ranking")
            self.console.print("[5] Spot Instance Savings Analysis")
            self.console.print("[6] Estimate LLM Training Cost")
            self.console.print("[7] GPU Price Evolution")
            self.console.print("[8] Provider Statistics")
            self.console.print("[9] Compare Specific Instances")
            self.console.print("[0] Back to Main Menu")
            self.console.print()

            choice = Prompt.ask(
                "Select an option",
                choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                default="1"
            )

            if choice == "0":
                break
            elif choice == "1":
                self._show_all_cloud_instances()
            elif choice == "2":
                self._compare_training_costs()
            elif choice == "3":
                self._compare_inference_costs()
            elif choice == "4":
                self._show_cost_efficiency()
            elif choice == "5":
                self._show_spot_savings()
            elif choice == "6":
                self._estimate_training_cost()
            elif choice == "7":
                self._show_gpu_price_evolution()
            elif choice == "8":
                self._show_provider_stats()
            elif choice == "9":
                self._compare_instances()

    def _show_all_cloud_instances(self):
        """Display all cloud instances."""
        table = Table(title="Cloud Compute Instances", box=box.ROUNDED)
        table.add_column("Provider", style="cyan")
        table.add_column("Instance Type", style="green")
        table.add_column("GPU Model", style="yellow")
        table.add_column("GPU Count", justify="right")
        table.add_column("GPU Memory", justify="right")
        table.add_column("vCPUs", justify="right")
        table.add_column("RAM (GB)", justify="right")
        table.add_column("On-Demand $/hr", justify="right", style="magenta")
        table.add_column("Spot $/hr", justify="right", style="green")

        for instance in self.cloud_cost_analyzer.instances:
            table.add_row(
                instance.provider,
                instance.instance_type,
                instance.gpu_model,
                str(instance.gpu_count),
                f"{instance.gpu_memory_gb}GB",
                str(instance.vcpus),
                f"{instance.ram_gb:.0f}",
                f"${instance.price_ondemand_hourly:.2f}",
                f"${instance.price_spot_hourly:.2f}" if instance.price_spot_hourly > 0 else "N/A"
            )

        self.console.print(table)
        Prompt.ask("\nPress Enter to continue", default="")

    def _compare_training_costs(self):
        """Compare cloud providers for training workload."""
        self.console.print("\n[bold cyan]Training Cost Comparison[/bold cyan]")

        training_hours = IntPrompt.ask(
            "Enter training time in hours",
            default=100
        )
        use_spot = Confirm.ask("Use spot pricing?", default=True)

        comparison = self.cloud_cost_analyzer.compare_providers_for_training(
            training_hours=training_hours,
            use_spot=use_spot
        )

        table = Table(title=f"Training Cost for {training_hours} Hours", box=box.ROUNDED)
        table.add_column("Provider", style="cyan")
        table.add_column("Instance Type", style="green")
        table.add_column("GPU Model", style="yellow")
        table.add_column("GPU Count", justify="right")
        table.add_column("Total TFLOPS", justify="right")
        table.add_column("Total Cost", justify="right", style="magenta")
        table.add_column("$/hour", justify="right")

        for provider, data in sorted(comparison.items(), key=lambda x: x[1]['total_cost_usd']):
            table.add_row(
                provider,
                data['instance_type'],
                data['gpu_model'],
                str(data['gpu_count']),
                f"{data['total_tflops_fp32']:.1f}",
                f"${data['total_cost_usd']:,.2f}",
                f"${data['hourly_rate']:.2f}"
            )

        self.console.print(table)

        # Visualize
        output_path = Path("output/cloud_training_comparison.png")
        output_path.parent.mkdir(exist_ok=True)
        self.plotter.plot_cloud_cost_comparison(
            comparison,
            title=f"Training Cost Comparison ({training_hours} hours)",
            output_path=output_path
        )
        self.console.print(f"\n[green]Visualization saved to {output_path}[/green]")

        Prompt.ask("\nPress Enter to continue", default="")

    def _compare_inference_costs(self):
        """Compare cloud providers for inference workload."""
        self.console.print("\n[bold cyan]Inference Cost Comparison[/bold cyan]")

        rps = IntPrompt.ask("Enter requests per second", default=10)
        tokens_per_request = IntPrompt.ask("Enter avg tokens per request", default=100)
        tokens_per_sec_per_gpu = IntPrompt.ask("Enter tokens/sec per GPU", default=50)
        days = IntPrompt.ask("Enter number of days", default=30)

        comparison = self.cloud_cost_analyzer.compare_providers_for_inference(
            requests_per_second=rps,
            avg_tokens_per_request=tokens_per_request,
            tokens_per_second_per_gpu=tokens_per_sec_per_gpu,
            days=days
        )

        table = Table(title=f"Inference Cost for {days} Days", box=box.ROUNDED)
        table.add_column("Provider", style="cyan")
        table.add_column("Instance Type", style="green")
        table.add_column("GPU Model", style="yellow")
        table.add_column("Instances Needed", justify="right")
        table.add_column("Total Cost", justify="right", style="magenta")
        table.add_column("Cost/1K Requests", justify="right")
        table.add_column("Cost/1M Tokens", justify="right")

        for provider, data in sorted(comparison.items(), key=lambda x: x[1]['total_cost_usd']):
            table.add_row(
                provider,
                data['instance_type'],
                data['gpu_model'],
                str(data['instances_needed']),
                f"${data['total_cost_usd']:,.2f}",
                f"${data['cost_per_1k_requests']:.4f}",
                f"${data['cost_per_1m_tokens']:.2f}"
            )

        self.console.print(table)

        # Visualize
        output_path = Path("output/cloud_inference_comparison.png")
        output_path.parent.mkdir(exist_ok=True)
        self.plotter.plot_cloud_cost_comparison(
            comparison,
            title=f"Inference Cost Comparison ({days} days)",
            output_path=output_path
        )
        self.console.print(f"\n[green]Visualization saved to {output_path}[/green]")

        Prompt.ask("\nPress Enter to continue", default="")

    def _show_cost_efficiency(self):
        """Show cost efficiency ranking."""
        workload = Prompt.ask(
            "Select workload type",
            choices=["training", "inference"],
            default="training"
        )

        ranking = self.cloud_cost_analyzer.get_cost_efficiency_ranking(workload_type=workload)

        table = Table(title=f"Cost Efficiency Ranking ({workload.title()})", box=box.ROUNDED)
        table.add_column("Rank", justify="right", style="cyan")
        table.add_column("Provider", style="cyan")
        table.add_column("Instance Type", style="green")
        table.add_column("GPU Model", style="yellow")
        table.add_column("TFLOPS/$", justify="right", style="magenta")
        table.add_column("On-Demand $/hr", justify="right")

        for i, instance in enumerate(ranking[:15], 1):
            table.add_row(
                str(i),
                instance['provider'],
                instance['instance_type'],
                instance['gpu_model'],
                f"{instance['tflops_per_dollar']:.2f}",
                f"${instance['price_ondemand_hourly']:.2f}"
            )

        self.console.print(table)

        # Visualize
        output_path = Path(f"output/cloud_efficiency_{workload}.png")
        output_path.parent.mkdir(exist_ok=True)
        self.plotter.plot_cost_efficiency_ranking(ranking, top_n=10, output_path=output_path)
        self.console.print(f"\n[green]Visualization saved to {output_path}[/green]")

        Prompt.ask("\nPress Enter to continue", default="")

    def _show_spot_savings(self):
        """Show spot instance savings analysis."""
        savings = self.cloud_cost_analyzer.get_spot_savings_analysis()

        table = Table(title="Spot Instance Savings Analysis", box=box.ROUNDED)
        table.add_column("Provider", style="cyan")
        table.add_column("Instance Type", style="green")
        table.add_column("GPU Model", style="yellow")
        table.add_column("On-Demand $/hr", justify="right")
        table.add_column("Spot $/hr", justify="right")
        table.add_column("Savings %", justify="right", style="green")
        table.add_column("Annual Savings", justify="right", style="magenta")

        for entry in savings[:12]:
            table.add_row(
                entry['provider'],
                entry['instance_type'],
                entry['gpu_model'],
                f"${entry['ondemand_hourly']:.2f}",
                f"${entry['spot_hourly']:.2f}",
                f"{entry['savings_percent']:.1f}%",
                f"${entry['annual_savings_usd']:,.0f}"
            )

        self.console.print(table)

        # Visualize
        output_path = Path("output/cloud_spot_savings.png")
        output_path.parent.mkdir(exist_ok=True)
        self.plotter.plot_spot_savings(savings, top_n=12, output_path=output_path)
        self.console.print(f"\n[green]Visualization saved to {output_path}[/green]")

        Prompt.ask("\nPress Enter to continue", default="")

    def _estimate_training_cost(self):
        """Estimate LLM training cost."""
        self.console.print("\n[bold cyan]LLM Training Cost Estimator[/bold cyan]")

        params_billions = IntPrompt.ask("Enter model size in billions of parameters", default=7)
        tokens_billions = IntPrompt.ask("Enter training tokens in billions", default=1000)
        use_spot = Confirm.ask("Use spot pricing?", default=True)

        estimate = self.cloud_cost_analyzer.estimate_llm_training_cost(
            parameters_billions=params_billions,
            training_tokens_billions=tokens_billions,
            use_spot=use_spot
        )

        # Display results
        panel = Panel(
            f"[cyan]Model Size:[/cyan] {estimate['model_size_params']}\n"
            f"[cyan]Training Tokens:[/cyan] {estimate['training_tokens']}\n"
            f"[cyan]Provider:[/cyan] {estimate['provider']}\n"
            f"[cyan]Instance Type:[/cyan] {estimate['instance_type']}\n"
            f"[cyan]GPU Model:[/cyan] {estimate['gpu_model']}\n"
            f"[cyan]GPU Count:[/cyan] {estimate['gpu_count']}\n"
            f"[cyan]Training Days:[/cyan] {estimate['training_days']:.1f}\n"
            f"[cyan]Pricing Model:[/cyan] {estimate['pricing_model']}\n\n"
            f"[magenta bold]Total Cost:[/magenta bold] ${estimate['total_cost_usd']:,.2f}\n"
            f"[green]Compute Cost:[/green] ${estimate['compute_cost_usd']:,.2f}\n"
            f"[green]Storage Cost:[/green] ${estimate['storage_cost_usd']:,.2f}\n"
            f"[yellow]Hourly Rate:[/yellow] ${estimate['hourly_rate']:.2f}/hr",
            title="Training Cost Estimate",
            border_style="green"
        )
        self.console.print(panel)

        # Visualize
        output_path = Path("output/cloud_training_estimate.png")
        output_path.parent.mkdir(exist_ok=True)
        self.plotter.plot_training_cost_breakdown(estimate, output_path=output_path)
        self.console.print(f"\n[green]Visualization saved to {output_path}[/green]")

        Prompt.ask("\nPress Enter to continue", default="")

    def _show_gpu_price_evolution(self):
        """Show GPU price evolution over time."""
        evolution = self.cloud_cost_analyzer.get_gpu_price_evolution()

        table = Table(title="GPU Price Evolution", box=box.ROUNDED)
        table.add_column("GPU Model", style="cyan")
        table.add_column("Provider", style="green")
        table.add_column("Year", justify="right")
        table.add_column("Instance Type", style="yellow")
        table.add_column("Price $/hr", justify="right", style="magenta")

        for gpu_model, price_data in evolution.items():
            for entry in price_data:
                table.add_row(
                    gpu_model,
                    entry['provider'],
                    str(entry['year']),
                    entry['instance_type'],
                    f"${entry['price_ondemand_hourly']:.2f}"
                )

        self.console.print(table)

        # Visualize
        output_path = Path("output/cloud_gpu_price_evolution.png")
        output_path.parent.mkdir(exist_ok=True)
        self.plotter.plot_gpu_price_evolution(evolution, output_path=output_path)
        self.console.print(f"\n[green]Visualization saved to {output_path}[/green]")

        Prompt.ask("\nPress Enter to continue", default="")

    def _show_provider_stats(self):
        """Show provider statistics."""
        stats = self.cloud_cost_analyzer.get_provider_statistics()

        for provider, data in stats.items():
            panel = Panel(
                f"[cyan]Instances:[/cyan] {data['instance_count']}\n"
                f"[cyan]Avg Hourly Cost:[/cyan] ${data['avg_hourly_cost']:.2f}\n"
                f"[cyan]Avg Spot Discount:[/cyan] {data['avg_spot_discount_percent']:.1f}%\n"
                f"[cyan]Total GPUs:[/cyan] {data['total_gpus']}\n"
                f"[cyan]Unique GPU Models:[/cyan] {data['unique_gpu_models']}\n"
                f"[cyan]Training Instances:[/cyan] {data['training_instances']}\n"
                f"[cyan]Inference Instances:[/cyan] {data['inference_instances']}\n"
                f"[cyan]Price Range:[/cyan] ${data['price_range']['min']:.2f} - ${data['price_range']['max']:.2f}/hr\n"
                f"[cyan]GPU Models:[/cyan] {', '.join(data['gpu_models'])}",
                title=f"{provider} Statistics",
                border_style="cyan"
            )
            self.console.print(panel)
            self.console.print()

        # Visualize
        output_path = Path("output/cloud_provider_comparison.png")
        output_path.parent.mkdir(exist_ok=True)
        self.plotter.plot_provider_comparison_matrix(stats, output_path=output_path)
        self.console.print(f"[green]Visualization saved to {output_path}[/green]")

        Prompt.ask("\nPress Enter to continue", default="")

    def _compare_instances(self):
        """Compare specific instances."""
        self.console.print("\n[bold cyan]Compare Specific Instances[/bold cyan]")
        self.console.print("Enter instance types separated by commas")
        self.console.print("Example: p5.48xlarge, Standard_ND96amsr_A100_v4, a2-ultragpu-8g")

        instance_types_str = Prompt.ask("\nInstance types")
        instance_types = [t.strip() for t in instance_types_str.split(',')]

        comparison = self.cloud_cost_analyzer.compare_instance_specs(instance_types)

        if not comparison:
            self.console.print("[red]No instances found with those names[/red]")
            return

        table = Table(title="Instance Comparison", box=box.ROUNDED)
        table.add_column("Attribute", style="cyan")
        for instance in comparison:
            table.add_column(f"{instance['provider']}\n{instance['instance_type']}", style="green")

        attributes = [
            ('GPU Model', 'gpu_model'),
            ('GPU Count', 'gpu_count'),
            ('GPU Memory/GPU', lambda d: f"{d['gpu_memory_gb']}GB"),
            ('Total GPU Memory', lambda d: f"{d['total_gpu_memory_gb']}GB"),
            ('vCPUs', 'vcpus'),
            ('RAM', lambda d: f"{d['ram_gb']:.0f}GB"),
            ('TFLOPS FP32', lambda d: f"{d['tflops_fp32']:.1f}"),
            ('TFLOPS FP16', lambda d: f"{d['tflops_fp16']:.1f}"),
            ('On-Demand $/hr', lambda d: f"${d['price_ondemand_hourly']:.2f}"),
            ('Spot $/hr', lambda d: f"${d['price_spot_hourly']:.2f}"),
            ('TFLOPS/$', lambda d: f"{d['tflops_per_dollar']:.2f}"),
            ('Cost/GPU/hr', lambda d: f"${d['cost_per_gpu_hour']:.2f}"),
        ]

        for attr_name, attr_key in attributes:
            row = [attr_name]
            for instance in comparison:
                if callable(attr_key):
                    value = attr_key(instance)
                else:
                    value = str(instance[attr_key])
                row.append(value)
            table.add_row(*row)

        self.console.print(table)
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
                elif choice == "8":
                    self.cloud_cost_analysis_menu()

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
