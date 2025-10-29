# Cloud Compute Instance Data

This directory contains cloud GPU instance specifications and pricing data for AWS, Azure, and Google Cloud Platform.

## Dataset: instances.json

### Overview

Tracks cloud GPU instance offerings across three major providers, enabling cost analysis, provider comparison, and training/inference cost estimation for ML/AI workloads.

### Provider Coverage

- **AWS**: P3, P4d, P5, G5, Inf2 families
- **Azure**: NCv3, NDv4, ND A100 v4, NCasT4 v3 families
- **GCP**: A2, N1, G2 families

### Data Schema

Each cloud instance record contains:

```json
{
  "provider": "string",                     // AWS | Azure | GCP
  "instance_type": "string",                // Instance name/SKU
  "instance_family": "string",              // Product family
  "year": integer,                          // Release year
  "region": "string",                       // Primary region

  // GPU configuration
  "gpu_count": integer,                     // Number of GPUs
  "gpu_model": "string",                    // V100 | A100 | H100 | T4 | A10G | L4 | Inferentia2
  "gpu_memory_gb": integer,                 // Memory per GPU

  // Compute resources
  "vcpus": integer,                         // Virtual CPUs
  "ram_gb": number,                         // System RAM in GB
  "storage_gb": integer,                    // Local storage
  "storage_type": "string",                 // EBS | SSD | NVMe SSD | Persistent Disk

  // Network and interconnect
  "network_bandwidth_gbps": number,         // Network bandwidth
  "gpu_interconnect": "string",             // NVLink | NVSwitch | InfiniBand
  "gpu_interconnect_bandwidth_gbps": number, // Interconnect speed

  // Performance metrics
  "tflops_fp32": number,                    // FP32 compute total
  "tflops_fp16": number,                    // FP16 compute total
  "tflops_int8": number,                    // INT8 compute total
  "tensor_cores": boolean,                  // Tensor core availability

  // Pricing (USD)
  "price_ondemand_hourly": number,          // On-demand $/hour
  "price_spot_hourly": number,              // Spot/preemptible $/hour
  "price_1yr_reserved_hourly": number,      // 1-year commitment $/hour
  "price_3yr_reserved_hourly": number,      // 3-year commitment $/hour

  // Optimization flags
  "ml_optimized": boolean,                  // ML/AI optimized
  "inference_optimized": boolean,           // Inference focused
  "training_optimized": boolean,            // Training focused
  "supports_multi_node": boolean,           // Multi-instance training

  // Additional costs
  "storage_cost_per_gb_month": number,      // Storage cost
  "egress_cost_per_gb": number,            // Data transfer out cost

  // Metadata
  "availability": "string",                 // GA | Preview | Limited
  "notes": "string"                         // Key features
}
```

### Data Collection Methodology

Data sourced from:
1. Official cloud provider pricing pages
2. Instance specification documentation
3. GPU manufacturer datasheets
4. Cloud provider calculators
5. Regular pricing audits (quarterly)

### Coverage Statistics

- **Total Instances**: 17
- **Providers**: AWS (6), Azure (4), GCP (7)
- **GPU Models**: V100, A100 (40GB/80GB), H100, T4, A10G, L4, Inferentia2
- **Instance Families**: 13
- **Year Range**: 2017-2023

### Pricing Evolution

| GPU | Year | Provider | $/hr (On-Demand) | $/hr (2024) | Change |
|-----|------|----------|-----------------|-------------|---------|
| V100 (1x) | 2017 | AWS P3 | $3.06 | $3.06 | Same |
| A100 40GB (8x) | 2020 | AWS P4d | $32.77 | $32.77 | Same |
| H100 80GB (8x) | 2023 | AWS P5 | $98.32 | $98.32 | New |

### Cost Comparison (8x GPU Training Instances)

| Provider | Instance | GPU | On-Demand $/hr | Spot $/hr | Savings |
|----------|----------|-----|----------------|-----------|---------|
| AWS | p5.48xlarge | H100 80GB | $98.32 | $29.50 | 70% |
| AWS | p4d.24xlarge | A100 40GB | $32.77 | $9.83 | 70% |
| Azure | ND96amsr_A100_v4 | A100 80GB | $32.77 | $6.55 | 80% |
| GCP | a2-ultragpu-8g | A100 80GB | $33.22 | $9.97 | 70% |

### Usage Examples

#### Load and analyze cloud instance data

```python
from llm_evolution.cloud_cost_analyzer import CloudCostAnalyzer

analyzer = CloudCostAnalyzer()

# Get all instances
instances = analyzer.instances

# Compare providers for training
training_comparison = analyzer.compare_providers_for_training(
    training_hours=100,
    use_spot=True
)

# Compare providers for inference
inference_comparison = analyzer.compare_providers_for_inference(
    requests_per_second=10,
    avg_tokens_per_request=100,
    tokens_per_second_per_gpu=50,
    days=30
)
```

#### Estimate LLM training costs

