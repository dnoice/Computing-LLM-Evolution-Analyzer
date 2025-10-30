# Computing & LLM Evolution Analyzer

## Overview

A comprehensive, feature-rich Python analysis tool for comparing computing hardware capabilities and Large Language Model (LLM) performance across different time periods. Built with modern Python practices and featuring a beautiful command-line interface powered by Rich.

## Features

### Comprehensive Analysis
- **Hardware Metrics**: CPU, RAM, Storage, Power consumption, Architecture
- **GPU Metrics**: TFLOPS (FP32/FP16/INT8), VRAM, Memory bandwidth, Ray tracing, Tensor cores
- **LLM Capabilities**: Parameters, context window, training compute, capability scores
- **Cloud Cost Analysis**: AWS, Azure, GCP pricing, training/inference cost estimation, spot savings
- **Moore's Law Analysis**: Prediction accuracy and actual growth rates
- **Economic Analysis**: Cost per performance, price trends
- **Scaling Laws**: Chinchilla optimal, compute efficiency, memory requirements
- **CAGR Calculations**: Compound Annual Growth Rates for all key metrics

### Beautiful CLI Interface
- **Rich Module Integration**: Color-coded tables, panels, and progress bars
- **Interactive Menu System**: User-friendly navigation
- **Real-time Progress Tracking**: Visual feedback for long operations
- **Formatted Output**: Professional tables and structured display
- **Error Handling**: Graceful error messages with full tracebacks

### Advanced Visualizations
- Hardware performance evolution (log scale)
- GPU performance and memory evolution
- GPU efficiency trends (TFLOPS/Watt)
- GPU manufacturer comparisons (NVIDIA, AMD, Intel)
- GPU price vs performance analysis
- Cost efficiency comparisons
- Energy efficiency trends
- Cloud cost comparisons (AWS vs Azure vs GCP)
- Spot savings analysis charts
- Training cost breakdown visualizations
- GPU price evolution across cloud providers
- Cost efficiency ranking charts
- LLM capability radar charts
- Moore's Law prediction vs reality
- CAGR heatmaps
- Growth factor bar charts
- Training compute evolution

### Multiple Export Formats
- JSON (structured data)
- CSV (tabular data)
- Markdown (documentation)
- Text (plain text reports)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/Computing-LLM-Evolution-Analyzer.git
cd Computing-LLM-Evolution-Analyzer

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive Web Dashboard

Launch the beautiful web dashboard for the best experience:

```bash
cd dashboard
python serve.py
```

Then open your browser to `http://localhost:8000`

**Features:**
- Beautiful, responsive design with dark mode
- Interactive charts powered by Chart.js
- Real-time data filtering and comparisons
- Mobile-first responsive layout
- Cost calculator for LLM training
- Moore's Law predictions with visualizations

See [dashboard/README.md](dashboard/README.md) for more details.

### Interactive CLI Mode

Run the command-line application:

```bash
python main.py
```

### Python API Examples

#### Hardware Analysis

```python
from src.llm_evolution.hardware_analyzer import HardwareAnalyzer

# Initialize analyzer
hw = HardwareAnalyzer()

# Calculate CAGR for all metrics
cagr_results = hw.calculate_all_cagrs()

# Analyze specific metric
transistor_growth = hw.analyze_metric_growth('cpu_transistors')
print(f"Transistor CAGR: {transistor_growth.cagr_percent:.2f}%")
```

#### LLM Analysis

```python
from src.llm_evolution.llm_analyzer import LLMAnalyzer

# Initialize analyzer
llm = LLMAnalyzer()

# Analyze parameter scaling
param_growth = llm.analyze_metric_growth('parameters_billions')
print(f"Parameter CAGR: {param_growth.cagr_percent:.2f}%")

# Chinchilla optimal analysis
chinchilla = llm.analyze_chinchilla_optimal()
```

#### GPU Analysis

```python
from src.llm_evolution.gpu_analyzer import GPUAnalyzer

# Initialize analyzer
gpu = GPUAnalyzer()

# Calculate CAGR for GPU metrics
gpu_cagr = gpu.calculate_all_cagrs()
print(f"TFLOPS CAGR: {gpu_cagr['tflops_fp32'].cagr_percent:.2f}%")

# Compare manufacturers
comparison = gpu.get_manufacturer_comparison()
for mfr, stats in comparison.items():
    print(f"{mfr}: {stats['count']} GPUs, Avg {stats['avg_tflops_fp32']:.1f} TFLOPS")
```

