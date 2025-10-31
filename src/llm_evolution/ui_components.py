"""
UI Components for beautiful CLI interface using Rich's built-in responsiveness.

This module provides styled UI components that leverage Rich's automatic
terminal width handling and responsive design capabilities.
"""

from typing import Optional, List, Tuple
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich import box
from rich.align import Align


# Color theme - consistent palette across the application
THEME = {
    'primary': 'bright_cyan',
    'secondary': 'bright_blue',
    'accent': 'bright_magenta',
    'success': 'bright_green',
    'warning': 'bright_yellow',
    'error': 'bright_red',
    'info': 'cyan',
    'muted': 'dim white',
    'highlight': 'bold bright_white'
}

# Menu icons for visual navigation
ICONS = {
    'hardware': '💻',
    'llm': '🤖',
    'gpu': '🖥️',
    'moores_law': '📈',
    'compare': '⚖️',
    'export': '📤',
    'visualize': '📊',
    'cloud': '☁️',
    'exit': '🚪',
    'back': '◀️',
    'settings': '⚙️',
    'help': '❓',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'loading': '⏳',
    'rocket': '🚀',
    'stats': '📉',
    'dollar': '💰',
    'checkmark': '✓',
    'arrow': '→'
}


def create_banner() -> Panel:
    """Create application banner - Rich Panel handles width automatically."""
    banner = Text()

    # ASCII art that scales with terminal
    banner.append("\n⚡ ", style=THEME['accent'])
    banner.append("COMPUTING & LLM EVOLUTION ANALYZER", style=f"bold {THEME['primary']}")
    banner.append(" ⚡\n", style=THEME['accent'])

    banner.append("\nVersion 2.1.0", style=THEME['muted'])
    banner.append("\n\nAnalyze hardware, LLM evolution, and cloud costs",
                 style=f"italic {THEME['info']}")
    banner.append("\n\n📊 Hardware  •  🖥️ GPU  •  🤖 LLM  •  ☁️ Cloud\n",
                 style=THEME['secondary'])

    return Panel(
        Align.center(banner),
        box=box.DOUBLE,
        border_style=THEME['primary'],
        padding=(1, 2)
    )


def create_menu_option(num_key: str, letter_key: str, label: str,
                       icon: str, description: str = "") -> Text:
    """
    Create a styled menu option with both number and letter shortcuts.

    Args:
        num_key: Number shortcut (e.g., "1")
        letter_key: Letter shortcut (e.g., "h")
        label: Option label
        icon: Emoji icon
        description: Optional description text
    """
    option = Text()

    # Keys in brackets with both number and letter
    option.append("  [", style=THEME['muted'])
    option.append(num_key, style=f"bold {THEME['accent']}")
    option.append("/", style=THEME['muted'])
    option.append(letter_key, style=f"bold {THEME['accent']}")
    option.append("]", style=THEME['muted'])

    # Icon and label
    option.append(f"  {icon}  ", style=THEME['secondary'])
    option.append(label, style=f"bold {THEME['highlight']}")

    # Description on same line if short enough, otherwise indent
    if description:
        if len(label) < 20:
            option.append(f"  →  {description}", style=THEME['muted'])
        else:
            option.append(f"\n      {description}", style=THEME['muted'])

    return option


def create_prompt_text(prompt_label: str = "Choose an option") -> str:
    """Create a styled prompt text for input."""
    return f"[{THEME['accent']}]▸[/{THEME['accent']}] [{THEME['highlight']}]{prompt_label}[/{THEME['highlight']}]"


def build_choice_validator(num_keys: list, letter_keys: list):
    """
    Build a validator that accepts both number and letter shortcuts.

    Args:
        num_keys: List of valid number keys
        letter_keys: List of valid letter keys

    Returns:
        A list of all valid choices (combined)
    """
    return num_keys + letter_keys


def normalize_choice(choice: str, key_map: dict) -> str:
    """
    Normalize user choice to a standard key.

    Args:
        choice: User input
        key_map: Dictionary mapping letter keys to number keys

    Returns:
        Normalized number key
    """
    choice_lower = choice.lower()
    return key_map.get(choice_lower, choice)


class BreadcrumbNav:
    """Manages breadcrumb navigation trail."""

    def __init__(self):
        """Initialize breadcrumb navigation."""
        self.trail = ["Home"]

    def push(self, name: str):
        """Add breadcrumb level."""
        self.trail.append(name)

    def pop(self):
        """Remove last breadcrumb level."""
        if len(self.trail) > 1:
            self.trail.pop()

    def reset(self):
        """Reset to home."""
        self.trail = ["Home"]

    def render(self) -> Text:
        """Render breadcrumb trail."""
        crumb = Text()
        for i, item in enumerate(self.trail):
            if i > 0:
                crumb.append(" → ", style=THEME['muted'])
            crumb.append(item, style=THEME['info'] if i == len(self.trail) - 1 else THEME['muted'])
        return crumb


