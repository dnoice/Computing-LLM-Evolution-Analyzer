"""Interactive CLI for Computing & LLM Evolution Analyzer."""

import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
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

# Import new UI components
from .ui_components import (
    THEME, ICONS,
    create_banner, create_menu_option, create_styled_table,
    create_dashboard_panel, create_status_bar, create_help_text,
    create_help_screen, show_help, clear_screen,
    print_section_header, create_prompt_text,
    build_choice_validator, normalize_choice,
    BreadcrumbNav, Notify
)


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
        self.breadcrumbs = BreadcrumbNav()

    def show_banner(self):
        """Display application banner."""
        self.console.print(create_banner())

    def show_main_menu(self) -> str:
        """Display main menu and get user choice."""
        while True:  # Loop to handle help requests
            # Clear screen for clean display
            clear_screen(self.console)

            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Create menu title
            print_section_header(self.console, "Main Menu", "🏠")
            self.console.print()

            # Display menu options with both number and letter shortcuts
            self.console.print(create_menu_option("1", "h", "Hardware Analysis", ICONS['hardware'],
                                                 "CPU, RAM, storage evolution"))
            self.console.print(create_menu_option("2", "l", "LLM Analysis", ICONS['llm'],
                                                 "Model parameters, capabilities"))
            self.console.print(create_menu_option("3", "g", "GPU Analysis", ICONS['gpu'],
                                                 "Performance, efficiency trends"))
            self.console.print(create_menu_option("4", "m", "Moore's Law Analysis", ICONS['moores_law'],
                                                 "Historical adherence & predictions"))
            self.console.print(create_menu_option("5", "c", "Compare Evolution", ICONS['compare'],
                                                 "Hardware vs LLM vs GPU"))
            self.console.print(create_menu_option("6", "e", "Export Data", ICONS['export'],
                                                 "JSON, CSV, Markdown formats"))
            self.console.print(create_menu_option("7", "v", "Generate Visualizations", ICONS['visualize'],
                                                 "Charts and plots"))
            self.console.print(create_menu_option("8", "k", "Cloud Cost Analysis", ICONS['cloud'],
                                                 "AWS, Azure, GCP pricing"))
            self.console.print()
            self.console.print(create_menu_option("0", "q", "Exit", ICONS['exit'],
                                                 "Quit application"))

            # Status bar with tip
            self.console.print()
            self.console.print(create_status_bar("Ready", "Type number/letter or '?' for help"))
            self.console.print()

            # Build choice validator with both numbers and letters + help
            num_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
            letter_keys = ["q", "h", "l", "g", "m", "c", "e", "v", "k", "?"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            # Key mapping: letter -> number
            key_map = {
                "q": "0", "h": "1", "l": "2", "g": "3",
                "m": "4", "c": "5", "e": "6", "v": "7", "k": "8"
            }

            choice = Prompt.ask(
                create_prompt_text("Enter your choice"),
                choices=valid_choices,
                default="1"
            )

            # Handle help request
            if choice == "?":
                clear_screen(self.console)
                show_help(self.console)
                continue  # Show menu again

            # Normalize the choice to a number
            return normalize_choice(choice, key_map)

    def load_data(self):
        """Load hardware, LLM, GPU, and cloud cost data."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console,
        ) as progress:
            task1 = progress.add_task(f"[cyan]{ICONS['hardware']} Loading hardware data...", total=None)
            self.hw_analyzer = HardwareAnalyzer()
            progress.update(task1, completed=True)

            task2 = progress.add_task(f"[cyan]{ICONS['llm']} Loading LLM data...", total=None)
            self.llm_analyzer = LLMAnalyzer()
            progress.update(task2, completed=True)

            task3 = progress.add_task(f"[cyan]{ICONS['gpu']} Loading GPU data...", total=None)
            self.gpu_analyzer = GPUAnalyzer()
            progress.update(task3, completed=True)

            task4 = progress.add_task(f"[cyan]{ICONS['cloud']} Loading cloud cost data...", total=None)
            self.cloud_cost_analyzer = CloudCostAnalyzer()
            progress.update(task4, completed=True)

        Notify.success(self.console, "All data loaded successfully!", "Ready to analyze")

        # Show dashboard
        self.show_dashboard()

    def show_dashboard(self):
        """Display quick stats dashboard."""
        self.console.print()
        print_section_header(self.console, "Dataset Overview", "📊")
        self.console.print()

        # Create a layout with 3 columns
        from rich.columns import Columns

        # Hardware stats
        hw_stats = Text()
        hw_stats.append(f"{ICONS['hardware']} ", style=THEME['accent'])
        hw_stats.append("Hardware\n", style=f"bold {THEME['primary']}")
        hw_stats.append(f"  {len(self.hw_analyzer.systems)} systems\n", style=THEME['info'])
        hw_stats.append(f"  1965-2024\n", style=THEME['muted'])
        hw_stats.append(f"  59 years", style=THEME['muted'])

        hw_panel = Panel(hw_stats, box=box.ROUNDED, border_style=THEME['primary'])

        # GPU stats
        gpu_stats = Text()
        gpu_stats.append(f"{ICONS['gpu']} ", style=THEME['accent'])
        gpu_stats.append("GPUs\n", style=f"bold {THEME['primary']}")
        gpu_stats.append(f"  {len(self.gpu_analyzer.gpus)} GPUs\n", style=THEME['info'])
        gpu_stats.append(f"  1999-2024\n", style=THEME['muted'])
        gpu_stats.append(f"  3 manufacturers", style=THEME['muted'])

        gpu_panel = Panel(gpu_stats, box=box.ROUNDED, border_style=THEME['primary'])

        # LLM stats
        llm_stats = Text()
        llm_stats.append(f"{ICONS['llm']} ", style=THEME['accent'])
        llm_stats.append("LLMs\n", style=f"bold {THEME['primary']}")
        llm_stats.append(f"  {len(self.llm_analyzer.models)} models\n", style=THEME['info'])
        llm_stats.append(f"  2018-2024\n", style=THEME['muted'])
        llm_stats.append(f"  6 organizations", style=THEME['muted'])

        llm_panel = Panel(llm_stats, box=box.ROUNDED, border_style=THEME['primary'])

        # Cloud stats
        cloud_stats = Text()
        cloud_stats.append(f"{ICONS['cloud']} ", style=THEME['accent'])
        cloud_stats.append("Cloud\n", style=f"bold {THEME['primary']}")
        cloud_stats.append(f"  {len(self.cloud_cost_analyzer.instances)} instances\n", style=THEME['info'])
        cloud_stats.append(f"  3 providers\n", style=THEME['muted'])
        cloud_stats.append(f"  AWS/Azure/GCP", style=THEME['muted'])

        cloud_panel = Panel(cloud_stats, box=box.ROUNDED, border_style=THEME['primary'])

        # Display columns
        self.console.print(Columns([hw_panel, gpu_panel, llm_panel, cloud_panel], equal=True, expand=True))

        # Quick highlights
        self.console.print()
        highlights = Text()
        highlights.append("⚡ Quick Facts: ", style=f"bold {THEME['warning']}")
        highlights.append("CPU transistors grew ", style=THEME['muted'])
        highlights.append("41.4% CAGR", style=f"bold {THEME['success']}")
        highlights.append(" • GPU performance ", style=THEME['muted'])
        highlights.append("51.3% CAGR", style=f"bold {THEME['success']}")
        highlights.append(" • LLM parameters ", style=THEME['muted'])
        highlights.append("227% CAGR", style=f"bold {THEME['warning']}")

        self.console.print(Panel(highlights, box=box.SIMPLE, border_style=THEME['info']))

        self.console.print()
        self.console.print(create_status_bar("Dashboard", "Press Enter to continue to main menu"))
        Prompt.ask("", default="")

    def hardware_analysis_menu(self):
        """Hardware analysis submenu."""
        self.breadcrumbs.push("Hardware Analysis")

        while True:
            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Menu header
            print_section_header(self.console, "Hardware Analysis", ICONS['hardware'])
            self.console.print()

            # Menu options
            self.console.print(create_menu_option("1", "a", "View All Systems", "📋",
                                                 "Complete hardware timeline"))
            self.console.print(create_menu_option("2", "c", "Calculate CAGR", "📈",
                                                 "Growth rates for all metrics"))
            self.console.print(create_menu_option("3", "m", "Metric Growth", "🔍",
                                                 "Analyze specific metric"))
            self.console.print(create_menu_option("4", "e", "Efficiency Trends", "⚡",
                                                 "Performance per watt"))
            self.console.print(create_menu_option("5", "s", "Summary Statistics", "📊",
                                                 "Overview of dataset"))
            self.console.print()
            self.console.print(create_menu_option("0", "b", "Back", ICONS['back'],
                                                 "Return to main menu"))

            self.console.print()
            self.console.print(create_status_bar("Hardware Analysis", "Analyzing 30 systems (1965-2024)"))
            self.console.print()

            # Get choice
            num_keys = ["0", "1", "2", "3", "4", "5"]
            letter_keys = ["b", "a", "c", "m", "e", "s"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            key_map = {"b": "0", "a": "1", "c": "2", "m": "3", "e": "4", "s": "5"}

            choice = Prompt.ask(
                create_prompt_text("Your choice"),
                choices=valid_choices,
                default="1"
            )
            choice = normalize_choice(choice, key_map)

            if choice == "0":
                self.breadcrumbs.pop()
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
        table = create_styled_table(
            f"{ICONS['hardware']} Hardware Systems Timeline",
            box_style=box.ROUNDED
        )

        table.add_column("Year", style=THEME['info'], justify="center", width=6)
        table.add_column("Name", style=THEME['highlight'], no_wrap=False, min_width=25)
        table.add_column("Manufacturer", style=THEME['secondary'], width=15)
        table.add_column("CPU", style=THEME['muted'], no_wrap=False)
        table.add_column("Transistors", justify="right", style=THEME['accent'])
        table.add_column("Clock", justify="right", style=THEME['success'])

        for system in self.hw_analyzer.systems:
            table.add_row(
                str(system.year),
                system.name,
                system.manufacturer,
                system.cpu_name[:30] if len(system.cpu_name) > 30 else system.cpu_name,
                f"{system.cpu_transistors:,}",
                f"{system.cpu_clock_mhz:.0f} MHz",
            )

        self.console.print()
        self.console.print(table)
        self.console.print()
        self.console.print(create_status_bar(f"Showing {len(self.hw_analyzer.systems)} systems",
                                            "Press Enter to continue"))
        Prompt.ask("", default="")

    def show_hardware_cagr(self):
        """Display CAGR for all hardware metrics."""
        results = self.hw_analyzer.calculate_all_cagrs()

        table = create_styled_table(
            f"{ICONS['stats']} Hardware CAGR Analysis (1965-2024)",
            box_style=box.HEAVY
        )

        table.add_column("Metric", style=THEME['primary'], no_wrap=False, min_width=20)
        table.add_column("Start", justify="right", style=THEME['muted'])
        table.add_column("End", justify="right", style=THEME['highlight'])
        table.add_column("Growth", justify="right", style=THEME['warning'])
        table.add_column("CAGR", justify="right", style=THEME['success'], width=10)

        for metric_name, result in results.items():
            # Format large numbers
            if result.start_value >= 1e9:
                start_str = f"{result.start_value/1e9:.1f}B"
            elif result.start_value >= 1e6:
                start_str = f"{result.start_value/1e6:.1f}M"
            else:
                start_str = f"{result.start_value:,.0f}"

            if result.end_value >= 1e9:
                end_str = f"{result.end_value/1e9:.1f}B"
            elif result.end_value >= 1e6:
                end_str = f"{result.end_value/1e6:.1f}M"
            else:
                end_str = f"{result.end_value:,.0f}"

            table.add_row(
                metric_name.replace('_', ' ').title(),
                start_str,
                end_str,
                f"{result.growth_factor:,.0f}x",
                f"{result.cagr_percent:.1f}%",
            )

        self.console.print()
        self.console.print(table)
        self.console.print()
        Notify.info(self.console, "CAGR = Compound Annual Growth Rate",
                   "Shows exponential growth over the time period")
        Prompt.ask("\nPress Enter to continue", default="")

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
        self.breadcrumbs.push("LLM Analysis")

        while True:
            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Menu header
            print_section_header(self.console, "LLM Analysis", ICONS['llm'])
            self.console.print()

            # Menu options
            self.console.print(create_menu_option("1", "a", "View All Models", "📋",
                                                 "GPT, Claude, LLaMA, Gemini"))
            self.console.print(create_menu_option("2", "c", "Calculate CAGR", "📈",
                                                 "Parameter & compute scaling"))
            self.console.print(create_menu_option("3", "o", "Chinchilla Optimal", "🐭",
                                                 "Training efficiency analysis"))
            self.console.print(create_menu_option("4", "p", "Capability Comparison", "⭐",
                                                 "Reasoning, coding, math scores"))
            self.console.print(create_menu_option("5", "e", "Cost Efficiency", "💰",
                                                 "Value per dollar analysis"))
            self.console.print(create_menu_option("6", "s", "Summary Statistics", "📊",
                                                 "Dataset overview"))
            self.console.print()
            self.console.print(create_menu_option("0", "b", "Back", ICONS['back'],
                                                 "Return to main menu"))

            self.console.print()
            self.console.print(create_status_bar("LLM Analysis", "22 models from 2018-2024"))
            self.console.print()

            # Get choice
            num_keys = ["0", "1", "2", "3", "4", "5", "6"]
            letter_keys = ["b", "a", "c", "o", "p", "e", "s"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            key_map = {"b": "0", "a": "1", "c": "2", "o": "3", "p": "4", "e": "5", "s": "6"}

            choice = Prompt.ask(
                create_prompt_text("Your choice"),
                choices=valid_choices,
                default="1"
            )
            choice = normalize_choice(choice, key_map)

            if choice == "0":
                self.breadcrumbs.pop()
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
        table = create_styled_table(
            f"{ICONS['llm']} LLM Models Timeline",
            box_style=box.ROUNDED
        )

        table.add_column("Year", style=THEME['info'], justify="center", width=6)
        table.add_column("Name", style=THEME['highlight'], no_wrap=False, min_width=20)
        table.add_column("Organization", style=THEME['secondary'], width=15)
        table.add_column("Parameters (B)", justify="right", style=THEME['accent'])
        table.add_column("Context", justify="right", style=THEME['warning'])
        table.add_column("Open Source", justify="center", style=THEME['muted'], width=12)

        for model in self.llm_analyzer.models:
            # Format open source status with icons
            if model.open_source:
                open_src = f"[{THEME['success']}]✓ Yes[/{THEME['success']}]"
            else:
                open_src = f"[{THEME['muted']}]✗ No[/{THEME['muted']}]"

            table.add_row(
                str(model.year),
                model.name,
                model.organization,
                f"{model.parameters_billions:.1f}B",
                f"{model.context_window:,}",
                open_src,
            )

        self.console.print()
        self.console.print(table)
        self.console.print()
        self.console.print(create_status_bar(f"Showing {len(self.llm_analyzer.models)} models",
                                            "Press Enter to continue", include_help=False))
        Prompt.ask("", default="")

    def show_llm_cagr(self):
        """Display CAGR for LLM metrics."""
        results = self.llm_analyzer.calculate_all_cagrs()

        table = create_styled_table(
            f"{ICONS['stats']} LLM CAGR Analysis (2018-2024)",
            box_style=box.HEAVY
        )

        table.add_column("Metric", style=THEME['primary'], no_wrap=False, min_width=20)
        table.add_column("Start", justify="right", style=THEME['muted'])
        table.add_column("End", justify="right", style=THEME['highlight'])
        table.add_column("Growth", justify="right", style=THEME['warning'])
        table.add_column("CAGR", justify="right", style=THEME['success'], width=10)
        table.add_column("Alert", justify="center", width=8)

        extreme_cagrs = []
        for metric_name, result in results.items():
            # Format values based on size
            if result.start_value >= 1e15:
                start_str = f"{result.start_value:.2e}"
            else:
                start_str = f"{result.start_value:,.2f}"

            if result.end_value >= 1e15:
                end_str = f"{result.end_value:.2e}"
            else:
                end_str = f"{result.end_value:,.2f}"

            # Determine warning level
            warning = ""
            if result.cagr_percent > 500:
                warning = "[red]⚠⚠⚠[/red]"
                extreme_cagrs.append((metric_name, result.cagr_percent))
            elif result.cagr_percent > 200:
                warning = "[yellow]⚠⚠[/yellow]"
                extreme_cagrs.append((metric_name, result.cagr_percent))
            elif result.cagr_percent > 100:
                warning = "[yellow]⚠[/yellow]"

            table.add_row(
                metric_name.replace('_', ' ').title(),
                start_str,
                end_str,
                f"{result.growth_factor:.2f}x",
                f"{result.cagr_percent:.2f}%",
                warning,
            )

        self.console.print()
        self.console.print(table)
        self.console.print()

        # Add important warning for extreme CAGRs
        if extreme_cagrs:
            warning_details = "These growth rates are UNSUSTAINABLE:\n"
            for metric, cagr in extreme_cagrs:
                warning_details += f"  • {metric.replace('_', ' ').title()}: {cagr:.0f}% CAGR\n"
            warning_details += "\nThis represents initial LLM scaling phase (2018-2024)"

            Notify.warning(self.console, "⚠ CRITICAL REALITY CHECK", warning_details)

            self.console.print(
                "\n[bold]Why these rates cannot continue:[/bold]\n"
                "  1. [red]Training Compute:[/red] Already using largest GPU clusters (~100K GPUs)\n"
                "  2. [red]Economic Limits:[/red] Cost scaling faster than value delivered\n"
                "  3. [red]Data Limits:[/red] Running out of high-quality training data\n"
                "  4. [red]Energy Limits:[/red] Power consumption becoming prohibitive\n"
                "  5. [red]Diminishing Returns:[/red] Each doubling yields smaller capability gains\n"
            )
            self.console.print(
                "[yellow]Expected future: Growth will slow to 20-50% CAGR as models focus on "
                "efficiency, specialization, and inference optimization rather than pure scale.[/yellow]\n"
            )

        Prompt.ask("\nPress Enter to continue", default="")

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
        self.breadcrumbs.push("GPU Analysis")

        while True:
            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Menu header
            print_section_header(self.console, "GPU Analysis", ICONS['gpu'])
            self.console.print()

            # Menu options
            self.console.print(create_menu_option("1", "a", "View All GPUs", "📋",
                                                 "NVIDIA, AMD, Intel GPUs"))
            self.console.print(create_menu_option("2", "c", "Calculate CAGR", "📈",
                                                 "Performance growth rates"))
            self.console.print(create_menu_option("3", "m", "Manufacturer Comparison", "🏭",
                                                 "NVIDIA vs AMD vs Intel"))
            self.console.print(create_menu_option("4", "p", "Performance Evolution", "🚀",
                                                 "TFLOPS over time"))
            self.console.print(create_menu_option("5", "v", "Memory Evolution", "💾",
                                                 "VRAM capacity trends"))
            self.console.print(create_menu_option("6", "e", "Efficiency Trends", "⚡",
                                                 "TFLOPS per watt"))
            self.console.print(create_menu_option("7", "l", "Architectural Milestones", "🏛️",
                                                 "Key innovations"))
            self.console.print(create_menu_option("8", "s", "Summary Statistics", "📊",
                                                 "Dataset overview"))
            self.console.print()
            self.console.print(create_menu_option("0", "b", "Back", ICONS['back'],
                                                 "Return to main menu"))

            self.console.print()
            self.console.print(create_status_bar("GPU Analysis", "28 GPUs from 1999-2024"))
            self.console.print()

            # Get choice
            num_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
            letter_keys = ["b", "a", "c", "m", "p", "v", "e", "l", "s"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            key_map = {"b": "0", "a": "1", "c": "2", "m": "3", "p": "4", "v": "5", "e": "6", "l": "7", "s": "8"}

            choice = Prompt.ask(
                create_prompt_text("Your choice"),
                choices=valid_choices,
                default="1"
            )
            choice = normalize_choice(choice, key_map)

            if choice == "0":
                self.breadcrumbs.pop()
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
        table = create_styled_table(
            f"{ICONS['gpu']} GPU Models Timeline",
            box_style=box.ROUNDED
        )

        table.add_column("Year", style=THEME['info'], justify="center", width=6)
        table.add_column("Name", style=THEME['highlight'], no_wrap=False, min_width=30)
        table.add_column("Manufacturer", style=THEME['secondary'], width=10)
        table.add_column("TFLOPS", justify="right", style=THEME['warning'])
        table.add_column("VRAM", justify="right", style=THEME['accent'])
        table.add_column("TDP", justify="right", style=THEME['muted'])

        for gpu in self.gpu_analyzer.gpus:
            table.add_row(
                str(gpu.year),
                gpu.name[:35] if len(gpu.name) > 35 else gpu.name,
                gpu.manufacturer,
                f"{gpu.tflops_fp32:.1f}",
                f"{gpu.vram_mb // 1024}GB",
                f"{gpu.tdp_watts}W",
            )

        self.console.print()
        self.console.print(table)
        self.console.print()
        self.console.print(create_status_bar(f"Showing {len(self.gpu_analyzer.gpus)} GPUs",
                                            "Press Enter to continue", include_help=False))
        Prompt.ask("", default="")

    def show_gpu_cagr(self):
        """Display CAGR for GPU metrics."""
        results = self.gpu_analyzer.calculate_all_cagrs()

        table = create_styled_table(
            f"{ICONS['stats']} GPU CAGR Analysis (1999-2024)",
            box_style=box.HEAVY
        )

        table.add_column("Metric", style=THEME['primary'], no_wrap=False, min_width=20)
        table.add_column("Start", justify="right", style=THEME['muted'])
        table.add_column("End", justify="right", style=THEME['highlight'])
        table.add_column("Growth", justify="right", style=THEME['warning'])
        table.add_column("CAGR", justify="right", style=THEME['success'], width=10)

        for metric_name, result in results.items():
            # Format large numbers nicely
            if result.start_value >= 1000:
                start_str = f"{result.start_value/1000:.1f}K"
            else:
                start_str = f"{result.start_value:.1f}"

            if result.end_value >= 1000:
                end_str = f"{result.end_value/1000:.1f}K"
            else:
                end_str = f"{result.end_value:.1f}"

            table.add_row(
                metric_name.replace('_', ' ').title(),
                start_str,
                end_str,
                f"{result.growth_factor:,.0f}x",
                f"{result.cagr_percent:.1f}%",
            )

        self.console.print()
        self.console.print(table)
        self.console.print()
        Notify.info(self.console, "GPU Performance Growth",
                   "TFLOPS grew 51.3% CAGR over 25 years - sustainable hardware progress")
        Prompt.ask("\nPress Enter to continue", default="")

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
        self.breadcrumbs.push("Moore's Law")

        while True:
            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Menu header
            print_section_header(self.console, "Moore's Law Analysis", ICONS['moores_law'])
            self.console.print()

            # Menu options
            self.console.print(create_menu_option("1", "h", "Historical Adherence", "📜",
                                                 "Predicted vs actual transistors"))
            self.console.print(create_menu_option("2", "e", "Era Trends", "📊",
                                                 "5-year period analysis"))
            self.console.print(create_menu_option("3", "f", "Future Predictions", "🔮",
                                                 "Extrapolate transistor counts"))
            self.console.print(create_menu_option("4", "y", "Year Comparison", "🎯",
                                                 "Specific year analysis"))
            self.console.print()
            self.console.print(create_menu_option("0", "b", "Back", ICONS['back'],
                                                 "Return to main menu"))

            self.console.print()
            self.console.print(create_status_bar("Moore's Law", "2x transistors every ~2 years"))
            self.console.print()

            # Get choice
            num_keys = ["0", "1", "2", "3", "4"]
            letter_keys = ["b", "h", "e", "f", "y"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            key_map = {"b": "0", "h": "1", "e": "2", "f": "3", "y": "4"}

            choice = Prompt.ask(
                create_prompt_text("Your choice"),
                choices=valid_choices,
                default="1"
            )
            choice = normalize_choice(choice, key_map)

            if choice == "0":
                self.breadcrumbs.pop()
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

        # Cap at reasonable maximum
        if years_ahead > 50:
            self.console.print(
                f"[yellow]Warning: Predictions beyond 20 years are highly speculative. Capping at 50 years.[/yellow]"
            )
            years_ahead = min(years_ahead, 50)

        # Use latest system as base
        base_system = self.hw_analyzer.systems[-1]
        predictions = self.moores_law.predict_future(base_system, years_ahead)

        # Add explanatory header
        self.console.print(
            f"\n[cyan]Base System:[/cyan] {base_system.name} "
            f"({base_system.cpu_transistors:,} transistors, {base_system.cpu_process_nm}nm)\n"
        )

        table = Table(title=f"Moore's Law Predictions from {base_system.year}", box=box.ROUNDED)
        table.add_column("Year", style="cyan")
        table.add_column("Years Ahead", justify="right")
        table.add_column("Predicted Transistors", justify="right", style="yellow")
        table.add_column("Process (nm)", justify="right")
        table.add_column("Doublings", justify="right")
        table.add_column("Confidence", justify="center")

        for pred in predictions:
            # Format transistor count - use scientific notation if very large
            transistor_count = pred['predicted_transistors']
            if transistor_count >= 1e15:
                transistor_str = f"{transistor_count:.2e}"
            else:
                transistor_str = f"{transistor_count:,}"

            # Color code based on confidence
            confidence_colors = {
                'high': 'green',
                'medium': 'yellow',
                'low': 'orange1',
                'very_low': 'red'
            }
            confidence_color = confidence_colors.get(pred['confidence'], 'white')
            confidence_icon = {
                'high': '●●●',
                'medium': '●●○',
                'low': '●○○',
                'very_low': '○○○'
            }

            # Add warning indicators
            process_str = f"{pred['predicted_process_nm']:.1f}"
            if pred['warning'] == 'physical_limit_reached':
                process_str = f"[red]{process_str}*[/red]"

            table.add_row(
                str(pred['year']),
                str(pred['years_from_base']),
                transistor_str,
                process_str,
                f"{pred['doublings_from_base']:.2f}",
                f"[{confidence_color}]{confidence_icon.get(pred['confidence'], '???')}[/{confidence_color}]",
            )

        self.console.print(table)

        # Print warnings and notes
        self.console.print("\n[bold]Legend:[/bold]")
        self.console.print("  Confidence: [green]●●●[/green] High  [yellow]●●○[/yellow] Medium  [orange1]●○○[/orange1] Low  [red]○○○[/red] Very Low")
        self.console.print("  [red]*[/red] = Physical/practical limit reached\n")

        # Show important notes
        has_warnings = any(p['note'] for p in predictions)
        if has_warnings:
            self.console.print("[bold yellow]Important Notes:[/bold yellow]")
            notes_shown = set()
            for pred in predictions:
                if pred['note'] and pred['note'] not in notes_shown:
                    self.console.print(f"  • {pred['note']}")
                    notes_shown.add(pred['note'])
            self.console.print()

        # Reality check message for long predictions
        if years_ahead > 20:
            self.console.print(
                "[bold red]Reality Check:[/bold red] Predictions beyond 2035 assume major paradigm shifts "
                "(quantum computing, photonic chips, 3D stacking, neuromorphic hardware, etc.). "
                "Traditional transistor-based Moore's Law is expected to end around 2025-2030.\n"
            )

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
        self.breadcrumbs.push("Export Data")

        while True:
            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Menu header
            print_section_header(self.console, "Export Data", ICONS['export'])
            self.console.print()

            # Menu options
            self.console.print(create_menu_option("1", "h", "Export Hardware Data", "💻",
                                                 "Systems data to file"))
            self.console.print(create_menu_option("2", "l", "Export LLM Data", "🤖",
                                                 "Models data to file"))
            self.console.print(create_menu_option("3", "g", "Export GPU Data", "🖥️",
                                                 "GPU data to file"))
            self.console.print(create_menu_option("4", "c", "Export CAGR Analysis", "📈",
                                                 "Growth rate analysis"))
            self.console.print(create_menu_option("5", "r", "Export Complete Report", "📄",
                                                 "Full analysis report"))
            self.console.print()
            self.console.print(create_menu_option("0", "b", "Back", ICONS['back'],
                                                 "Return to main menu"))

            self.console.print()
            self.console.print(create_status_bar("Export", "JSON, CSV, Markdown, Text formats available"))
            self.console.print()

            # Get choice
            num_keys = ["0", "1", "2", "3", "4", "5"]
            letter_keys = ["b", "h", "l", "g", "c", "r"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            key_map = {"b": "0", "h": "1", "l": "2", "g": "3", "c": "4", "r": "5"}

            choice = Prompt.ask(
                create_prompt_text("Your choice"),
                choices=valid_choices,
                default="1"
            )
            choice = normalize_choice(choice, key_map)

            if choice == "0":
                self.breadcrumbs.pop()
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
            create_prompt_text("Select format"),
            choices=["json", "csv", "markdown", "text"],
            default="json"
        )

        data = self.hw_analyzer.to_dict()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(f"[cyan]Exporting hardware data as {format_choice}...", total=None)

            try:
                if format_choice == "json":
                    path = self.exporter.export_json(data, "hardware_systems.json")
                elif format_choice == "csv":
                    path = self.exporter.export_csv(data, "hardware_systems.csv")
                elif format_choice == "markdown":
                    path = self.exporter.export_markdown(data, "hardware_systems.md", "Hardware Systems")
                elif format_choice == "text":
                    path = self.exporter.export_text(data, "hardware_systems.txt", "Hardware Systems")

                progress.update(task, completed=True)

                Notify.success(self.console, "Export Complete!", f"File saved to: {path}")
            except Exception as e:
                progress.update(task, completed=True)
                Notify.error(self.console, "Export Failed", str(e))

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
        self.breadcrumbs.push("Visualizations")

        while True:
            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Menu header
            print_section_header(self.console, "Generate Visualizations", ICONS['visualize'])
            self.console.print()

            # Hardware section
            self.console.print(Text("  Hardware Charts", style=f"bold {THEME['primary']}"))
            self.console.print(create_menu_option("1", "h", "Transistor Evolution", "📈",
                                                 "Log scale hardware trends"))
            self.console.print(create_menu_option("2", "m", "Moore's Law Comparison", "🎯",
                                                 "Predicted vs actual"))
            self.console.print(create_menu_option("3", "g", "Growth Factors", "📊",
                                                 "Bar chart of growth rates"))
            self.console.print()

            # LLM section
            self.console.print(Text("  LLM Charts", style=f"bold {THEME['primary']}"))
            self.console.print(create_menu_option("4", "p", "Parameter Scaling", "🤖",
                                                 "Model size over time"))
            self.console.print(create_menu_option("5", "w", "Context Window Evolution", "📏",
                                                 "Context length trends"))
            self.console.print(create_menu_option("6", "r", "Capability Radar", "⭐",
                                                 "Multi-dimensional scores"))
            self.console.print()

            # GPU section
            self.console.print(Text("  GPU Charts", style=f"bold {THEME['primary']}"))
            self.console.print(create_menu_option("7", "a", "Performance Evolution", "🚀",
                                                 "TFLOPS over time"))
            self.console.print(create_menu_option("8", "v", "Memory Evolution", "💾",
                                                 "VRAM capacity trends"))
            self.console.print(create_menu_option("9", "e", "Efficiency Trends", "⚡",
                                                 "TFLOPS per watt"))
            self.console.print(create_menu_option("10", "f", "Manufacturer Comparison", "🏭",
                                                 "NVIDIA vs AMD vs Intel"))
            self.console.print(create_menu_option("11", "x", "Price vs Performance", "💰",
                                                 "Value analysis"))
            self.console.print()

            # Analysis charts
            self.console.print(Text("  Analysis Charts", style=f"bold {THEME['primary']}"))
            self.console.print(create_menu_option("12", "c", "CAGR Heatmap", "🌡️",
                                                 "Growth rate visualization"))
            self.console.print()

            self.console.print(create_menu_option("0", "b", "Back", ICONS['back'],
                                                 "Return to main menu"))

            self.console.print()
            self.console.print(create_status_bar("Visualizations", "Charts saved to output/ directory"))
            self.console.print()

            # Get choice
            num_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
            letter_keys = ["b", "h", "m", "g", "p", "w", "r", "a", "v", "e", "f", "x", "c"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            key_map = {
                "b": "0", "h": "1", "m": "2", "g": "3", "p": "4", "w": "5", "r": "6",
                "a": "7", "v": "8", "e": "9", "f": "10", "x": "11", "c": "12"
            }

            choice = Prompt.ask(
                create_prompt_text("Your choice"),
                choices=valid_choices,
                default="1"
            )
            choice = normalize_choice(choice, key_map)

            if choice == "0":
                self.breadcrumbs.pop()
                break
            elif choice == "1":
                self.plot_hardware_evolution()
            elif choice == "2":
                self.plot_moores_law_comparison()
            elif choice == "3":
                self.plot_growth_factors()
            elif choice == "4":
                self.plot_llm_parameters()
            elif choice == "5":
                self.plot_context_window()
            elif choice == "6":
                self.plot_llm_capabilities()
            elif choice == "7":
                self.plot_gpu_performance()
            elif choice == "8":
                self.plot_gpu_memory()
            elif choice == "9":
                self.plot_gpu_efficiency()
            elif choice == "10":
                self.plot_gpu_manufacturer_comp()
            elif choice == "11":
                self.plot_gpu_price_performance()
            elif choice == "12":
                self.plot_cagr_heatmap()

    def plot_hardware_evolution(self):
        """Plot hardware metric evolution."""
        metric = Prompt.ask(
            create_prompt_text("Select metric to plot"),
            choices=["cpu_transistors", "cpu_clock_mhz", "ram_mb", "storage_mb", "performance_mips"],
            default="cpu_transistors"
        )

        output_path = Path("output") / f"hardware_{metric}_evolution.png"
        output_path.parent.mkdir(exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(f"[cyan]📈 Generating {metric} plot...", total=None)

            try:
                self.plotter.plot_hardware_evolution(
                    self.hw_analyzer.systems,
                    metric,
                    output_path,
                    log_scale=True
                )
                progress.update(task, completed=True)
                Notify.success(self.console, "Plot Generated!", f"Saved to: {output_path}")
            except Exception as e:
                progress.update(task, completed=True)
                Notify.error(self.console, "Plot Failed", str(e))

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

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                     console=self.console) as progress:
            task = progress.add_task(f"[cyan]🎯 Generating Moore's Law comparison...", total=None)
            try:
                self.plotter.plot_moores_law_comparison(self.hw_analyzer.systems, predictions, output_path)
                progress.update(task, completed=True)
                Notify.success(self.console, "Plot Generated!", f"Saved to: {output_path}")
            except Exception as e:
                progress.update(task, completed=True)
                Notify.error(self.console, "Plot Failed", str(e))

    def plot_cagr_heatmap(self):
        """Plot CAGR heatmap."""
        results = self.hw_analyzer.calculate_all_cagrs()
        cagr_data = {k: v.cagr_percent for k, v in results.items()}

        output_path = Path("output") / "cagr_heatmap.png"
        output_path.parent.mkdir(exist_ok=True)

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                     console=self.console) as progress:
            task = progress.add_task(f"[cyan]🌡️ Generating CAGR heatmap...", total=None)
            try:
                self.plotter.plot_cagr_heatmap(cagr_data, output_path)
                progress.update(task, completed=True)
                Notify.success(self.console, "Plot Generated!", f"Saved to: {output_path}")
            except Exception as e:
                progress.update(task, completed=True)
                Notify.error(self.console, "Plot Failed", str(e))

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
        self.breadcrumbs.push("Compare Evolution")

        # Show breadcrumbs
        self.console.print()
        self.console.print(self.breadcrumbs.render())
        self.console.print()

        # Header
        print_section_header(self.console, "Hardware vs LLM vs GPU Evolution", ICONS['compare'])
        self.console.print()

        hw_cagr = self.hw_analyzer.calculate_all_cagrs()
        llm_cagr = self.llm_analyzer.calculate_all_cagrs()
        gpu_cagr = self.gpu_analyzer.calculate_all_cagrs()

        # Hardware summary
        self.console.print(Text(f"  {ICONS['hardware']} Hardware Evolution (1965-2024)", style=f"bold {THEME['primary']}"))
        hw_table = create_styled_table("", box_style=box.SIMPLE, show_header=False)
        hw_table.add_column("Metric", style=THEME['secondary'])
        hw_table.add_column("CAGR %", justify="right", style=THEME['success'])

        for metric, result in hw_cagr.items():
            hw_table.add_row(
                metric.replace('_', ' ').title(),
                f"{result.cagr_percent:.2f}%"
            )

        self.console.print(hw_table)
        self.console.print()

        # GPU summary
        self.console.print(Text(f"  {ICONS['gpu']} GPU Evolution (1999-2024)", style=f"bold {THEME['primary']}"))
        gpu_table = create_styled_table("", box_style=box.SIMPLE, show_header=False)
        gpu_table.add_column("Metric", style=THEME['secondary'])
        gpu_table.add_column("CAGR %", justify="right", style=THEME['success'])

        for metric, result in gpu_cagr.items():
            gpu_table.add_row(
                metric.replace('_', ' ').title(),
                f"{result.cagr_percent:.2f}%"
            )

        self.console.print(gpu_table)
        self.console.print()

        # LLM summary
        self.console.print(Text(f"  {ICONS['llm']} LLM Evolution (2018-2024)", style=f"bold {THEME['primary']}"))
        llm_table = create_styled_table("", box_style=box.SIMPLE, show_header=False)
        llm_table.add_column("Metric", style=THEME['secondary'])
        llm_table.add_column("CAGR %", justify="right", style=THEME['warning'])

        for metric, result in llm_cagr.items():
            llm_table.add_row(
                metric.replace('_', ' ').title(),
                f"{result.cagr_percent:.2f}%"
            )

        self.console.print(llm_table)
        self.console.print()

        # Key insights
        llm_vs_cpu_ratio = llm_cagr['parameters_billions'].cagr_percent / hw_cagr['cpu_transistors'].cagr_percent
        gpu_vs_cpu_ratio = gpu_cagr['tflops_fp32'].cagr_percent / hw_cagr['cpu_transistors'].cagr_percent

        panel = Panel(
            "[cyan]Key Insights:[/cyan]\n"
            f"• CPU transistors grew {hw_cagr['cpu_transistors'].growth_factor:.1f}x over [bold]59 years[/bold] ({hw_cagr['cpu_transistors'].cagr_percent:.1f}% CAGR)\n"
            f"• GPU TFLOPS grew {gpu_cagr['tflops_fp32'].growth_factor:.1f}x over [bold]25 years[/bold] ({gpu_cagr['tflops_fp32'].cagr_percent:.1f}% CAGR)\n"
            f"• GPU VRAM grew {gpu_cagr['vram_mb'].growth_factor:.0f}x over [bold]25 years[/bold] ({gpu_cagr['vram_mb'].cagr_percent:.1f}% CAGR)\n"
            f"• LLM parameters grew {llm_cagr['parameters_billions'].growth_factor:.1f}x in just [bold]6 years[/bold] ({llm_cagr['parameters_billions'].cagr_percent:.1f}% CAGR)\n"
            f"  [yellow]⚠[/yellow] LLM CAGR appears {llm_vs_cpu_ratio:.1f}x faster than CPU scaling, [italic]but this is temporary[/italic]\n"
            f"• GPU performance CAGR is {gpu_vs_cpu_ratio:.1f}x CPU transistor CAGR (more sustainable)",
            title="Comparison Summary",
            border_style="yellow",
        )
        self.console.print(panel)

        # Add important context about the comparison
        self.console.print(
            "\n[bold yellow]⚠ Important Context:[/bold yellow]\n"
            "[yellow]The LLM scaling rate is NOT directly comparable to hardware trends because:[/yellow]\n"
            "  1. [cyan]Different time periods:[/cyan] 6 years (LLM) vs 59 years (CPU) vs 25 years (GPU)\n"
            "  2. [cyan]Temporary phase:[/cyan] LLM scaling represents initial research phase, not sustainable trend\n"
            "  3. [cyan]Different constraints:[/cyan] Hardware limited by physics; LLMs limited by data, compute, and economics\n"
            "  4. [cyan]Expected slowdown:[/cyan] LLM scaling will normalize to 20-50% CAGR as field matures\n"
        )

        self.console.print()
        self.console.print(create_status_bar("Comparison Complete", "Press Enter to return"))
        Prompt.ask("", default="")

        self.breadcrumbs.pop()

    def cloud_cost_analysis_menu(self):
        """Cloud cost analysis submenu."""
        self.breadcrumbs.push("Cloud Cost Analysis")

        while True:
            # Show breadcrumbs
            self.console.print()
            self.console.print(self.breadcrumbs.render())
            self.console.print()

            # Menu header
            print_section_header(self.console, "Cloud Cost Analysis", ICONS['cloud'])
            self.console.print()

            # Menu options
            self.console.print(create_menu_option("1", "a", "View All Instances", "📋",
                                                 "AWS, Azure, GCP inventory"))
            self.console.print(create_menu_option("2", "t", "Compare Training Costs", "🎓",
                                                 "Best providers for training"))
            self.console.print(create_menu_option("3", "i", "Compare Inference Costs", "🚀",
                                                 "Best providers for serving"))
            self.console.print(create_menu_option("4", "r", "Cost Efficiency Ranking", "🏆",
                                                 "TFLOPS per dollar"))
            self.console.print(create_menu_option("5", "s", "Spot Savings Analysis", "💸",
                                                 "On-demand vs spot pricing"))
            self.console.print(create_menu_option("6", "e", "Estimate Training Cost", "🧮",
                                                 "Calculate LLM training costs"))
            self.console.print(create_menu_option("7", "p", "GPU Price Evolution", "📈",
                                                 "Historical pricing trends"))
            self.console.print(create_menu_option("8", "v", "Provider Statistics", "📊",
                                                 "AWS vs Azure vs GCP"))
            self.console.print(create_menu_option("9", "c", "Compare Instances", "⚖️",
                                                 "Side-by-side comparison"))
            self.console.print()
            self.console.print(create_menu_option("0", "b", "Back", ICONS['back'],
                                                 "Return to main menu"))

            self.console.print()
            self.console.print(create_status_bar("Cloud Costs", "17 instances across 3 providers"))
            self.console.print()

            # Get choice
            num_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            letter_keys = ["b", "a", "t", "i", "r", "s", "e", "p", "v", "c"]
            valid_choices = build_choice_validator(num_keys, letter_keys)

            key_map = {"b": "0", "a": "1", "t": "2", "i": "3", "r": "4", "s": "5", "e": "6", "p": "7", "v": "8", "c": "9"}

            choice = Prompt.ask(
                create_prompt_text("Your choice"),
                choices=valid_choices,
                default="1"
            )
            choice = normalize_choice(choice, key_map)

            if choice == "0":
                self.breadcrumbs.pop()
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

        try:
            training_hours = IntPrompt.ask(
                "Enter training time in hours",
                default=100
            )
            use_spot = Confirm.ask("Use spot pricing?", default=True)

            comparison = self.cloud_cost_analyzer.compare_providers_for_training(
                training_hours=training_hours,
                use_spot=use_spot
            )

            if not comparison:
                self.console.print("\n[yellow]No training instances found for the selected pricing model.[/yellow]")
                if use_spot:
                    self.console.print("[yellow]Try using on-demand pricing instead.[/yellow]")
                Prompt.ask("\nPress Enter to continue", default="")
                return

        except ValueError as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
            Prompt.ask("\nPress Enter to continue", default="")
            return

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

        try:
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

            if not comparison:
                self.console.print("\n[yellow]No inference instances found.[/yellow]")
                Prompt.ask("\nPress Enter to continue", default="")
                return

        except ValueError as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
            Prompt.ask("\nPress Enter to continue", default="")
            return

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

        try:
            params_billions = IntPrompt.ask("Enter model size in billions of parameters", default=7)
            tokens_billions = IntPrompt.ask("Enter training tokens in billions", default=1000)
            use_spot = Confirm.ask("Use spot pricing?", default=True)

            estimate = self.cloud_cost_analyzer.estimate_llm_training_cost(
                parameters_billions=params_billions,
                training_tokens_billions=tokens_billions,
                use_spot=use_spot
            )

        except ValueError as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
            Prompt.ask("\nPress Enter to continue", default="")
            return

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