#### Cloud Cost Analysis

```python
from src.llm_evolution.cloud_cost_analyzer import CloudCostAnalyzer

# Initialize analyzer
cloud = CloudCostAnalyzer()

# Compare providers for training
training_comparison = cloud.compare_providers_for_training(
    training_hours=100,
    use_spot=True
)
for provider, data in training_comparison.items():
    print(f"{provider}: ${data['total_cost_usd']:.2f} using {data['instance_type']}")

# Estimate LLM training cost
cost_estimate = cloud.estimate_llm_training_cost(
    parameters_billions=7,
    training_tokens_billions=1000,
    use_spot=True
)
print(f"Training 7B model: ${cost_estimate['total_cost_usd']:,.2f}")
print(f"Instance: {cost_estimate['instance_type']} ({cost_estimate['provider']})")
print(f"Training days: {cost_estimate['training_days']:.1f}")

# Analyze spot savings
savings = cloud.get_spot_savings_analysis()
for entry in savings[:5]:
    print(f"{entry['provider']} {entry['instance_type']}: {entry['savings_percent']:.1f}% savings")

# Cost efficiency ranking
ranking = cloud.get_cost_efficiency_ranking(workload_type='training')
for i, instance in enumerate(ranking[:5], 1):
    print(f"{i}. {instance['provider']} {instance['instance_type']}: {instance['tflops_per_dollar']:.2f} TFLOPS/$")
```

## Project Structure

```
Computing-LLM-Evolution-Analyzer/
├── dashboard/                # Interactive web dashboard
│   ├── index.html           # Main dashboard page
│   ├── serve.py             # Development server
│   ├── README.md            # Dashboard documentation
│   └── assets/
│       ├── css/
│       │   └── custom.css   # Custom styles with CSS variables
│       ├── js/
│       │   ├── main.js      # Alpine.js app logic
│       │   ├── charts.js    # Chart.js configurations
│       │   └── data-loader.js  # Data loading utilities
│       └── images/
│           └── logo.svg     # SVG logo
├── data/                    # Data files
│   ├── hardware/
│   │   ├── systems.json    # Hardware specifications (1965-2024)
│   │   └── README.md       # Hardware dataset documentation
│   ├── gpu/
│   │   ├── gpus.json       # GPU specifications (1999-2024)
│   │   └── README.md       # GPU dataset documentation
│   ├── llm/
│   │   ├── models.json     # LLM specifications (2018-2024)
│   │   └── README.md       # LLM dataset documentation
│   ├── cloud/
│   │   ├── instances.json  # Cloud instance pricing (AWS, Azure, GCP)
│   │   └── README.md       # Cloud dataset documentation
│   ├── schemas/            # JSON validation schemas
│   │   ├── hardware_schema.json
│   │   ├── gpu_schema.json
│   │   ├── llm_schema.json
│   │   └── cloud_schema.json
│   ├── reference/          # Reference data
│   │   ├── benchmarks.json
│   │   ├── theoretical_limits.json
│   │   └── conversion_factors.json
│   ├── README.md           # Data directory overview
│   ├── SOURCES.md          # Data sources and attribution
│   └── CHANGELOG.md        # Data version history
├── src/
│   └── llm_evolution/      # Main package
│       ├── models.py       # Data models
│       ├── hardware_analyzer.py
│       ├── gpu_analyzer.py
│       ├── llm_analyzer.py
│       ├── cloud_cost_analyzer.py  # Cloud cost analysis
│       ├── moores_law.py
│       ├── cli.py          # Interactive CLI
│       ├── visualizations/ # Plotting modules
│       ├── exports/        # Export modules
│       ├── data/           # Data loading utilities
│       └── utils/          # Utility functions
├── scripts/                # Data validation and utilities
│   ├── validate_data.py    # Schema validation tool
│   ├── data_statistics.py  # Statistics generation
│   └── README.md           # Scripts documentation
├── docs/                   # Documentation
│   ├── audits/             # System audits
│   └── PR-SUMMARY.md       # Project status
├── examples/               # Example scripts
│   └── quick_analysis.py   # Quick start example
├── output/                 # Generated outputs
├── main.py                 # Main entry point
├── setup.py                # Package configuration
├── requirements.txt        # Dependencies
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
└── README.md               # This file
```

