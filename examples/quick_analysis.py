#!/usr/bin/env python3
"""Quick analysis example script."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_evolution.hardware_analyzer import HardwareAnalyzer
from llm_evolution.llm_analyzer import LLMAnalyzer
from llm_evolution.moores_law import MooresLawAnalyzer

def main():
    """Run quick analysis."""
    print("Computing & LLM Evolution Analyzer - Quick Analysis")
    print("=" * 60)

    # Hardware Analysis
    print("\n1. HARDWARE ANALYSIS")
    print("-" * 60)
    hw = HardwareAnalyzer()

    print(f"Total systems: {len(hw.systems)}")
    print(f"Year range: {hw.systems[0].year} - {hw.systems[-1].year}")

    cagr_results = hw.calculate_all_cagrs()
    print("\nCAGR Results:")
    for metric, result in cagr_results.items():
        print(f"  {metric:20s}: {result.cagr_percent:6.2f}% "
              f"({result.growth_factor:.1f}x growth)")

    # LLM Analysis
    print("\n2. LLM ANALYSIS")
    print("-" * 60)
    llm = LLMAnalyzer()

    print(f"Total models: {len(llm.models)}")
    print(f"Year range: {llm.models[0].year} - {llm.models[-1].year}")

    llm_cagr = llm.calculate_all_cagrs()
    print("\nCAGR Results:")
    for metric, result in llm_cagr.items():
        print(f"  {metric:25s}: {result.cagr_percent:6.2f}% "
              f"({result.growth_factor:.1f}x growth)")

    # Moore's Law
    print("\n3. MOORE'S LAW ANALYSIS")
    print("-" * 60)
    moores = MooresLawAnalyzer()

    result = hw.analyze_moores_law()
    print(f"Period: {result.start_year} - {result.end_year}")
    print(f"Actual transistors: {result.end_value:,.0f}")
    print(f"Moore's Law prediction: {result.moores_law_predicted:,.0f}")
    print(f"Accuracy: {result.moores_law_accuracy:.2f}%")

    print("\n" + "=" * 60)
    print("Analysis complete!")


if __name__ == "__main__":
    main()
