"""Moore's Law analysis and predictions."""

from typing import List, Dict, Any, Optional
import math
from datetime import datetime

from .models import HardwareMetrics


class MooresLawAnalyzer:
    """Analyzer for Moore's Law predictions and comparisons."""

    def __init__(self, doubling_period: float = 2.0):
        """Initialize Moore's Law analyzer.

        Args:
            doubling_period: Years for transistor count doubling (default 2.0)
        """
        self.doubling_period = doubling_period

    def predict_transistors(
        self,
        base_transistors: int,
        base_year: int,
        target_year: int,
    ) -> float:
        """Predict transistor count using Moore's Law.

        Args:
            base_transistors: Starting transistor count
            base_year: Starting year
            target_year: Target year for prediction

        Returns:
            Predicted transistor count
        """
        years = target_year - base_year
        doublings = years / self.doubling_period

        predicted = base_transistors * (2 ** doublings)
        return predicted

    def calculate_accuracy(
        self,
        predicted: float,
        actual: float,
    ) -> float:
        """Calculate prediction accuracy as percentage.

        Args:
            predicted: Predicted value
            actual: Actual value

        Returns:
            Accuracy percentage (100 = perfect, >100 = exceeded prediction)
        """
        if predicted <= 0:
            return 0.0

        accuracy = (actual / predicted) * 100
        return accuracy

    def analyze_historical_adherence(
        self,
        systems: List[HardwareMetrics],
    ) -> List[Dict[str, Any]]:
        """Analyze how well historical data adheres to Moore's Law.

        Args:
            systems: List of hardware systems to analyze

        Returns:
            List of dictionaries with analysis for each system
        """
        if not systems or len(systems) < 2:
            return []

        results = []
        base_system = systems[0]

        for system in systems[1:]:
            predicted = self.predict_transistors(
                base_system.cpu_transistors,
                base_system.year,
                system.year,
            )

            accuracy = self.calculate_accuracy(predicted, system.cpu_transistors)

            # Calculate actual doubling period
            years = system.year - base_system.year
            if system.cpu_transistors > 0 and base_system.cpu_transistors > 0:
                growth_factor = system.cpu_transistors / base_system.cpu_transistors
                if growth_factor > 1:
                    doublings = math.log2(growth_factor)
                    actual_doubling_period = years / doublings if doublings > 0 else 0
                else:
                    actual_doubling_period = 0
            else:
                actual_doubling_period = 0

            results.append({
                'system_name': system.name,
                'year': system.year,
                'actual_transistors': system.cpu_transistors,
                'predicted_transistors': predicted,
                'accuracy_percent': accuracy,
                'years_from_base': years,
                'actual_doubling_period': actual_doubling_period,
                'moores_law_doubling_period': self.doubling_period,
                'ahead_behind': 'ahead' if accuracy > 105 else 'behind' if accuracy < 95 else 'on_track',
            })

        return results

    def calculate_effective_doubling_period(
        self,
        start_system: HardwareMetrics,
        end_system: HardwareMetrics,
    ) -> float:
        """Calculate the effective transistor doubling period between two systems.

        Args:
            start_system: Starting system
            end_system: Ending system

        Returns:
            Effective doubling period in years
        """
        years = end_system.year - start_system.year

        if years <= 0 or start_system.cpu_transistors <= 0 or end_system.cpu_transistors <= 0:
            return 0.0

        growth_factor = end_system.cpu_transistors / start_system.cpu_transistors

        if growth_factor <= 1:
            return 0.0

        doublings = math.log2(growth_factor)
        effective_period = years / doublings

        return effective_period

    def analyze_era_trends(
        self,
        systems: List[HardwareMetrics],
        era_length: int = 5,
    ) -> List[Dict[str, Any]]:
        """Analyze Moore's Law trends across different eras.

        Args:
            systems: List of hardware systems
            era_length: Length of each era in years

        Returns:
            List of era analyses
        """
        if not systems or len(systems) < 2:
            return []

        sorted_systems = sorted(systems, key=lambda x: x.year)
        start_year = sorted_systems[0].year
        end_year = sorted_systems[-1].year

        results = []
        current_year = start_year

        while current_year < end_year:
            era_end = current_year + era_length
            era_systems = [
                s for s in sorted_systems
                if current_year <= s.year < era_end
            ]

            if len(era_systems) >= 2:
                start_system = era_systems[0]
                end_system = era_systems[-1]

                doubling_period = self.calculate_effective_doubling_period(
                    start_system, end_system
                )

                # Calculate average transistor growth rate for this era
                years = end_system.year - start_system.year
                if years > 0 and start_system.cpu_transistors > 0:
                    growth_rate = (
                        (end_system.cpu_transistors / start_system.cpu_transistors)
                        ** (1 / years) - 1
                    ) * 100
                else:
                    growth_rate = 0

                results.append({
                    'era_start': current_year,
                    'era_end': era_end,
                    'era_label': f"{current_year}-{era_end}",
                    'system_count': len(era_systems),
                    'doubling_period': doubling_period,
                    'annual_growth_rate_percent': growth_rate,
                    'moores_law_adherence': 'strong' if 1.5 <= doubling_period <= 2.5 else 'moderate' if 1.0 <= doubling_period <= 3.5 else 'weak',
                    'start_transistors': start_system.cpu_transistors,
                    'end_transistors': end_system.cpu_transistors,
                })

            current_year = era_end

        return results

    def predict_future(
        self,
        base_system: HardwareMetrics,
        years_ahead: int = 10,
    ) -> List[Dict[str, Any]]:
        """Generate Moore's Law predictions for future years.

        Args:
            base_system: System to use as baseline
            years_ahead: Number of years to predict

        Returns:
            List of yearly predictions
        """
        predictions = []
        base_year = base_system.year
        base_transistors = base_system.cpu_transistors

        for year_offset in range(1, years_ahead + 1):
            target_year = base_year + year_offset
            predicted_transistors = self.predict_transistors(
                base_transistors, base_year, target_year
            )

            # Also predict process node (rough estimate)
            # Assume process node halves every 2 years (not exact but illustrative)
            process_reductions = year_offset / 2
            predicted_process = base_system.cpu_process_nm / (2 ** process_reductions)

            predictions.append({
                'year': target_year,
                'years_from_base': year_offset,
                'predicted_transistors': int(predicted_transistors),
                'predicted_process_nm': round(predicted_process, 1),
                'doublings_from_base': year_offset / self.doubling_period,
            })

        return predictions

    def compare_predictions_vs_reality(
        self,
        systems: List[HardwareMetrics],
        prediction_year: int,
    ) -> Dict[str, Any]:
        """Compare Moore's Law predictions with reality for a specific year.

        Args:
            systems: List of historical systems
            prediction_year: Year to analyze

        Returns:
            Comparison analysis
        """
        sorted_systems = sorted(systems, key=lambda x: x.year)

        # Find systems before and at the prediction year
        past_systems = [s for s in sorted_systems if s.year < prediction_year]
        target_systems = [s for s in sorted_systems if s.year == prediction_year]

        if not past_systems or not target_systems:
            return {}

        # Use a system from 5-10 years before as base
        base_system = None
        for s in reversed(past_systems):
            if prediction_year - s.year >= 5:
                base_system = s
                break

        if not base_system:
            base_system = past_systems[0]

        # Get the most advanced system in the target year
        target_system = max(target_systems, key=lambda s: s.cpu_transistors)

        predicted = self.predict_transistors(
            base_system.cpu_transistors,
            base_system.year,
            prediction_year,
        )

        accuracy = self.calculate_accuracy(predicted, target_system.cpu_transistors)

        return {
            'prediction_year': prediction_year,
            'base_system': base_system.name,
            'base_year': base_system.year,
            'base_transistors': base_system.cpu_transistors,
            'target_system': target_system.name,
            'actual_transistors': target_system.cpu_transistors,
            'predicted_transistors': predicted,
            'accuracy_percent': accuracy,
            'years_predicted': prediction_year - base_system.year,
        }