class Notify:
    """Static notification methods for user feedback."""

    @staticmethod
    def success(console: Console, message: str, details: Optional[str] = None):
        """Show success notification."""
        text = Text()
        text.append("✅ ", style=THEME['success'])
        text.append(message, style=f"bold {THEME['success']}")
        if details:
            text.append(f"\n{details}", style=THEME['muted'])

        console.print(Panel(text, box=box.ROUNDED, border_style=THEME['success'],
                           padding=(0, 1)))

    @staticmethod
    def error(console: Console, message: str, details: Optional[str] = None):
        """Show error notification."""
        text = Text()
        text.append("❌ ", style=THEME['error'])
        text.append(message, style=f"bold {THEME['error']}")
        if details:
            text.append(f"\n{details}", style=THEME['muted'])

        console.print(Panel(text, box=box.ROUNDED, border_style=THEME['error'],
                           padding=(0, 1)))

    @staticmethod
    def warning(console: Console, message: str, details: Optional[str] = None):
        """Show warning notification."""
        text = Text()
        text.append("⚠️  ", style=THEME['warning'])
        text.append(message, style=f"bold {THEME['warning']}")
        if details:
            text.append(f"\n{details}", style=THEME['muted'])

        console.print(Panel(text, box=box.ROUNDED, border_style=THEME['warning'],
                           padding=(0, 1)))

    @staticmethod
    def info(console: Console, message: str, details: Optional[str] = None):
        """Show info notification."""
        text = Text()
        text.append("ℹ️  ", style=THEME['info'])
        text.append(message, style=f"bold {THEME['info']}")
        if details:
            text.append(f"\n{details}", style=THEME['muted'])

        console.print(Panel(text, box=box.ROUNDED, border_style=THEME['info'],
                           padding=(0, 1)))


def create_styled_table(title: str,
                       box_style: box.Box = box.ROUNDED,
                       show_header: bool = True,
                       row_styles: Optional[List[str]] = None) -> Table:
    """
    Create a styled table that's automatically responsive.

    Rich Table handles terminal width automatically - just set expand=True
    and it will adapt to available space.
    """
    if row_styles is None:
        # Alternating row colors for better readability
        row_styles = [THEME['muted'], ""]

    return Table(
        title=title,
        title_style=f"bold {THEME['primary']}",
        box=box_style,
        show_header=show_header,
        row_styles=row_styles,
        expand=True,  # Let Rich handle the width
        padding=(0, 1)
    )


def create_dashboard_panel(title: str, content: Text, icon: str = "📊") -> Panel:
    """Create a dashboard info panel."""
    titled_content = Text()
    titled_content.append(f"{icon} ", style=THEME['accent'])
    titled_content.append(title, style=f"bold {THEME['secondary']}")
    titled_content.append("\n\n")
    titled_content.append(content)

    return Panel(
        titled_content,
        box=box.ROUNDED,
        border_style=THEME['info'],
        padding=(1, 2)
    )


def create_status_bar(message: str, tip: Optional[str] = None, include_help: bool = True) -> Text:
    """Create bottom status bar with tips."""
    status = Text()
    status.append("▎", style=THEME['accent'])
    status.append(f" {message}", style=THEME['info'])

    if tip:
        status.append(" │ ", style=THEME['muted'])
        status.append(f"💡 {tip}", style=THEME['muted'])

    if include_help:
        status.append(" │ ", style=THEME['muted'])
        status.append("? for help", style=f"dim {THEME['accent']}")

    return status


def create_divider(char: str = "─", style: Optional[str] = None) -> Text:
    """Create a visual divider - Rich will expand to terminal width."""
    if style is None:
        style = THEME['muted']
    # Rich will handle expanding this to full width
    return Text(char * 80, style=style)


