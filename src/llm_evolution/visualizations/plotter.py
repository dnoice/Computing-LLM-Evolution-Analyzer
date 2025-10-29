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

    def plot_gpu_performance_evolution(
        self,
        gpus: List,
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot GPU performance (TFLOPS) evolution over time.

        Args:
            gpus: List of GPU metrics
            output_path: Path to save the plot
        """
        gpus = sorted(gpus, key=lambda x: x.year)

        # Get max TFLOPS per year
        year_max = {}
        for gpu in gpus:
            if gpu.year not in year_max or gpu.tflops_fp32 > year_max[gpu.year]['tflops']:
                year_max[gpu.year] = {
                    'tflops': gpu.tflops_fp32,
                    'name': gpu.name,
                    'manufacturer': gpu.manufacturer
                }

        years = sorted(year_max.keys())
        tflops = [year_max[y]['tflops'] for y in years]
        names = [year_max[y]['name'] for y in years]
        manufacturers = [year_max[y]['manufacturer'] for y in years]

        # Color by manufacturer
        colors = []
        for mfr in manufacturers:
            if 'NVIDIA' in mfr:
                colors.append('#76B900')  # NVIDIA green
            elif 'AMD' in mfr:
                colors.append('#ED1C24')  # AMD red
            elif 'Intel' in mfr:
                colors.append('#0071C5')  # Intel blue
            else:
                colors.append('#888888')

        plt.figure(figsize=self.figsize)
        plt.plot(years, tflops, marker='o', linewidth=2, markersize=8,
                 color='#2E86AB', alpha=0.7)

        # Color the markers by manufacturer
        for year, tflop, color in zip(years, tflops, colors):
            plt.scatter(year, tflop, s=100, c=color, edgecolor='black',
                       linewidth=1, zorder=5)

        plt.yscale('log')
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('TFLOPS (FP32)', fontsize=12, fontweight='bold')
        plt.title('GPU Performance Evolution (Max TFLOPS per Year)',
                  fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#76B900', label='NVIDIA'),
            Patch(facecolor='#ED1C24', label='AMD'),
            Patch(facecolor='#0071C5', label='Intel')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_gpu_memory_evolution(
        self,
        gpus: List,
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot GPU memory (VRAM) evolution over time.

        Args:
            gpus: List of GPU metrics
            output_path: Path to save the plot
        """
        gpus = sorted(gpus, key=lambda x: x.year)

        years = [g.year for g in gpus]
        vram_gb = [g.vram_mb / 1024 for g in gpus]
        names = [g.name for g in gpus]
        manufacturers = [g.manufacturer for g in gpus]

        # Color by manufacturer
        colors = []
        for mfr in manufacturers:
            if 'NVIDIA' in mfr:
                colors.append('#76B900')
            elif 'AMD' in mfr:
                colors.append('#ED1C24')
            elif 'Intel' in mfr:
                colors.append('#0071C5')
            else:
                colors.append('#888888')

        plt.figure(figsize=self.figsize)
        plt.scatter(years, vram_gb, s=100, c=colors, edgecolor='black',
                   linewidth=1, alpha=0.7)

        plt.yscale('log')
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('VRAM (GB)', fontsize=12, fontweight='bold')
        plt.title('GPU Memory Evolution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#76B900', label='NVIDIA'),
            Patch(facecolor='#ED1C24', label='AMD'),
            Patch(facecolor='#0071C5', label='Intel')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_gpu_efficiency(
        self,
        gpus: List,
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot GPU efficiency (TFLOPS/Watt) over time.

        Args:
            gpus: List of GPU metrics
            output_path: Path to save the plot
        """
        gpus = sorted(gpus, key=lambda x: x.year)

        data = []
        for gpu in gpus:
            if gpu.tflops_fp32 > 0 and gpu.tdp_watts > 0:
                efficiency = gpu.tflops_fp32 / gpu.tdp_watts
                data.append({
                    'year': gpu.year,
                    'efficiency': efficiency,
                    'name': gpu.name,
                    'manufacturer': gpu.manufacturer
                })

        years = [d['year'] for d in data]
        efficiency = [d['efficiency'] for d in data]
        manufacturers = [d['manufacturer'] for d in data]

        # Color by manufacturer
        colors = []
        for mfr in manufacturers:
            if 'NVIDIA' in mfr:
                colors.append('#76B900')
            elif 'AMD' in mfr:
                colors.append('#ED1C24')
            elif 'Intel' in mfr:
                colors.append('#0071C5')
            else:
                colors.append('#888888')

        plt.figure(figsize=self.figsize)
        plt.scatter(years, efficiency, s=100, c=colors, edgecolor='black',
                   linewidth=1, alpha=0.7)

        plt.yscale('log')
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('TFLOPS per Watt', fontsize=12, fontweight='bold')
        plt.title('GPU Power Efficiency Evolution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#76B900', label='NVIDIA'),
            Patch(facecolor='#ED1C24', label='AMD'),
            Patch(facecolor='#0071C5', label='Intel')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_gpu_manufacturer_comparison(
        self,
        comparison_data: Dict[str, Dict[str, Any]],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot comparison of GPU manufacturers.

        Args:
            comparison_data: Dictionary with manufacturer statistics
            output_path: Path to save the plot
        """
        manufacturers = list(comparison_data.keys())
        counts = [comparison_data[m]['count'] for m in manufacturers]
        avg_tflops = [comparison_data[m]['avg_tflops_fp32'] for m in manufacturers]

        # Set up colors
        mfr_colors = []
        for mfr in manufacturers:
            if 'NVIDIA' in mfr:
                mfr_colors.append('#76B900')
            elif 'AMD' in mfr:
                mfr_colors.append('#ED1C24')
            elif 'Intel' in mfr:
                mfr_colors.append('#0071C5')
            else:
                mfr_colors.append('#888888')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # GPU count by manufacturer
        ax1.bar(manufacturers, counts, color=mfr_colors, alpha=0.8, edgecolor='black')
        ax1.set_ylabel('Number of GPUs', fontsize=11, fontweight='bold')
        ax1.set_title('GPU Count by Manufacturer', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')

        # Average TFLOPS by manufacturer
        ax2.bar(manufacturers, avg_tflops, color=mfr_colors, alpha=0.8, edgecolor='black')
        ax2.set_ylabel('Average TFLOPS (FP32)', fontsize=11, fontweight='bold')
        ax2.set_title('Average Performance by Manufacturer', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_gpu_price_performance(
        self,
        gpus: List,
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot GPU price vs performance scatter.

        Args:
            gpus: List of GPU metrics
            output_path: Path to save the plot
        """
        data = []
        for gpu in gpus:
            if gpu.tflops_fp32 > 0 and gpu.launch_price_usd > 0:
                data.append({
                    'tflops': gpu.tflops_fp32,
                    'price': gpu.launch_price_usd,
                    'name': gpu.name,
                    'year': gpu.year,
                    'manufacturer': gpu.manufacturer
                })

        if not data:
            return

        tflops = [d['tflops'] for d in data]
        prices = [d['price'] for d in data]
        years = [d['year'] for d in data]
        manufacturers = [d['manufacturer'] for d in data]

        # Color by manufacturer
        colors = []
        for mfr in manufacturers:
            if 'NVIDIA' in mfr:
                colors.append('#76B900')
            elif 'AMD' in mfr:
                colors.append('#ED1C24')
            elif 'Intel' in mfr:
                colors.append('#0071C5')
            else:
                colors.append('#888888')

        plt.figure(figsize=self.figsize)
        scatter = plt.scatter(tflops, prices, s=100, c=colors, edgecolor='black',
                            linewidth=1, alpha=0.7)

        plt.xlabel('TFLOPS (FP32)', fontsize=12, fontweight='bold')
        plt.ylabel('Launch Price (USD)', fontsize=12, fontweight='bold')
        plt.title('GPU Price vs Performance', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#76B900', label='NVIDIA'),
            Patch(facecolor='#ED1C24', label='AMD'),
            Patch(facecolor='#0071C5', label='Intel')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_cloud_cost_comparison(
        self,
        comparison_data: Dict[str, Dict[str, Any]],
        title: str = "Cloud Provider Cost Comparison",
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot cost comparison across cloud providers."""
        if not comparison_data:
            return

        providers = list(comparison_data.keys())
        costs = [comparison_data[p]['total_cost_usd'] for p in providers]
        instance_types = [comparison_data[p]['instance_type'] for p in providers]

        colors = []
        for provider in providers:
            if 'AWS' in provider:
                colors.append('#FF9900')
            elif 'Azure' in provider:
                colors.append('#0078D4')
            elif 'GCP' in provider:
                colors.append('#4285F4')
            else:
                colors.append('#888888')

        plt.figure(figsize=self.figsize)
        bars = plt.bar(providers, costs, color=colors, edgecolor='black', linewidth=1.5)

        for bar, cost, instance_type in zip(bars, costs, instance_types):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${cost:,.0f}\n{instance_type}',
                    ha='center', va='bottom', fontsize=9)

        plt.xlabel('Cloud Provider', fontsize=12, fontweight='bold')
        plt.ylabel('Total Cost (USD)', fontsize=12, fontweight='bold')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_cost_efficiency_ranking(
        self,
        ranking_data: List[Dict[str, Any]],
        top_n: int = 10,
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot cost efficiency ranking for cloud instances."""
        if not ranking_data:
            return

        data = ranking_data[:top_n]
        labels = [f"{d['provider']}\n{d['instance_type']}" for d in data]
        tflops_per_dollar = [d['tflops_per_dollar'] for d in data]

        colors = []
        for d in data:
            if 'AWS' in d['provider']:
                colors.append('#FF9900')
            elif 'Azure' in d['provider']:
                colors.append('#0078D4')
            elif 'GCP' in d['provider']:
                colors.append('#4285F4')
            else:
                colors.append('#888888')

        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(labels)), tflops_per_dollar, color=colors,
                       edgecolor='black', linewidth=1)

        for i, (bar, value) in enumerate(zip(bars, tflops_per_dollar)):
            plt.text(value, i, f' {value:.2f}', va='center', fontsize=9)

        plt.yticks(range(len(labels)), labels, fontsize=9)
        plt.xlabel('TFLOPS per Dollar', fontsize=12, fontweight='bold')
        plt.title('Cloud Instance Cost Efficiency Ranking', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_spot_savings(
        self,
        savings_data: List[Dict[str, Any]],
        top_n: int = 12,
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot spot instance savings analysis."""
        if not savings_data:
            return

        data = savings_data[:top_n]
        labels = [f"{d['provider']}\n{d['instance_type']}" for d in data]
        savings_percent = [d['savings_percent'] for d in data]
        annual_savings = [d['annual_savings_usd'] for d in data]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        colors = []
        for d in data:
            if 'AWS' in d['provider']:
                colors.append('#FF9900')
            elif 'Azure' in d['provider']:
                colors.append('#0078D4')
            elif 'GCP' in d['provider']:
                colors.append('#4285F4')
            else:
                colors.append('#888888')

        bars1 = ax1.barh(range(len(labels)), savings_percent, color=colors,
                        edgecolor='black', linewidth=1)
        for i, (bar, value) in enumerate(zip(bars1, savings_percent)):
            ax1.text(value, i, f' {value:.1f}%', va='center', fontsize=8)

        ax1.set_yticks(range(len(labels)))
        ax1.set_yticklabels(labels, fontsize=8)
        ax1.set_xlabel('Savings Percentage', fontsize=11, fontweight='bold')
        ax1.set_title('Spot vs On-Demand Savings (%)', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')

        bars2 = ax2.barh(range(len(labels)), annual_savings, color=colors,
                        edgecolor='black', linewidth=1)
        for i, (bar, value) in enumerate(zip(bars2, annual_savings)):
            ax2.text(value, i, f' ${value:,.0f}', va='center', fontsize=8)

        ax2.set_yticks(range(len(labels)))
        ax2.set_yticklabels(labels, fontsize=8)
        ax2.set_xlabel('Annual Savings (USD)', fontsize=11, fontweight='bold')
        ax2.set_title('Annual Savings (24/7 Usage)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_gpu_price_evolution(
        self,
        evolution_data: Dict[str, List[Dict[str, Any]]],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot GPU price evolution over time across providers."""
        if not evolution_data:
            return

        plt.figure(figsize=(14, 8))

        for gpu_model, price_data in evolution_data.items():
            if not price_data:
                continue

            providers = {}
            for entry in price_data:
                provider = entry['provider']
                if provider not in providers:
                    providers[provider] = []
                providers[provider].append(entry)

            for provider, entries in providers.items():
                years = [e['year'] for e in entries]
                prices = [e['price_ondemand_hourly'] for e in entries]

                if 'AWS' in provider:
                    color = '#FF9900'
                elif 'Azure' in provider:
                    color = '#0078D4'
                elif 'GCP' in provider:
                    color = '#4285F4'
                else:
                    color = '#888888'

                plt.plot(years, prices, marker='o', linewidth=2, markersize=8,
                        label=f'{gpu_model} ({provider})', color=color)

        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('On-Demand Price (USD/hour)', fontsize=12, fontweight='bold')
        plt.title('Cloud GPU Instance Price Evolution', fontsize=14, fontweight='bold')
        plt.legend(fontsize=9, loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_training_cost_breakdown(
        self,
        cost_estimate: Dict[str, Any],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot LLM training cost breakdown."""
        if not cost_estimate:
            return

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

        compute_cost = cost_estimate['compute_cost_usd']
        storage_cost = cost_estimate['storage_cost_usd']

        if compute_cost > 0 or storage_cost > 0:
            costs = [compute_cost, storage_cost]
            labels = ['Compute', 'Storage']
            colors = ['#FF6B6B', '#4ECDC4']

            ax1.pie(costs, labels=labels, autopct='%1.1f%%', startangle=90,
                   colors=colors, textprops={'fontsize': 11, 'fontweight': 'bold'})
            ax1.set_title('Cost Breakdown', fontsize=12, fontweight='bold')

        details = [
            ['Model Size', cost_estimate.get('model_size_params', 'N/A')],
            ['Training Tokens', cost_estimate.get('training_tokens', 'N/A')],
            ['Provider', cost_estimate.get('provider', 'N/A')],
            ['Instance Type', cost_estimate.get('instance_type', 'N/A')],
            ['GPU Model', cost_estimate.get('gpu_model', 'N/A')],
            ['GPU Count', str(cost_estimate.get('gpu_count', 0))],
            ['Training Days', f"{cost_estimate.get('training_days', 0):.1f}"],
            ['Pricing Model', cost_estimate.get('pricing_model', 'N/A')],
        ]

        ax2.axis('tight')
        ax2.axis('off')
        table = ax2.table(cellText=details, cellLoc='left',
                         colWidths=[0.5, 0.5], loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        ax2.set_title('Training Configuration', fontsize=12, fontweight='bold', pad=20)

        pricing_model = cost_estimate.get('pricing_model', 'on-demand')
        total_cost = cost_estimate.get('total_cost_usd', 0)

        if pricing_model == 'spot':
            ondemand_cost = total_cost / 0.3
            costs = [ondemand_cost, total_cost]
            labels = ['On-Demand\n(Estimated)', 'Spot\n(Actual)']
        else:
            costs = [total_cost]
            labels = ['On-Demand']

        bars = ax3.bar(labels, costs, color=['#FF9900', '#4ECDC4'][:len(costs)],
                      edgecolor='black', linewidth=1.5)
        for bar, cost in zip(bars, costs):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'${cost:,.0f}', ha='center', va='bottom', fontsize=10,
                    fontweight='bold')

        ax3.set_ylabel('Total Cost (USD)', fontsize=11, fontweight='bold')
        ax3.set_title('Pricing Model Comparison', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')

        summary_text = f"""
TOTAL TRAINING COST
${total_cost:,.2f}

Compute: ${compute_cost:,.2f}
Storage: ${storage_cost:,.2f}

Hourly Rate: ${cost_estimate.get('hourly_rate', 0):.2f}/hr
Training Hours: {cost_estimate.get('training_hours', 0):.1f}
        """

        ax4.text(0.5, 0.5, summary_text.strip(), transform=ax4.transAxes,
                fontsize=12, verticalalignment='center', horizontalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontfamily='monospace', fontweight='bold')
        ax4.axis('off')
        ax4.set_title('Cost Summary', fontsize=12, fontweight='bold')

        plt.suptitle(f'LLM Training Cost Analysis - {cost_estimate.get("model_size_params", "N/A")} Model',
                    fontsize=14, fontweight='bold', y=0.98)
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def plot_provider_comparison_matrix(
        self,
        provider_stats: Dict[str, Dict[str, Any]],
        output_path: Optional[Path] = None,
    ) -> None:
        """Plot comparison matrix of provider statistics."""
        if not provider_stats:
            return

        providers = list(provider_stats.keys())
        metrics = ['instance_count', 'avg_hourly_cost', 'avg_spot_discount_percent',
                  'training_instances', 'inference_instances']

        matrix_data = []
        metric_labels = []

        for metric in metrics:
            row = []
            for provider in providers:
                value = provider_stats[provider].get(metric, 0)
                row.append(value)
            matrix_data.append(row)
            metric_labels.append(metric.replace('_', ' ').title())

        normalized_data = []
        for row in matrix_data:
            max_val = max(row) if max(row) > 0 else 1
            normalized_data.append([v / max_val for v in row])

        plt.figure(figsize=(10, 6))
        sns.heatmap(normalized_data, annot=[[f'{v:.1f}' for v in row] for row in matrix_data],
                   fmt='s', cmap='YlOrRd', xticklabels=providers,
                   yticklabels=metric_labels, cbar_kws={'label': 'Normalized Value'})

        plt.title('Cloud Provider Comparison Matrix', fontsize=14, fontweight='bold')
        plt.xlabel('Provider', fontsize=12, fontweight='bold')
        plt.ylabel('Metric', fontsize=12, fontweight='bold')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()
