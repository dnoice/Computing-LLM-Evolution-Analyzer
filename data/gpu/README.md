# GPU Evolution Data

This directory contains comprehensive historical data on GPU specifications and evolution from 1999 to 2024.

## Dataset: gpus.json

### Overview

Tracks the evolution of Graphics Processing Units (GPUs) across 25 years, documenting the transformation from simple graphics accelerators to powerful compute engines driving AI and scientific computing.

### Key Milestones Covered

- **1999**: First GPU (GeForce 256) introducing hardware T&L
- **2006**: First unified shader architecture (GeForce 8800 GTX) with CUDA
- **2008**: First GDDR5 memory (Radeon HD 4870)
- **2015**: First HBM memory (Radeon R9 Fury X)
- **2018**: First RT cores and Tensor cores (RTX 2080 Ti)
- **2022**: Ada Lovelace architecture with DLSS 3.0 (RTX 4090)

### Data Schema

Each GPU record contains:

```json
{
  "name": "string",                      // GPU model name
  "year": integer,                       // Release year
  "manufacturer": "string",              // NVIDIA | AMD | Intel
  "series": "string",                    // Product series
  "architecture": "string",              // Architecture codename
  "process_nm": integer,                 // Process node in nanometers
  "transistors_millions": integer,       // Transistor count
  "die_size_mm2": number,               // Die size in mm²

  // Compute units
  "cuda_cores": integer|null,           // NVIDIA CUDA cores
  "stream_processors": integer|null,    // AMD stream processors
  "execution_units": integer|null,      // Intel execution units
  "tensor_cores": integer|null,         // Tensor cores for AI
  "rt_cores": integer|null,             // Ray tracing cores

  // Clock speeds (MHz)
  "base_clock_mhz": integer,
  "boost_clock_mhz": integer,

  // Memory specifications
  "vram_mb": integer,                   // Video RAM in MB
  "memory_type": "string",              // SDR | DDR | GDDR3-6X | HBM | HBM2
  "memory_bus_width": integer,          // Bus width in bits
  "memory_bandwidth_gbps": number,      // Bandwidth in GB/s
  "memory_clock_mhz": integer,          // Memory clock speed

  // Performance metrics
  "tflops_fp32": number,                // FP32 compute in TFLOPS
  "tflops_fp16": number,                // FP16 compute in TFLOPS
  "tflops_int8": number,                // INT8 compute in TFLOPS
  "ray_tracing_tflops": number|null,    // RT performance

  // Power and connectivity
  "tdp_watts": integer,                 // Thermal Design Power
  "power_connectors": "string",         // Power connector requirements

  // Economics
  "launch_price_usd": integer,          // MSRP at launch

  // Graphics API support
  "directx_version": "string",
  "opengl_version": "string",
  "vulkan_support": boolean,

  // Advanced features
  "ray_tracing_support": boolean,
  "dlss_support": boolean,             // NVIDIA DLSS
  "fsr_support": boolean,              // AMD FSR
  "xess_support": boolean,             // Intel XeSS

  // Display capabilities
  "max_displays": integer,
  "max_resolution": "string",
  "release_date": "YYYY-MM",
  "notes": "string"
}
```

### Data Collection Methodology

Data sourced from:
1. Official manufacturer specifications
2. TechPowerUp GPU Database
3. AnandTech reviews and benchmarks
4. Tom's Hardware GPU specifications
5. Hardware Unboxed testing data

### Coverage Statistics

- **Total GPUs**: 28
- **Manufacturers**: NVIDIA (18), AMD (9), Intel (1)
- **Time Span**: 1999-2024 (25 years)
- **Architecture Generations**: 20+ distinct architectures
- **Process Nodes**: 220nm to 5nm

### Key Metrics Evolution

| Metric | 1999 (GeForce 256) | 2024 (RTX 4090) | Growth Factor |
|--------|-------------------|-----------------|---------------|
| TFLOPS FP32 | 0.48 | 82.58 | 172x |
| VRAM | 32 MB | 24 GB | 768x |
| Memory Bandwidth | 2.9 GB/s | 1008 GB/s | 348x |
| Transistors | 23M | 76,300M | 3,317x |
| Process Node | 220nm | 5nm | 44x smaller |
| TDP | 30W | 450W | 15x |

### Usage Examples

#### Load and analyze GPU data

```python
from llm_evolution.gpu_analyzer import GPUAnalyzer

analyzer = GPUAnalyzer()

# Get all GPUs
gpus = analyzer.gpus

# Filter by manufacturer
nvidia_gpus = [g for g in gpus if g.manufacturer == "NVIDIA"]

# Calculate performance growth
cagr_results = analyzer.calculate_all_cagrs()
print(f"TFLOPS CAGR: {cagr_results['tflops_fp32'].cagr_percent:.2f}%")

# Get manufacturer comparison
comparison = analyzer.get_manufacturer_comparison()

# Find architectural milestones
milestones = analyzer.get_architectural_milestones()
```

#### Query specific generations

```python
# Get RTX 40-series cards
rtx_40_series = [g for g in gpus if g.series == "GeForce RTX 40"]

# Find first GPU with ray tracing
first_rt = next(g for g in gpus if g.ray_tracing_support)
print(f"First RT GPU: {first_rt.name} ({first_rt.year})")

# Calculate efficiency trends
efficiency = analyzer.get_efficiency_trends()
```

### Data Quality Notes

- **Accuracy**: All specifications verified against multiple sources
- **Completeness**: Some early GPUs have `null` values for metrics that didn't exist yet (e.g., tensor_cores)
- **Precision**: FP16/INT8 performance set to 0 for GPUs without dedicated hardware
- **Pricing**: Launch MSRP in USD, not adjusted for inflation
- **Selection Bias**: Focuses on flagship and significant mid-range models

### Update History

- **v2.1.0 (2024-10-29)**: Added Intel Arc A770, updated RTX 40 Super series
- **v2.0.0 (2024-06)**: Restructured schema, added tensor core counts
- **v1.5.0 (2023-12)**: Added RDNA 3 architecture GPUs
- **v1.0.0 (2023-06)**: Initial dataset with 25 GPUs

### Related Data

- See `../cloud/instances.json` for cloud GPU pricing
- See `../reference/benchmarks.json` for real-world performance data
- See `../hardware/systems.json` for CPU comparison

### Known Limitations

1. **Early GPUs**: Limited compute metrics for pre-CUDA/Stream Processor era
2. **Variants**: Only includes one variant per model (not all VRAM/clock configurations)
3. **Professional**: Primarily consumer GPUs; limited Quadro/Radeon Pro coverage
4. **Regional**: Pricing and availability may vary by region
5. **Mobile**: Desktop GPUs only; no mobile/laptop variants

### Contributing

To add a GPU:
1. Follow the schema exactly
2. Verify all specs with manufacturer datasheet
3. Include release date and notable features in notes
4. Cross-reference with multiple sources
5. Validate with `python scripts/validate_data.py --dataset gpu`

### References

- NVIDIA GPU specifications: https://www.nvidia.com/en-us/geforce/graphics-cards/
- AMD GPU specifications: https://www.amd.com/en/graphics/
- Intel Arc specifications: https://www.intel.com/content/www/us/en/products/details/discrete-gpus/arc.html
- TechPowerUp GPU Database: https://www.techpowerup.com/gpu-specs/
