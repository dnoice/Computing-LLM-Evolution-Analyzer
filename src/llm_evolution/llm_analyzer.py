"""LLM performance and scaling analysis module."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import math

from .models import LLMMetrics, ComparisonResult


class LLMAnalyzer:
    """Analyzer for Large Language Model metrics and trends."""

    def __init__(self, data_path: Optional[Path] = None):
        """Initialize LLM analyzer.

        Args:
            data_path: Path to LLM data JSON file
        """
        if data_path is None:
            # Default to data/llm/models.json
            data_path = Path(__file__).parent.parent.parent / "data" / "llm" / "models.json"

        self.data_path = data_path
        self.models: List[LLMMetrics] = []
        self.load_data()

    def load_data(self) -> None:
        """Load LLM data from JSON file."""
        with open(self.data_path, 'r') as f:
            data = json.load(f)

        self.models = []
        for item in data:
            model = LLMMetrics(**item)
            self.models.append(model)

        # Sort by year and then by parameters
        self.models.sort(key=lambda x: (x.year, x.parameters_billions))

    def get_models_by_year_range(
        self, start_year: int, end_year: int
    ) -> List[LLMMetrics]:
        """Get models within a year range."""
        return [m for m in self.models if start_year <= m.year <= end_year]

    def get_model_by_name(self, name: str) -> Optional[LLMMetrics]:
        """Get a specific model by name."""
        for model in self.models:
            if model.name.lower() == name.lower():
                return model
        return None

    def get_models_by_organization(self, org: str) -> List[LLMMetrics]:
        """Get all models from a specific organization."""
        return [m for m in self.models if m.organization.lower() == org.lower()]

    def get_open_source_models(self) -> List[LLMMetrics]:
        """Get all open source models."""
        return [m for m in self.models if m.open_source]

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
        if not self.models:
            raise ValueError("No models loaded")

        # Filter by year range
        if start_year is None:
            start_year = self.models[0].year
        if end_year is None:
            end_year = self.models[-1].year

        models_in_range = self.get_models_by_year_range(start_year, end_year)

        if not models_in_range:
            raise ValueError(f"No models found in year range {start_year}-{end_year}")

        # Get the largest model in start and end years
        start_models = [m for m in models_in_range if m.year == start_year]
        end_models = [m for m in models_in_range if m.year == end_year]

        if not start_models or not end_models:
            raise ValueError("No models found at start or end year")

        # For parameters, get the largest model
        if metric_name.lower() in ['parameters', 'parameters_billions']:
            start_model = max(start_models, key=lambda m: m.parameters_billions)
            end_model = max(end_models, key=lambda m: m.parameters_billions)
        else:
            start_model = start_models[0]
            end_model = end_models[-1]

        # Map metric name to attribute
        metric_map = {
            'parameters': 'parameters_billions',
            'parameters_billions': 'parameters_billions',
            'training_tokens': 'training_tokens_billions',
            'training_tokens_billions': 'training_tokens_billions',
            'training_compute': 'training_compute_flops',
            'training_compute_flops': 'training_compute_flops',
            'context_window': 'context_window',
            'context': 'context_window',
            'cost_input': 'cost_per_1m_input_tokens',
            'cost_output': 'cost_per_1m_output_tokens',
        }

        attr_name = metric_map.get(metric_name.lower(), metric_name)

        try:
            start_value = getattr(start_model, attr_name)
            end_value = getattr(end_model, attr_name)
        except AttributeError:
            raise ValueError(f"Unknown metric: {metric_name}")

        if start_value is None or end_value is None:
            raise ValueError(f"Metric {metric_name} has None values")

        return ComparisonResult(
            metric_name=metric_name,
            start_value=start_value,
            end_value=end_value,
            start_year=start_model.year,
            end_year=end_model.year,
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
            'parameters_billions',
            'training_tokens_billions',
            'training_compute_flops',
            'context_window',
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

    def analyze_chinchilla_optimal(self) -> List[Dict[str, Any]]:
        """Analyze Chinchilla optimal scaling for all models.

        Chinchilla suggests ~20 tokens per parameter is optimal.

        Returns:
            List of dicts with model name and Chinchilla analysis
        """
        results = []

        for model in self.models:
            if model.parameters_billions and model.training_tokens_billions:
                optimal_tokens = model.parameters_billions * 20
                token_ratio = model.training_tokens_billions / model.parameters_billions

                efficiency = min(
                    model.training_tokens_billions / optimal_tokens,
                    optimal_tokens / model.training_tokens_billions
                )

                status = "optimal"
                if model.training_tokens_billions < optimal_tokens * 0.5:
                    status = "undertrained"
                elif model.training_tokens_billions > optimal_tokens * 2:
                    status = "overtrained"

                results.append({
                    'name': model.name,
                    'year': model.year,
                    'parameters_billions': model.parameters_billions,
                    'training_tokens_billions': model.training_tokens_billions,
                    'optimal_tokens_billions': optimal_tokens,
                    'token_ratio': token_ratio,
                    'efficiency': efficiency,
                    'status': status,
                })

        return results

    def get_capability_comparison(
        self, models: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, float]]:
        """Compare capability scores across models.

        Args:
            models: List of model names to compare (None for all)

        Returns:
            Dictionary mapping model names to capability scores
        """
        if models is None:
            compare_models = self.models
        else:
            compare_models = [self.get_model_by_name(m) for m in models]
            compare_models = [m for m in compare_models if m is not None]

        results = {}
        for model in compare_models:
            results[model.name] = {
                'reasoning': model.capability_score_reasoning,
                'coding': model.capability_score_coding,
                'math': model.capability_score_math,
                'knowledge': model.capability_score_knowledge,
                'multilingual': model.capability_score_multilingual,
                'average': sum([
                    model.capability_score_reasoning,
                    model.capability_score_coding,
                    model.capability_score_math,
                    model.capability_score_knowledge,
                    model.capability_score_multilingual
                ]) / 5
            }

        return results

    def analyze_cost_efficiency(self) -> List[Dict[str, Any]]:
        """Analyze cost efficiency of models.

        Returns:
            List of dicts with cost per capability metrics
        """
        results = []

        for model in self.models:
            if model.cost_per_1m_input_tokens > 0:
                avg_score = sum([
                    model.capability_score_reasoning,
                    model.capability_score_coding,
                    model.capability_score_math,
                    model.capability_score_knowledge,
                    model.capability_score_multilingual
                ]) / 5

                # Cost per capability point
                cost_efficiency = avg_score / model.cost_per_1m_input_tokens

                results.append({
                    'name': model.name,
                    'year': model.year,
                    'cost_per_1m_input': model.cost_per_1m_input_tokens,
                    'cost_per_1m_output': model.cost_per_1m_output_tokens,
                    'avg_capability_score': avg_score,
                    'cost_efficiency': cost_efficiency,
                })

        # Sort by cost efficiency descending
        results.sort(key=lambda x: x['cost_efficiency'], reverse=True)

        return results

    def get_parameter_scaling_trend(self) -> List[Dict[str, Any]]:
        """Get parameter count scaling trend over time.

        Returns:
            List of yearly maximum parameter counts
        """
        # Group by year and get max parameters
        year_max = {}
        for model in self.models:
            year = model.year
            params = model.parameters_billions

            if year not in year_max or params > year_max[year]['parameters']:
                year_max[year] = {
                    'year': year,
                    'parameters': params,
                    'model_name': model.name,
                }

        return sorted(year_max.values(), key=lambda x: x['year'])

    def get_context_window_evolution(self) -> List[Dict[str, Any]]:
        """Get context window evolution over time.

        Returns:
            List of yearly maximum context windows
        """
        year_max = {}
        for model in self.models:
            year = model.year
            context = model.context_window

            if year not in year_max or context > year_max[year]['context_window']:
                year_max[year] = {
                    'year': year,
                    'context_window': context,
                    'model_name': model.name,
                }

        return sorted(year_max.values(), key=lambda x: x['year'])

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for all models."""
        if not self.models:
            return {}

        open_source_count = len([m for m in self.models if m.open_source])

        return {
            'total_models': len(self.models),
            'year_range': f"{self.models[0].year}-{self.models[-1].year}",
            'organizations': list(set(m.organization for m in self.models)),
            'open_source_count': open_source_count,
            'closed_source_count': len(self.models) - open_source_count,
            'max_parameters': max(m.parameters_billions for m in self.models),
            'max_context_window': max(m.context_window for m in self.models),
            'earliest_model': self.models[0].name,
            'latest_model': self.models[-1].name,
        }

    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert all models to dictionaries."""
        return [model.to_dict() for model in self.models]
