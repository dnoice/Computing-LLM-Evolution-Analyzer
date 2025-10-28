"""Data export functionality for various formats."""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import pandas as pd
from tabulate import tabulate


class Exporter:
    """Exporter for analysis results in multiple formats."""

    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize exporter.

        Args:
            output_dir: Directory for output files
        """
        if output_dir is None:
            output_dir = Path("output")

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_json(
        self,
        data: Any,
        filename: str,
        pretty: bool = True,
    ) -> Path:
        """Export data to JSON format.

        Args:
            data: Data to export
            filename: Output filename
            pretty: Pretty print JSON

        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            if pretty:
                json.dump(data, f, indent=2, default=str)
            else:
                json.dump(data, f, default=str)

        return output_path

    def export_csv(
        self,
        data: List[Dict[str, Any]],
        filename: str,
    ) -> Path:
        """Export data to CSV format.

        Args:
            data: List of dictionaries to export
            filename: Output filename

        Returns:
            Path to exported file
        """
        if not data:
            raise ValueError("No data to export")

        output_path = self.output_dir / filename

        # Get all unique keys
        keys = set()
        for item in data:
            keys.update(item.keys())

        keys = sorted(keys)

        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        return output_path

    def export_markdown(
        self,
        data: List[Dict[str, Any]],
        filename: str,
        title: Optional[str] = None,
    ) -> Path:
        """Export data to Markdown format.

        Args:
            data: List of dictionaries to export
            filename: Output filename
            title: Optional title for the document

        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            if title:
                f.write(f"# {title}\n\n")

            f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            if data:
                # Convert to DataFrame for better table formatting
                df = pd.DataFrame(data)
                markdown_table = df.to_markdown(index=False)
                f.write(markdown_table)
                f.write("\n\n")

        return output_path

    def export_text(
        self,
        data: List[Dict[str, Any]],
        filename: str,
        title: Optional[str] = None,
        table_format: str = "grid",
    ) -> Path:
        """Export data to plain text format.

        Args:
            data: List of dictionaries to export
            filename: Output filename
            title: Optional title for the document
            table_format: Table format for tabulate (grid, plain, simple, etc.)

        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            if title:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n\n")

            f.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            if data:
                # Convert to table
                table = tabulate(data, headers="keys", tablefmt=table_format)
                f.write(table)
                f.write("\n\n")

        return output_path

    def export_analysis_report(
        self,
        analysis_data: Dict[str, Any],
        filename_base: str = "analysis_report",
        formats: List[str] = ["json", "markdown", "text"],
    ) -> Dict[str, Path]:
        """Export comprehensive analysis report in multiple formats.

        Args:
            analysis_data: Dictionary containing analysis results
            filename_base: Base filename (without extension)
            formats: List of formats to export

        Returns:
            Dictionary mapping formats to output paths
        """
        exported_files = {}

        for fmt in formats:
            if fmt == "json":
                path = self.export_json(
                    analysis_data,
                    f"{filename_base}.json"
                )
                exported_files["json"] = path

            elif fmt == "markdown":
                # Create structured markdown report
                path = self._create_markdown_report(
                    analysis_data,
                    f"{filename_base}.md"
                )
                exported_files["markdown"] = path

            elif fmt == "text":
                # Create text report
                path = self._create_text_report(
                    analysis_data,
                    f"{filename_base}.txt"
                )
                exported_files["text"] = path

            elif fmt == "csv" and "data" in analysis_data:
                # Export data section as CSV
                if isinstance(analysis_data["data"], list):
                    path = self.export_csv(
                        analysis_data["data"],
                        f"{filename_base}.csv"
                    )
                    exported_files["csv"] = path

        return exported_files

    def _create_markdown_report(
        self,
        analysis_data: Dict[str, Any],
        filename: str,
    ) -> Path:
        """Create a formatted markdown report."""
        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            # Title
            if "title" in analysis_data:
                f.write(f"# {analysis_data['title']}\n\n")
            else:
                f.write("# Analysis Report\n\n")

            # Metadata
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            if "date_range" in analysis_data:
                f.write(f"**Date Range:** {analysis_data['date_range']}\n\n")

            # Summary section
            if "summary" in analysis_data:
                f.write("## Summary\n\n")
                summary = analysis_data["summary"]
                if isinstance(summary, dict):
                    for key, value in summary.items():
                        f.write(f"- **{key.replace('_', ' ').title()}:** {value}\n")
                else:
                    f.write(f"{summary}\n")
                f.write("\n")

            # CAGR section
            if "cagr" in analysis_data:
                f.write("## Compound Annual Growth Rates (CAGR)\n\n")
                cagr_data = analysis_data["cagr"]
                if isinstance(cagr_data, dict):
                    cagr_list = []
                    for metric, result in cagr_data.items():
                        if hasattr(result, 'to_dict'):
                            cagr_list.append(result.to_dict())
                        elif isinstance(result, dict):
                            cagr_list.append(result)

                    if cagr_list:
                        df = pd.DataFrame(cagr_list)
                        f.write(df.to_markdown(index=False))
                        f.write("\n\n")

            # Data section
            if "data" in analysis_data:
                f.write("## Detailed Data\n\n")
                data = analysis_data["data"]
                if isinstance(data, list) and data:
                    df = pd.DataFrame(data)
                    f.write(df.to_markdown(index=False))
                    f.write("\n\n")

            # Additional sections
            for key, value in analysis_data.items():
                if key not in ["title", "summary", "cagr", "data", "date_range"]:
                    f.write(f"## {key.replace('_', ' ').title()}\n\n")

                    if isinstance(value, list) and value:
                        df = pd.DataFrame(value)
                        f.write(df.to_markdown(index=False))
                        f.write("\n\n")
                    elif isinstance(value, dict):
                        for k, v in value.items():
                            f.write(f"- **{k.replace('_', ' ').title()}:** {v}\n")
                        f.write("\n")
                    else:
                        f.write(f"{value}\n\n")

        return output_path

    def _create_text_report(
        self,
        analysis_data: Dict[str, Any],
        filename: str,
    ) -> Path:
        """Create a formatted text report."""
        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            # Title
            title = analysis_data.get("title", "Analysis Report")
            f.write(f"{title}\n")
            f.write("=" * len(title) + "\n\n")

            # Metadata
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            if "date_range" in analysis_data:
                f.write(f"Date Range: {analysis_data['date_range']}\n\n")

            # Summary
            if "summary" in analysis_data:
                f.write("SUMMARY\n")
                f.write("-" * 80 + "\n")
                summary = analysis_data["summary"]
                if isinstance(summary, dict):
                    for key, value in summary.items():
                        f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                else:
                    f.write(f"{summary}\n")
                f.write("\n")

            # CAGR section
            if "cagr" in analysis_data:
                f.write("COMPOUND ANNUAL GROWTH RATES (CAGR)\n")
                f.write("-" * 80 + "\n")
                cagr_data = analysis_data["cagr"]
                if isinstance(cagr_data, dict):
                    cagr_list = []
                    for metric, result in cagr_data.items():
                        if hasattr(result, 'to_dict'):
                            cagr_list.append(result.to_dict())
                        elif isinstance(result, dict):
                            cagr_list.append(result)

                    if cagr_list:
                        table = tabulate(cagr_list, headers="keys", tablefmt="grid")
                        f.write(table)
                        f.write("\n\n")

            # Data section
            if "data" in analysis_data:
                f.write("DETAILED DATA\n")
                f.write("-" * 80 + "\n")
                data = analysis_data["data"]
                if isinstance(data, list) and data:
                    table = tabulate(data, headers="keys", tablefmt="grid")
                    f.write(table)
                    f.write("\n\n")

            # Additional sections
            for key, value in analysis_data.items():
                if key not in ["title", "summary", "cagr", "data", "date_range"]:
                    section_title = key.replace('_', ' ').upper()
                    f.write(f"{section_title}\n")
                    f.write("-" * 80 + "\n")

                    if isinstance(value, list) and value:
                        table = tabulate(value, headers="keys", tablefmt="grid")
                        f.write(table)
                        f.write("\n\n")
                    elif isinstance(value, dict):
                        for k, v in value.items():
                            f.write(f"{k.replace('_', ' ').title()}: {v}\n")
                        f.write("\n")
                    else:
                        f.write(f"{value}\n\n")

        return output_path
