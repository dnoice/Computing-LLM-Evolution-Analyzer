"""GPU performance analysis module."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import math

from .models import GPUMetrics, ComparisonResult


class GPUAnalyzer:
    """Analyzer for GPU metrics and trends."""

    def __init__(self, data_path: Optional[Path] = None):
        """Initialize GPU analyzer.

        Args:
            data_path: Path to GPU data JSON file
        """
        if data_path is None:
            # Default to data/gpu/gpus.json
            data_path = Path(__file__).parent.parent.parent / "data" / "gpu" / "gpus.json"

        self.data_path = data_path
        self.gpus: List[GPUMetrics] = []
        self.load_data()

    def load_data(self) -> None:
        """Load GPU data from JSON file."""
        with open(self.data_path, 'r') as f:
            data = json.load(f)

        self.gpus = []
        for item in data:
            gpu = GPUMetrics(**item)
            self.gpus.append(gpu)

        # Sort by year and then by performance
        self.gpus.sort(key=lambda x: (x.year, x.tflops_fp32))

    def get_gpus_by_year_range(
        self, start_year: int, end_year: int
    ) -> List[GPUMetrics]:
        """Get GPUs within a year range."""
        return [g for g in self.gpus if start_year <= g.year <= end_year]

    def get_gpu_by_name(self, name: str) -> Optional[GPUMetrics]:
        """Get a specific GPU by name."""
        for gpu in self.gpus:
            if gpu.name.lower() == name.lower():
                return gpu
        return None

    def get_gpus_by_manufacturer(self, manufacturer: str) -> List[GPUMetrics]:
        """Get all GPUs from a specific manufacturer."""
        return [g for g in self.gpus if g.manufacturer.lower() == manufacturer.lower()]

    def calculate_cagr(
        self, start_value: float, end_value: float, years: int
    ) -> float:
        """Calculate Compound Annual Growth Rate.

        Args:
            start_value: Starting value
            end_value: Ending value
            years: Number of years

        Returns:
            CAGR as a percentage
        """
        if start_value <= 0 or years <= 0:
            return 0.0

        cagr = (math.pow(end_value / start_value, 1 / years) - 1) * 100
        return cagr

    def analyze_metric_growth(
        self,
        metric_name: str,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> ComparisonResult:
        """Analyze growth of a specific metric over time.

        Args:
            metric_name: Name of the metric to analyze
            start_year: Starting year (defaults to earliest)
            end_year: Ending year (defaults to latest)

        Returns:
            ComparisonResult with growth analysis
        """
        if not self.gpus:
            raise ValueError("No GPUs loaded")

        # Filter by year range
        if start_year is None:
            start_year = self.gpus[0].year
        if end_year is None:
            end_year = self.gpus[-1].year

        gpus_in_range = self.get_gpus_by_year_range(start_year, end_year)

        if not gpus_in_range:
            raise ValueError(f"No GPUs found in year range {start_year}-{end_year}")

        # Get metric values
        start_gpu = gpus_in_range[0]
        end_gpu = gpus_in_range[-1]

        # Map metric name to attribute
        metric_map = {
            'cuda_cores': 'cuda_cores',
            'compute_cores': 'cuda_cores',
            'tflops': 'tflops_fp32',
            'tflops_fp32': 'tflops_fp32',
            'vram': 'vram_mb',
            'vram_mb': 'vram_mb',
            'memory_bandwidth': 'memory_bandwidth_gbps',
            'memory_bandwidth_gbps': 'memory_bandwidth_gbps',
            'tdp': 'tdp_watts',
            'tdp_watts': 'tdp_watts',
            'price': 'launch_price_usd',
            'launch_price_usd': 'launch_price_usd',
            'transistors': 'transistors_millions',
            'transistors_millions': 'transistors_millions',
        }

        attr_name = metric_map.get(metric_name.lower(), metric_name)

        try:
            start_value = getattr(start_gpu, attr_name)
            end_value = getattr(end_gpu, attr_name)
        except AttributeError:
            raise ValueError(f"Unknown metric: {metric_name}")

        if start_value is None or end_value is None:
            raise ValueError(f"Metric {metric_name} has None values")

        return ComparisonResult(
            metric_name=metric_name,
            start_value=start_value,
            end_value=end_value,
            start_year=start_gpu.year,
            end_year=end_gpu.year,
        )

    def calculate_all_cagrs(
        self, start_year: Optional[int] = None, end_year: Optional[int] = None
    ) -> Dict[str, ComparisonResult]:
        """Calculate CAGRs for all major metrics.

        Args:
            start_year: Starting year
            end_year: Ending year

        Returns:
            Dictionary mapping metric names to ComparisonResult objects
        """
        metrics = [
            'tflops_fp32',
            'vram_mb',
            'memory_bandwidth_gbps',
            'transistors_millions',
            'tdp_watts',
        ]

        results = {}
        for metric in metrics:
            try:
                result = self.analyze_metric_growth(metric, start_year, end_year)
                results[metric] = result
            except (ValueError, AttributeError):
                # Skip metrics that don't have data
                continue

        return results

    def get_efficiency_trends(
        self, start_year: Optional[int] = None, end_year: Optional[int] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Calculate efficiency trends over time.

        Returns metrics like TFLOPS/Watt, TFLOPS/Dollar, etc.

        Args:
            start_year: Starting year
            end_year: Ending year

        Returns:
            Dictionary with efficiency metric time series
        """
        gpus = self.gpus
        if start_year:
            gpus = [g for g in gpus if g.year >= start_year]
        if end_year:
            gpus = [g for g in gpus if g.year <= end_year]

        tflops_per_watt = []
        tflops_per_dollar = []
        transistor_density = []

        for gpu in gpus:
            metrics = gpu.compute_efficiency_metrics()

            if 'tflops_per_watt' in metrics:
                tflops_per_watt.append({
                    'year': gpu.year,
                    'name': gpu.name,
                    'manufacturer': gpu.manufacturer,
                    'value': metrics['tflops_per_watt']
                })

            if 'tflops_per_dollar' in metrics:
                tflops_per_dollar.append({
                    'year': gpu.year,
                    'name': gpu.name,
                    'manufacturer': gpu.manufacturer,
                    'value': metrics['tflops_per_dollar']
                })

            if 'transistor_density_per_mm2' in metrics:
                transistor_density.append({
                    'year': gpu.year,
                    'name': gpu.name,
                    'manufacturer': gpu.manufacturer,
                    'value': metrics['transistor_density_per_mm2']
                })

        return {
            'tflops_per_watt': tflops_per_watt,
            'tflops_per_dollar': tflops_per_dollar,
            'transistor_density_per_mm2': transistor_density,
        }

    def get_manufacturer_comparison(self) -> Dict[str, Dict[str, Any]]:
        """Compare GPUs across manufacturers.

        Returns:
            Dictionary with statistics per manufacturer
        """
        manufacturers = ['NVIDIA', 'AMD', 'Intel']
        comparison = {}

        for mfr in manufacturers:
            mfr_gpus = self.get_gpus_by_manufacturer(mfr)
            if not mfr_gpus:
                continue

            # Calculate averages
            avg_tflops = sum(g.tflops_fp32 for g in mfr_gpus) / len(mfr_gpus)
            avg_vram = sum(g.vram_mb for g in mfr_gpus) / len(mfr_gpus)
            avg_tdp = sum(g.tdp_watts for g in mfr_gpus) / len(mfr_gpus)

            # Count features
            rt_count = sum(1 for g in mfr_gpus if g.ray_tracing_support)

            comparison[mfr] = {
                'count': len(mfr_gpus),
                'avg_tflops_fp32': avg_tflops,
                'avg_vram_mb': avg_vram,
                'avg_tdp_watts': avg_tdp,
                'ray_tracing_count': rt_count,
                'first_year': mfr_gpus[0].year,
                'latest_year': mfr_gpus[-1].year,
            }

        return comparison

    def get_performance_evolution(self) -> List[Dict[str, Any]]:
        """Get performance evolution over time (max TFLOPS per year).

        Returns:
            List of yearly maximum performance
        """
        year_max = {}
        for gpu in self.gpus:
            year = gpu.year
            tflops = gpu.tflops_fp32

            if year not in year_max or tflops > year_max[year]['tflops']:
                year_max[year] = {
                    'year': year,
                    'tflops': tflops,
                    'gpu_name': gpu.name,
                    'manufacturer': gpu.manufacturer,
                }

        return sorted(year_max.values(), key=lambda x: x['year'])

    def get_memory_evolution(self) -> List[Dict[str, Any]]:
        """Get memory capacity evolution over time.

        Returns:
            List of yearly maximum VRAM
        """
        year_max = {}
        for gpu in self.gpus:
            year = gpu.year
            vram = gpu.vram_mb

            if year not in year_max or vram > year_max[year]['vram_mb']:
                year_max[year] = {
                    'year': year,
                    'vram_mb': vram,
                    'vram_gb': vram / 1024,
                    'gpu_name': gpu.name,
                    'manufacturer': gpu.manufacturer,
                }

        return sorted(year_max.values(), key=lambda x: x['year'])

    def get_architectural_milestones(self) -> List[Dict[str, Any]]:
        """Identify major architectural milestones.

        Returns:
            List of milestone GPUs
        """
        milestones = []

        for gpu in self.gpus:
            is_milestone = False
            reasons = []

            # First GPU
            if gpu == self.gpus[0]:
                is_milestone = True
                reasons.append("First in dataset")

            # First with ray tracing
            if gpu.ray_tracing_support and not any(
                g.ray_tracing_support for g in self.gpus if g.year < gpu.year
            ):
                is_milestone = True
                reasons.append("First with hardware ray tracing")

            # First with tensor cores
            if gpu.tensor_cores and not any(
                g.tensor_cores for g in self.gpus if g.year < gpu.year
            ):
                is_milestone = True
                reasons.append("First with Tensor cores")

            # Major process node transitions
            if gpu.process_nm in [90, 28, 16, 7, 5]:
                prev_gpus = [g for g in self.gpus if g.year < gpu.year]
                if not prev_gpus or all(g.process_nm > gpu.process_nm for g in prev_gpus):
                    is_milestone = True
                    reasons.append(f"First {gpu.process_nm}nm process")

            if is_milestone:
                milestones.append({
                    'name': gpu.name,
                    'year': gpu.year,
                    'manufacturer': gpu.manufacturer,
                    'architecture': gpu.architecture,
                    'reasons': reasons,
                })

        return milestones

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for all GPUs."""
        if not self.gpus:
            return {}

        return {
            'total_gpus': len(self.gpus),
            'year_range': f"{self.gpus[0].year}-{self.gpus[-1].year}",
            'manufacturers': list(set(g.manufacturer for g in self.gpus)),
            'manufacturer_count': {
                mfr: len(self.get_gpus_by_manufacturer(mfr))
                for mfr in set(g.manufacturer for g in self.gpus)
            },
            'earliest_gpu': self.gpus[0].name,
            'latest_gpu': self.gpus[-1].name,
            'max_tflops': max(g.tflops_fp32 for g in self.gpus),
            'max_vram_gb': max(g.vram_mb for g in self.gpus) / 1024,
            'ray_tracing_count': sum(1 for g in self.gpus if g.ray_tracing_support),
        }

    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert all GPUs to dictionaries."""
        return [gpu.to_dict() for gpu in self.gpus]
