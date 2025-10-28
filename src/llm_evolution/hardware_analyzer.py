"""Hardware performance analysis module."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import math

from .models import HardwareMetrics, ComparisonResult


class HardwareAnalyzer:
    """Analyzer for computing hardware metrics and trends."""

    def __init__(self, data_path: Optional[Path] = None):
        """Initialize hardware analyzer.

        Args:
            data_path: Path to hardware data JSON file
        """
        if data_path is None:
            # Default to data/hardware/systems.json
            data_path = Path(__file__).parent.parent.parent / "data" / "hardware" / "systems.json"

        self.data_path = data_path
        self.systems: List[HardwareMetrics] = []
        self.load_data()

    def load_data(self) -> None:
        """Load hardware data from JSON file."""
        with open(self.data_path, 'r') as f:
            data = json.load(f)

        self.systems = []
        for item in data:
            system = HardwareMetrics(**item)
            self.systems.append(system)

        # Sort by year
        self.systems.sort(key=lambda x: x.year)

    def get_systems_by_year_range(
        self, start_year: int, end_year: int
    ) -> List[HardwareMetrics]:
        """Get systems within a year range."""
        return [s for s in self.systems if start_year <= s.year <= end_year]

    def get_system_by_name(self, name: str) -> Optional[HardwareMetrics]:
        """Get a specific system by name."""
        for system in self.systems:
            if system.name.lower() == name.lower():
                return system
        return None

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
        if not self.systems:
            raise ValueError("No systems loaded")

        # Filter by year range
        if start_year is None:
            start_year = self.systems[0].year
        if end_year is None:
            end_year = self.systems[-1].year

        systems_in_range = self.get_systems_by_year_range(start_year, end_year)

        if not systems_in_range:
            raise ValueError(f"No systems found in year range {start_year}-{end_year}")

        # Get metric values
        start_system = systems_in_range[0]
        end_system = systems_in_range[-1]

        # Map metric name to attribute
        metric_map = {
            'cpu_transistors': 'cpu_transistors',
            'transistors': 'cpu_transistors',
            'cpu_clock_mhz': 'cpu_clock_mhz',
            'clock_speed': 'cpu_clock_mhz',
            'ram_mb': 'ram_mb',
            'ram': 'ram_mb',
            'storage_mb': 'storage_mb',
            'storage': 'storage_mb',
            'performance_mips': 'performance_mips',
            'mips': 'performance_mips',
            'performance_flops': 'performance_flops',
            'flops': 'performance_flops',
            'power_watts': 'power_watts',
            'power': 'power_watts',
            'price_usd': 'price_usd',
            'price': 'price_usd',
            'cpu_cores': 'cpu_cores',
            'cores': 'cpu_cores',
        }

        attr_name = metric_map.get(metric_name.lower(), metric_name)

        try:
            start_value = getattr(start_system, attr_name)
            end_value = getattr(end_system, attr_name)
        except AttributeError:
            raise ValueError(f"Unknown metric: {metric_name}")

        if start_value is None or end_value is None:
            raise ValueError(f"Metric {metric_name} has None values")

        return ComparisonResult(
            metric_name=metric_name,
            start_value=start_value,
            end_value=end_value,
            start_year=start_system.year,
            end_year=end_system.year,
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
            'cpu_transistors',
            'cpu_clock_mhz',
            'cpu_cores',
            'ram_mb',
            'storage_mb',
            'performance_mips',
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

    def analyze_moores_law(
        self,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        doubling_period: float = 2.0,
    ) -> ComparisonResult:
        """Analyze Moore's Law prediction vs actual transistor growth.

        Args:
            start_year: Starting year
            end_year: Ending year
            doubling_period: Years for transistor doubling (default 2.0)

        Returns:
            ComparisonResult with Moore's Law comparison
        """
        result = self.analyze_metric_growth('cpu_transistors', start_year, end_year)

        # Calculate Moore's Law prediction
        years = result.end_year - result.start_year
        doublings = years / doubling_period
        moores_law_predicted = result.start_value * (2 ** doublings)

        result.moores_law_predicted = moores_law_predicted

        # Calculate accuracy (how close actual is to predicted)
        if moores_law_predicted > 0:
            accuracy = (result.end_value / moores_law_predicted) * 100
            result.moores_law_accuracy = accuracy

        return result

    def get_efficiency_trends(
        self, start_year: Optional[int] = None, end_year: Optional[int] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Calculate efficiency trends over time.

        Returns metrics like MIPS/Watt, MIPS/Dollar, etc.

        Args:
            start_year: Starting year
            end_year: Ending year

        Returns:
            Dictionary with efficiency metric time series
        """
        systems = self.systems
        if start_year:
            systems = [s for s in systems if s.year >= start_year]
        if end_year:
            systems = [s for s in systems if s.year <= end_year]

        mips_per_watt = []
        mips_per_dollar = []
        transistor_density = []

        for system in systems:
            metrics = system.compute_efficiency_metrics()

            if 'mips_per_watt' in metrics:
                mips_per_watt.append({
                    'year': system.year,
                    'name': system.name,
                    'value': metrics['mips_per_watt']
                })

            if 'mips_per_dollar' in metrics:
                mips_per_dollar.append({
                    'year': system.year,
                    'name': system.name,
                    'value': metrics['mips_per_dollar']
                })

            if 'transistor_density' in metrics:
                transistor_density.append({
                    'year': system.year,
                    'name': system.name,
                    'value': metrics['transistor_density']
                })

        return {
            'mips_per_watt': mips_per_watt,
            'mips_per_dollar': mips_per_dollar,
            'transistor_density': transistor_density,
        }

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for all systems."""
        if not self.systems:
            return {}

        return {
            'total_systems': len(self.systems),
            'year_range': f"{self.systems[0].year}-{self.systems[-1].year}",
            'manufacturers': list(set(s.manufacturer for s in self.systems)),
            'architectures': list(set(s.architecture for s in self.systems)),
            'earliest_system': self.systems[0].name,
            'latest_system': self.systems[-1].name,
        }

    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert all systems to dictionaries."""
        return [system.to_dict() for system in self.systems]
