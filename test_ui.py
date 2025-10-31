#!/usr/bin/env python3
"""Quick UI preview test script."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from llm_evolution.ui_components import (
    THEME, ICONS,
    create_banner, create_menu_option,
    create_status_bar, print_section_header,
    BreadcrumbNav, Notify
)

def main():
    console = Console()

    # Show banner
    console.print(create_banner())

    # Show breadcrumbs
    breadcrumbs = BreadcrumbNav()
    console.print()
    console.print(breadcrumbs.render())
    console.print()

    # Show main menu header
    print_section_header(console, "Main Menu", "🏠")
    console.print()

    # Show menu options
    console.print(create_menu_option("1", "h", "Hardware Analysis", ICONS['hardware'],
                                     "CPU, RAM, storage evolution"))
    console.print(create_menu_option("2", "l", "LLM Analysis", ICONS['llm'],
                                     "Model parameters, capabilities"))
    console.print(create_menu_option("3", "g", "GPU Analysis", ICONS['gpu'],
                                     "Performance, efficiency trends"))
    console.print(create_menu_option("4", "m", "Moore's Law Analysis", ICONS['moores_law'],
                                     "Historical adherence & predictions"))
    console.print(create_menu_option("5", "c", "Compare Evolution", ICONS['compare'],
                                     "Hardware vs LLM vs GPU"))
    console.print(create_menu_option("6", "e", "Export Data", ICONS['export'],
                                     "JSON, CSV, Markdown formats"))
    console.print(create_menu_option("7", "v", "Generate Visualizations", ICONS['visualize'],
                                     "Charts and plots"))
    console.print(create_menu_option("8", "k", "Cloud Cost Analysis", ICONS['cloud'],
                                     "AWS, Azure, GCP pricing"))
    console.print()
    console.print(create_menu_option("0", "q", "Exit", ICONS['exit'],
                                     "Quit application"))

    # Show status bar
    console.print()
    console.print(create_status_bar("Ready", "Type a number or letter shortcut"))
    console.print()

    # Show notifications
    console.print("\n[bold]Notification Examples:[/bold]\n")
    Notify.success(console, "Operation completed!", "All systems operational")
    console.print()
    Notify.info(console, "Did you know?", "You can use letter shortcuts for faster navigation")
    console.print()
    Notify.warning(console, "High memory usage detected", "Consider closing other applications")
    console.print()
    Notify.error(console, "Connection failed", "Unable to reach remote server")

    console.print(f"\n\n[{THEME['success']}]✓[/{THEME['success']}] UI Components Preview Complete!")
    console.print(f"[{THEME['muted']}]Terminal width: {console.width} columns[/{THEME['muted']}]")

if __name__ == "__main__":
    main()
