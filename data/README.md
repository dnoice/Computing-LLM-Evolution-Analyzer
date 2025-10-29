# Data Directory

This directory contains comprehensive datasets tracking the evolution of computing hardware, GPUs, LLMs, and cloud infrastructure from 1965 to 2024.

## Directory Structure

```
data/
├── README.md                 # This file
├── SOURCES.md               # Data source documentation
├── CHANGELOG.md             # Data version history
├── schemas/                 # JSON schemas for validation
│   ├── gpu_schema.json
│   ├── hardware_schema.json
│   ├── llm_schema.json
│   └── cloud_schema.json
├── reference/              # Reference data and benchmarks
│   ├── benchmarks.json
│   ├── theoretical_limits.json
│   ├── industry_standards.json
│   └── conversion_factors.json
├── gpu/                    # GPU evolution data
│   ├── README.md
│   └── gpus.json
├── hardware/               # Historical computer systems
│   ├── README.md
│   └── systems.json
├── llm/                    # LLM model evolution
│   ├── README.md
│   └── models.json
└── cloud/                  # Cloud compute pricing
    ├── README.md
    └── instances.json
```

## Datasets Overview

### GPU Data (`gpu/gpus.json`)
Historical GPU specifications from 1999-2024 including:
- Performance metrics (TFLOPS FP32/FP16/INT8)
- Memory specifications (VRAM, bandwidth, type)
- Power consumption (TDP)
- Architectural features (tensor cores, RT cores)
- Pricing and availability

**Records**: 28 GPUs spanning 25 years
**Coverage**: NVIDIA, AMD, Intel
**Update Frequency**: Quarterly for new releases

### Hardware Systems (`hardware/systems.json`)
Computing system evolution from 1965-2024 including:
- CPU specifications (transistors, clock speed, process node)
- Memory and storage capacity
- Performance metrics (MIPS, FLOPS)
- Power consumption
- Historical pricing

**Records**: 30 systems spanning 59 years
**Coverage**: IBM, Intel, AMD, Apple, Commodore
**Update Frequency**: Annually for historical completeness

### LLM Models (`llm/models.json`)
Large Language Model evolution from 2018-2024 including:
- Model architecture and parameters
- Training metrics (tokens, compute, days)
- Capability scores (reasoning, coding, math, knowledge, multilingual)
- Context window size
- API pricing
- Open source status

**Records**: 22 models spanning 6 years
**Coverage**: OpenAI, Anthropic, Google, Meta, Mistral AI
**Update Frequency**: Monthly for active development period

### Cloud Instances (`cloud/instances.json`)
Cloud GPU instance pricing and specifications including:
- Provider (AWS, Azure, GCP)
- GPU configurations
- Compute resources (vCPUs, RAM, storage)
- Pricing models (on-demand, spot, reserved)
- Performance characteristics
- Optimization type (training vs inference)

**Records**: 17 instance types across 3 providers
**Coverage**: AWS, Azure, GCP
**Update Frequency**: Quarterly for pricing updates

## Data Quality

All datasets undergo validation against JSON schemas and include:
- ✅ Consistent field naming and types
- ✅ Comprehensive metadata
- ✅ Source attribution
- ✅ Temporal accuracy
- ✅ Cross-validation with public sources

## Usage

### Python Integration

```python
from llm_evolution.hardware_analyzer import HardwareAnalyzer
from llm_evolution.llm_analyzer import LLMAnalyzer
from llm_evolution.gpu_analyzer import GPUAnalyzer
from llm_evolution.cloud_cost_analyzer import CloudCostAnalyzer

# Load data through analyzers
hw_analyzer = HardwareAnalyzer()
llm_analyzer = LLMAnalyzer()
gpu_analyzer = GPUAnalyzer()
cloud_analyzer = CloudCostAnalyzer()

# Access parsed data
systems = hw_analyzer.systems
models = llm_analyzer.models
gpus = gpu_analyzer.gpus
instances = cloud_analyzer.instances
```

### Direct JSON Access

```python
import json
from pathlib import Path

# Load GPU data
with open('data/gpu/gpus.json', 'r') as f:
    gpus = json.load(f)

# Load LLM data
with open('data/llm/models.json', 'r') as f:
    llms = json.load(f)
```

## Data Validation

Validate data files against schemas:

```bash
# Validate all data files
python scripts/validate_data.py

# Validate specific dataset
python scripts/validate_data.py --dataset gpu
```

## Contributing

When adding or updating data:

1. Follow the existing JSON structure
2. Validate against the schema: `python scripts/validate_data.py`
3. Update CHANGELOG.md with changes
4. Add sources to SOURCES.md
5. Run quality checks: `python scripts/data_quality_check.py`

### Data Standards

- **Dates**: Use ISO 8601 format (YYYY-MM)
- **Numbers**: Use consistent units (see `reference/conversion_factors.json`)
- **Nulls**: Use `null` for missing data, not 0 or empty string
- **Naming**: Use snake_case for field names
- **Booleans**: Use `true`/`false`, not 1/0 or "yes"/"no"

## License

Data compiled from publicly available sources. See SOURCES.md for attribution.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Maintenance

**Last Updated**: 2024-10-29
**Maintainer**: Computing-LLM-Evolution-Analyzer Project
**Data Version**: 2.1.0