```python
# Estimate training a 7B parameter model
estimate = analyzer.estimate_llm_training_cost(
    parameters_billions=7,
    training_tokens_billions=1000,
    use_spot=True
)

print(f"Total Cost: ${estimate['total_cost_usd']:,.2f}")
print(f"Training Days: {estimate['training_days']:.1f}")
print(f"Provider: {estimate['provider']}")
print(f"Instance: {estimate['instance_type']}")
```

#### Find most cost-efficient instances

```python
# Get cost efficiency ranking for training
ranking = analyzer.get_cost_efficiency_ranking(workload_type='training')

for i, instance in enumerate(ranking[:5], 1):
    print(f"{i}. {instance['provider']} {instance['instance_type']}")
    print(f"   TFLOPS/$: {instance['tflops_per_dollar']:.2f}")
    print(f"   Price: ${instance['price_ondemand_hourly']:.2f}/hr")
```

#### Analyze spot savings

```python
# Get spot instance savings analysis
savings = analyzer.get_spot_savings_analysis()

total_annual_savings = sum(s['annual_savings_usd'] for s in savings)
print(f"Total potential annual savings: ${total_annual_savings:,.0f}")
```

### Key Insights

#### Training Cost Comparison

For 100-hour training job (8x GPU):
- **AWS P5 (H100)**: $9,832 on-demand, $2,950 spot (fastest)
- **AWS P4d (A100 40GB)**: $3,277 on-demand, $983 spot
- **Azure ND A100 v4 (80GB)**: $3,277 on-demand, $655 spot (best value)
- **GCP A2 Ultra (80GB)**: $3,322 on-demand, $997 spot

#### Spot Instance Strategy

- **Average savings**: 70-80% vs on-demand
- **Best for**: Training workloads with checkpointing
- **Risks**: Interruption (mitigate with automatic resume)
- **Not recommended**: Production inference serving

#### GPU Generation Impact

| GPU Generation | Representative | TFLOPS/$ (on-demand) | Performance/Watt |
|---------------|----------------|---------------------|------------------|
| Volta (2017) | V100 | 5.1 | Baseline |
| Ampere (2020) | A100 40GB | 4.8 | 2.5x |
| Hopper (2023) | H100 80GB | 5.5 | 4x |

### Provider Differentiation

#### AWS
- **Strengths**: Fastest availability of new hardware, EFA networking
- **Best for**: Cutting-edge training, large-scale deployments
- **Pricing**: Premium for latest hardware

#### Azure
- **Strengths**: Best spot pricing, InfiniBand on ND-series
- **Best for**: Cost-sensitive large-scale training
- **Pricing**: Competitive spot instances

#### GCP
- **Strengths**: Flexible configurations, good spot availability
- **Best for**: Experimentation, smaller workloads
- **Pricing**: Mid-range, good spot rates

### Data Quality Notes

- **Pricing**: Updated quarterly; may vary by region and commitment
- **Spot Pricing**: Average historical spot prices; actual may vary
- **Performance**: Manufacturer specs; real-world may differ
- **Availability**: Regional availability varies
- **Quotas**: Subject to cloud provider quotas and approvals

### Update History

- **v2.1.0 (2024-10-29)**: Verified all pricing, added notes on H100 availability
- **v2.0.0 (2024-06)**: Added AWS P5 instances, updated Azure pricing
- **v1.5.0 (2024-01)**: Added GCP G2 L4 instances
- **v1.0.0 (2023-09)**: Initial dataset with 15 instances

### Related Data

- See `../gpu/gpus.json` for GPU specifications
- See `../llm/models.json` for training requirements
- See `../reference/benchmarks.json` for real-world performance

### Known Limitations

1. **Regional Variation**: Pricing varies 10-30% by region
2. **Spot Volatility**: Spot prices fluctuate based on demand
3. **Quotas**: High-end instances require quota increases
4. **Availability**: New instances may have limited availability
5. **Networking**: Network performance varies by region/AZ
6. **Egress**: Inter-region data transfer adds significant cost

### Cost Optimization Strategies

1. **Spot Instances**: Use for training with checkpointing (70-80% savings)
2. **Reserved Instances**: Commit for 1-3 years for steady workloads (40-60% savings)
3. **Right-sizing**: Match instance to workload (avoid over-provisioning)
4. **Regional Selection**: Choose regions with lower pricing
5. **Batch Processing**: Schedule training during low-demand periods
6. **Multi-cloud**: Compare across providers for best rates

### Contributing

To add a cloud instance:
1. Follow the schema exactly
2. Verify pricing from official calculators
3. Include all pricing models (on-demand, spot, reserved)
4. Cross-reference performance specs with GPU data
5. Validate with `python scripts/validate_data.py --dataset cloud`

### References

- AWS Pricing: https://aws.amazon.com/ec2/pricing/
- Azure Pricing: https://azure.microsoft.com/en-us/pricing/details/virtual-machines/
- GCP Pricing: https://cloud.google.com/compute/gpus-pricing
- AWS P5 Instances: https://aws.amazon.com/ec2/instance-types/p5/
- Azure ND-series: https://learn.microsoft.com/en-us/azure/virtual-machines/nd-series
- GCP A2/G2: https://cloud.google.com/compute/docs/gpus