def create_help_screen() -> Panel:
    """Create comprehensive help screen."""
    from rich.columns import Columns

    # Navigation section
    nav_help = Text()
    nav_help.append("Navigation\n", style=f"bold {THEME['primary']}")
    nav_help.append("─────────────\n", style=THEME['muted'])
    nav_help.append("Numbers ", style=f"bold {THEME['accent']}")
    nav_help.append("1-9 for options\n", style=THEME['info'])
    nav_help.append("Letters ", style=f"bold {THEME['accent']}")
    nav_help.append("h,l,g,m,etc.\n", style=THEME['info'])
    nav_help.append("0 or b ", style=f"bold {THEME['accent']}")
    nav_help.append("Go back\n", style=THEME['info'])
    nav_help.append("q ", style=f"bold {THEME['accent']}")
    nav_help.append("Quit from main\n", style=THEME['info'])
    nav_help.append("? ", style=f"bold {THEME['accent']}")
    nav_help.append("Show this help\n", style=THEME['info'])

    # Shortcuts section
    shortcut_help = Text()
    shortcut_help.append("Main Menu Shortcuts\n", style=f"bold {THEME['primary']}")
    shortcut_help.append("──────────────────\n", style=THEME['muted'])
    shortcut_help.append("h ", style=f"bold {THEME['accent']}")
    shortcut_help.append("Hardware Analysis\n", style=THEME['info'])
    shortcut_help.append("l ", style=f"bold {THEME['accent']}")
    shortcut_help.append("LLM Analysis\n", style=THEME['info'])
    shortcut_help.append("g ", style=f"bold {THEME['accent']}")
    shortcut_help.append("GPU Analysis\n", style=THEME['info'])
    shortcut_help.append("m ", style=f"bold {THEME['accent']}")
    shortcut_help.append("Moore's Law\n", style=THEME['info'])
    shortcut_help.append("c ", style=f"bold {THEME['accent']}")
    shortcut_help.append("Compare Evolution\n", style=THEME['info'])
    shortcut_help.append("e ", style=f"bold {THEME['accent']}")
    shortcut_help.append("Export Data\n", style=THEME['info'])
    shortcut_help.append("v ", style=f"bold {THEME['accent']}")
    shortcut_help.append("Visualizations\n", style=THEME['info'])
    shortcut_help.append("k ", style=f"bold {THEME['accent']}")
    shortcut_help.append("Cloud Costs\n", style=THEME['info'])

    # Features section
    feature_help = Text()
    feature_help.append("Features\n", style=f"bold {THEME['primary']}")
    feature_help.append("────────\n", style=THEME['muted'])
    feature_help.append("Breadcrumbs ", style=f"bold {THEME['accent']}")
    feature_help.append("Show location\n", style=THEME['info'])
    feature_help.append("Status Bar ", style=f"bold {THEME['accent']}")
    feature_help.append("Context tips\n", style=THEME['info'])
    feature_help.append("Icons ", style=f"bold {THEME['accent']}")
    feature_help.append("Visual guides\n", style=THEME['info'])
    feature_help.append("Descriptions ", style=f"bold {THEME['accent']}")
    feature_help.append("Explain options\n", style=THEME['info'])
    feature_help.append("Case-insensitive ", style=f"bold {THEME['accent']}")
    feature_help.append("H = h\n", style=THEME['info'])

    help_layout = Columns([nav_help, shortcut_help, feature_help], equal=True, expand=True)

    tips = Text()
    tips.append("\n💡 Tips: ", style=f"bold {THEME['warning']}")
    tips.append("Use letter shortcuts for faster navigation • ", style=THEME['muted'])
    tips.append("Press Enter to use default • ", style=THEME['muted'])
    tips.append("Follow breadcrumbs to know where you are", style=THEME['muted'])

    from rich.console import Group
    help_group = Group(help_layout, tips)

    return Panel(
        help_group,
        title=f"{ICONS['help']} Help & Keyboard Shortcuts",
        title_align="left",
        box=box.DOUBLE,
        border_style=THEME['info'],
        padding=(1, 2)
    )


def create_help_text() -> Panel:
    """Create help/shortcuts panel (compact version)."""
    help_content = Text()
    help_content.append("Keyboard Shortcuts\n\n", style=f"bold {THEME['secondary']}")
    help_content.append("↑/↓  ", style=THEME['accent'])
    help_content.append("Navigate • ", style=THEME['muted'])
    help_content.append("Enter ", style=THEME['accent'])
    help_content.append("Select • ", style=THEME['muted'])
    help_content.append("0 ", style=THEME['accent'])
    help_content.append("Back/Exit • ", style=THEME['muted'])
    help_content.append("? ", style=THEME['accent'])
    help_content.append("Help • ", style=THEME['muted'])
    help_content.append("Ctrl+C ", style=THEME['accent'])
    help_content.append("Quit", style=THEME['muted'])

    return Panel(
        help_content,
        title="❓ Help",
        title_align="left",
        box=box.ROUNDED,
        border_style=THEME['info'],
        padding=(0, 2)
    )


def clear_screen(console: Console):
    """Clear the screen with a smooth transition."""
    console.clear()


def show_help(console: Console):
    """Display the global help screen."""
    console.print()
    console.print(create_help_screen())
    console.print()
    console.print(create_status_bar("Help", "Press Enter to return"))
    from rich.prompt import Prompt
    Prompt.ask("", default="")


def print_section_header(console: Console, text: str, icon: str = ""):
    """Print a styled section header."""
    header = Text()
    if icon:
        header.append(f"{icon} ", style=THEME['accent'])
    header.append(text, style=f"bold {THEME['primary']}")

    console.print()
    console.print(header)
    console.print(create_divider())
