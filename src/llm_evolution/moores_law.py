"""Moore's Law analysis and predictions."""

from typing import List, Dict, Any, Optional
import math
from datetime import datetime

from .models import HardwareMetrics


class MooresLawAnalyzer:
    """Analyzer for Moore's Law predictions and comparisons."""

    # Physical and practical limits
    MINIMUM_PROCESS_NM = 0.5  # Absolute physical limit (atomic scale)
    PRACTICAL_LIMIT_YEAR = 2030  # Year when Moore's Law significantly slows
    MAX_REASONABLE_YEARS = 20  # Maximum years for reasonable predictions
    MAX_TRANSISTOR_COUNT = 1e15  # 1 quadrillion transistors (far future limit)

    def __init__(self, doubling_period: float = 2.0):
        """Initialize Moore's Law analyzer.

        Args:
            doubling_period: Years for transistor count doubling (default 2.0)
        """
        self.doubling_period = doubling_period

    def get_adjusted_doubling_period(self, year: int) -> float:
        """Calculate adjusted doubling period based on year.

        Moore's Law has been slowing down:
        - Pre-2020: ~2 years
        - 2020-2025: ~2.5 years
        - 2025-2030: ~3 years
        - 2030+: ~4-5 years (approaching physical limits)

        Args:
            year: Year to calculate doubling period for

        Returns:
            Adjusted doubling period in years
        """
        if year < 2020:
            return 2.0
        elif year < 2025:
            return 2.5
        elif year < 2030:
            return 3.0
        elif year < 2035:
            return 4.0
        else:
            # Beyond 2035, Moore's Law is expected to be largely dead
            return 5.0

    def predict_transistors(
        self,
        base_transistors: int,
        base_year: int,
        target_year: int,
        use_realistic_slowdown: bool = True,
    ) -> float:
        """Predict transistor count using Moore's Law.

        Args:
            base_transistors: Starting transistor count
            base_year: Starting year
            target_year: Target year for prediction
            use_realistic_slowdown: If True, applies realistic Moore's Law slowdown

        Returns:
            Predicted transistor count
        """
        if not use_realistic_slowdown:
            # Original naive calculation
            years = target_year - base_year
            doublings = years / self.doubling_period
            predicted = base_transistors * (2 ** doublings)
        else:
            # Realistic calculation with slowdown
            current_transistors = float(base_transistors)
            current_year = base_year

            while current_year < target_year:
                # Get the doubling period for this time period
                doubling_period = self.get_adjusted_doubling_period(current_year)

                # Calculate growth for this year
                years_to_advance = min(1, target_year - current_year)
                doublings = years_to_advance / doubling_period
                current_transistors *= (2 ** doublings)

                current_year += years_to_advance

            predicted = current_transistors

        # Cap at maximum realistic transistor count
        predicted = min(predicted, self.MAX_TRANSISTOR_COUNT)

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
            List of yearly predictions with warnings for unrealistic projections
        """
        predictions = []
        base_year = base_system.year
        base_transistors = base_system.cpu_transistors
        base_process = base_system.cpu_process_nm

        for year_offset in range(1, years_ahead + 1):
            target_year = base_year + year_offset

            # Use realistic slowdown for predictions
            predicted_transistors = self.predict_transistors(
                base_transistors, base_year, target_year, use_realistic_slowdown=True
            )

            # Predict process node with realistic constraints
            # Process node reduction slows down significantly after 2025
            if target_year < 2025:
                # Still following ~2 year cadence
                process_reductions = year_offset / 2
            elif target_year < 2030:
                # Slowing to ~3 year cadence
                years_since_2025 = target_year - 2025
                reductions_to_2025 = (2025 - base_year) / 2
                reductions_after_2025 = years_since_2025 / 3
                process_reductions = reductions_to_2025 + reductions_after_2025
            else:
                # After 2030, very slow progress
                years_to_2030 = min(2030 - base_year, year_offset)
                years_after_2030 = max(0, year_offset - years_to_2030)

                reductions_to_2025 = min((2025 - base_year), years_to_2030) / 2
                reductions_2025_2030 = max(0, min(5, years_to_2030 - (2025 - base_year))) / 3
                reductions_after_2030 = years_after_2030 / 5  # Very slow

                process_reductions = reductions_to_2025 + reductions_2025_2030 + reductions_after_2030

            predicted_process = base_process / (2 ** process_reductions)

            # Apply physical minimum
            predicted_process = max(predicted_process, self.MINIMUM_PROCESS_NM)

            # Determine prediction confidence/warnings
            warning = None
            confidence = "high"

            if year_offset > self.MAX_REASONABLE_YEARS:
                warning = "highly_speculative"
                confidence = "very_low"
            elif target_year > self.PRACTICAL_LIMIT_YEAR + 10:
                warning = "speculative"
                confidence = "low"
            elif target_year > self.PRACTICAL_LIMIT_YEAR:
                warning = "uncertain"
                confidence = "medium"

            # Check if we hit physical limits
            if predicted_process <= self.MINIMUM_PROCESS_NM:
                warning = "physical_limit_reached"

            if predicted_transistors >= self.MAX_TRANSISTOR_COUNT:
                warning = "transistor_limit_reached"

            # Calculate actual doublings considering slowdown
            doublings = 0
            temp_transistors = float(base_transistors)
            for y in range(base_year, target_year):
                doubling_period = self.get_adjusted_doubling_period(y)
                doublings += 1 / doubling_period

            predictions.append({
                'year': target_year,
                'years_from_base': year_offset,
                'predicted_transistors': int(predicted_transistors),
                'predicted_process_nm': round(predicted_process, 1),
                'doublings_from_base': round(doublings, 2),
                'confidence': confidence,
                'warning': warning,
                'note': self._get_prediction_note(target_year, warning),
            })

        return predictions

    def _get_prediction_note(self, year: int, warning: Optional[str]) -> str:
        """Generate explanatory note for prediction.

        Args:
            year: Prediction year
            warning: Warning level

        Returns:
            Human-readable note
        """
        if warning == "physical_limit_reached":
            return "Physical limit: Process node cannot go smaller (atomic scale)"
        elif warning == "transistor_limit_reached":
            return "Practical limit: Transistor count capped at realistic maximum"
        elif warning == "highly_speculative":
            return "Highly speculative: Requires breakthrough technologies"
        elif warning == "speculative":
            return "Speculative: Assumes continued Moore's Law beyond expected end"
        elif warning == "uncertain":
            return "Uncertain: Moore's Law expected to slow significantly"
        elif year >= 2030:
            return "Note: Predictions beyond 2030 assume paradigm shifts (3D, photonics, etc.)"
        else:
            return ""

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