## Data Included

### Hardware Dataset (1965-2025)
- IBM System/360, Intel 4004, Apple II, IBM PC
- Intel Pentium through Core i9 series
- AMD Ryzen series, AMD EPYC Turin (2025)
- Apple M-series chips
- 49 systems spanning 60 years

### GPU Dataset (1999-2024)
- NVIDIA: GeForce 256, GTX series, RTX 20/30/40 series
- AMD: Radeon 7500, HD series, RX 5000/6000/7000 series
- Intel: Arc A770
- 40 GPUs spanning 25 years
- Comprehensive metrics: TFLOPS, VRAM, transistors, process nodes, efficiency

### LLM Dataset (2018-2024)
- BERT, GPT-2, GPT-3, GPT-3.5, GPT-4 series
- Claude series (Anthropic) - including Claude Opus 4.1, Claude Sonnet 4.5
- LLaMA series (Meta) - including Llama 3.3 70B
- Gemini series (Google)
- Mistral models
- 26 major models with comprehensive metrics

### Cloud Instance Dataset (2017-2024)
- **AWS**: P3, P4d, P5, G5, Inf2 instances
- **Azure**: NCv3, NDv4, ND A100 v4, NCasT4 v3
- **GCP**: A2, N1, G2 instances
- 22 instances across 3 major cloud providers
- Comprehensive metrics: GPU specs, pricing (on-demand, spot, reserved), TFLOPS, memory, interconnect
- Training and inference-optimized configurations

### Data Infrastructure

The project includes a comprehensive data infrastructure with:

- **📚 Complete Documentation**: Detailed README files for each dataset with usage examples, coverage statistics, and historical context
- **✅ Validation Schemas**: JSON schemas for all datasets ensuring data quality and consistency
- **📊 Reference Data**: Benchmarks, theoretical limits, and conversion factors for analysis
- **🔍 Quality Tools**: Automated validation and statistics generation scripts
- **📝 Source Attribution**: Complete documentation of data sources and methodology
- **📈 Version Control**: Changelog tracking all dataset updates and improvements

**Quick Links:**
- [Data Directory Overview](data/README.md) - Comprehensive dataset documentation
- [Validation Scripts](scripts/README.md) - Data quality and validation tools
- [Data Sources](data/SOURCES.md) - Source attribution and methodology
- [Changelog](data/CHANGELOG.md) - Version history and updates

**Validate Data:**
```bash
# Validate all datasets
python scripts/validate_data.py

# Generate statistics report
python scripts/data_statistics.py
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

### Completed Features
- [x] Hardware evolution analysis (CPU, RAM, Storage)
- [x] GPU comprehensive analysis (TFLOPS, VRAM, efficiency)
- [x] LLM scaling analysis
- [x] Moore's Law analysis
- [x] Interactive CLI with Rich integration
- [x] CAGR calculations for all metrics
- [x] Advanced visualizations (charts, heatmaps, radar plots)
- [x] Multi-format exports (JSON, CSV, Markdown, Text)
- [x] GPU manufacturer comparisons
- [x] Economic analysis (cost per performance)
- [x] Cloud cost analysis engine (AWS, Azure, GCP)
- [x] Training and inference cost estimation
- [x] Spot instance savings analysis
- [x] Provider comparison tools
- [x] Enhanced energy consumption analysis (power_watts tracking across all systems)
- [x] Extended dataset coverage (2025+ models including AMD EPYC Turin, Llama 3.3 70B, Claude Opus 4.1, Claude Sonnet 4.5)

### Recently Completed
- [x] Interactive web dashboard (v1.0)
  - Beautiful responsive design with Tailwind CSS
  - Chart.js visualizations for all analyzers
  - Dark mode support
  - Mobile-first design
  - Interactive cost calculator
  - Real-time filtering and comparisons

### Planned Features
- [ ] Real-time data updates from APIs
- [ ] Carbon footprint analysis
- [ ] Benchmark database integration
- [ ] Custom dataset support
- [ ] API endpoint for programmatic access
- [ ] Comparative analysis reports (PDF generation)
- [ ] Cost optimization recommendations
- [ ] Multi-cloud workload optimization
- [ ] Historical cost trend predictions

## Version

**Version 2.1.0** - Added Cloud Cost Analysis Engine with support for AWS, Azure, and GCP. Includes training/inference cost estimation, spot savings analysis, and comprehensive provider comparisons.
