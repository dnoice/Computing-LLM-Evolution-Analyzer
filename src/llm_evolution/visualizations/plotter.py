"""Visualization plotter for hardware and LLM data."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import math

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np

from ..models import HardwareMetrics, LLMMetrics


class Plotter:
    """Plotter for creating various visualizations."""

    def __init__(self, style: str = "seaborn-v0_8-darkgrid", figsize: tuple = (12, 8)):
        """Initialize plotter.

        Args:
            style: Matplotlib style
            figsize: Default figure size
        """
        # Use available style
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        self.figsize = figsize
        sns.set_palette("husl")

    def plot_hardware_evolution(
        self,
        systems: List[HardwareMetrics],
        metric: str,
        output_path: Optional[Path] = None,
        log_scale: bool = True,
    ) -> None:
        """Plot hardware metric evolution over time.

        Args:
            systems: List of hardware systems
            metric: Metric to plot
            output_path: Path to save the plot
            log_scale: Use logarithmic scale for y-axis
        """
        systems = sorted(systems, key=lambda x: x.year)

        years = [s.year for s in systems]
        values = [getattr(s, metric) for s in systems]

        # Filter out None values
        filtered_data = [(y, v) for y, v in zip(years, values) if v is not None and v > 0]
        if not filtered_data:
            return

        years, values = zip(*filtered_data)

        plt.figure(figsize=self.figsize)
        plt.plot(years, values, marker='o', linewidth=2, markersize=6)

        if log_scale:
            plt.yscale('log')

        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel(metric.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        plt.title(f'{metric.replace("_", " ").title()} Evolution Over Time',
                  fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_moores_law_comparison(
        self,
        systems: List[HardwareMetrics],
        predictions: List[float],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot Moore's Law prediction vs actual transistor counts.

        Args:
            systems: List of hardware systems
            predictions: List of Moore's Law predictions
            output_path: Path to save the plot
        """
        systems = sorted(systems, key=lambda x: x.year)

        years = [s.year for s in systems]
        actual = [s.cpu_transistors for s in systems]

        plt.figure(figsize=self.figsize)
        plt.plot(years, actual, marker='o', linewidth=2, markersize=6,
                 label='Actual', color='#2E86AB')
        plt.plot(years, predictions[:len(years)], marker='s', linewidth=2,
                 markersize=6, label="Moore's Law Prediction",
                 linestyle='--', color='#A23B72')

        plt.yscale('log')
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('Transistor Count', fontsize=12, fontweight='bold')
        plt.title("Moore's Law: Prediction vs Reality",
                  fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_cagr_heatmap(
        self,
        cagr_data: Dict[str, float],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot CAGR values as a heatmap.

        Args:
            cagr_data: Dictionary of metric names to CAGR values
            output_path: Path to save the plot
        """
        metrics = list(cagr_data.keys())
        values = [[cagr_data[m]] for m in metrics]

        plt.figure(figsize=(10, len(metrics) * 0.8))
        sns.heatmap(
            values,
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            yticklabels=[m.replace('_', ' ').title() for m in metrics],
            xticklabels=['CAGR (%)'],
            cbar_kws={'label': 'Growth Rate (%)'},
            vmin=0,
            vmax=max(values)[0] if values else 100,
        )

        plt.title('Compound Annual Growth Rates (CAGR)',
                  fontsize=14, fontweight='bold')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_llm_capability_radar(
        self,
        models: List[LLMMetrics],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot LLM capability scores as radar chart.

        Args:
            models: List of LLM models to compare
            output_path: Path to save the plot
        """
        categories = ['Reasoning', 'Coding', 'Math', 'Knowledge', 'Multilingual']
        num_vars = len(categories)

        # Compute angle for each axis
        angles = [n / float(num_vars) * 2 * math.pi for n in range(num_vars)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=self.figsize, subplot_kw=dict(projection='polar'))

        # Plot each model
        colors = plt.cm.tab10(np.linspace(0, 1, len(models)))

        for idx, model in enumerate(models):
            values = [
                model.capability_score_reasoning,
                model.capability_score_coding,
                model.capability_score_math,
                model.capability_score_knowledge,
                model.capability_score_multilingual,
            ]
            values += values[:1]

            ax.plot(angles, values, 'o-', linewidth=2, label=model.name,
                    color=colors[idx])
            ax.fill(angles, values, alpha=0.15, color=colors[idx])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=11)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], size=9)
        ax.grid(True)

        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
        plt.title('LLM Capability Comparison', fontsize=14, fontweight='bold',
                  pad=20)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_llm_parameter_scaling(
        self,
        models: List[LLMMetrics],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot LLM parameter count scaling over time.

        Args:
            models: List of LLM models
            output_path: Path to save the plot
        """
        models = sorted(models, key=lambda x: (x.year, x.parameters_billions))

        # Get max parameters per year
        year_max = {}
        for model in models:
            if model.year not in year_max or model.parameters_billions > year_max[model.year]['params']:
                year_max[model.year] = {
                    'params': model.parameters_billions,
                    'name': model.name
                }

        years = sorted(year_max.keys())
        params = [year_max[y]['params'] for y in years]
        names = [year_max[y]['name'] for y in years]

        plt.figure(figsize=self.figsize)
        bars = plt.bar(years, params, color='#3A86FF', alpha=0.8, edgecolor='black')

        # Add model names on top of bars
        for i, (year, param, name) in enumerate(zip(years, params, names)):
            plt.text(year, param, f' {name}', rotation=45, ha='left',
                     va='bottom', fontsize=9)

        plt.yscale('log')
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('Parameters (Billions)', fontsize=12, fontweight='bold')
        plt.title('LLM Parameter Count Evolution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_cost_efficiency(
        self,
        efficiency_data: List[Dict[str, Any]],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot cost efficiency comparison.

        Args:
            efficiency_data: List of dicts with cost efficiency data
            output_path: Path to save the plot
        """
        if not efficiency_data:
            return

        # Take top 10
        data = sorted(efficiency_data, key=lambda x: x['cost_efficiency'],
                      reverse=True)[:10]

        names = [d['name'] for d in data]
        efficiency = [d['cost_efficiency'] for d in data]

        plt.figure(figsize=(12, 8))
        bars = plt.barh(names, efficiency, color='#06FFA5', alpha=0.8,
                        edgecolor='black')

        plt.xlabel('Cost Efficiency (Capability Score / $1M tokens)',
                   fontsize=12, fontweight='bold')
        plt.ylabel('Model', fontsize=12, fontweight='bold')
        plt.title('LLM Cost Efficiency Comparison', fontsize=14,
                  fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_context_window_evolution(
        self,
        models: List[LLMMetrics],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot context window evolution over time.

        Args:
            models: List of LLM models
            output_path: Path to save the plot
        """
        models = sorted(models, key=lambda x: x.year)

        # Get unique years and max context window for each
        year_max = {}
        for model in models:
            if model.year not in year_max or model.context_window > year_max[model.year]['context']:
                year_max[model.year] = {
                    'context': model.context_window,
                    'name': model.name
                }

        years = sorted(year_max.keys())
        contexts = [year_max[y]['context'] for y in years]
        names = [year_max[y]['name'] for y in years]

        plt.figure(figsize=self.figsize)
        plt.plot(years, contexts, marker='o', linewidth=2, markersize=8,
                 color='#FF006E')

        # Annotate notable jumps
        for year, context, name in zip(years, contexts, names):
            if context >= 100000:  # Highlight large contexts
                plt.annotate(name, (year, context), textcoords="offset points",
                            xytext=(0, 10), ha='center', fontsize=9,
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow',
                                     alpha=0.7))

        plt.yscale('log')
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('Context Window (tokens)', fontsize=12, fontweight='bold')
        plt.title('LLM Context Window Evolution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_growth_factors(
        self,
        comparison_results: Dict[str, Any],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot growth factors for multiple metrics.

        Args:
            comparison_results: Dictionary of ComparisonResult objects
            output_path: Path to save the plot
        """
        metrics = []
        growth_factors = []

        for metric_name, result in comparison_results.items():
            metrics.append(metric_name.replace('_', ' ').title())
            growth_factors.append(result.growth_factor)

        plt.figure(figsize=(12, 8))
        bars = plt.barh(metrics, growth_factors, color='#8338EC', alpha=0.8,
                        edgecolor='black')

        # Add value labels on bars
        for i, (metric, factor) in enumerate(zip(metrics, growth_factors)):
            plt.text(factor, i, f'  {factor:.1f}x', va='center', fontsize=10,
                     fontweight='bold')

        plt.xlabel('Growth Factor', fontsize=12, fontweight='bold')
        plt.ylabel('Metric', fontsize=12, fontweight='bold')
        plt.title('Hardware Metrics Growth Factors', fontsize=14,
                  fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()
