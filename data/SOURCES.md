# Data Sources

This document tracks the sources and methodologies used to compile the datasets in this project.

## Data Collection Principles

1. **Primary Sources**: Official manufacturer specifications and technical documentation
2. **Cross-Validation**: Multiple independent sources for critical metrics
3. **Transparency**: All sources documented and verifiable
4. **Accuracy**: Conservative estimates when exact data unavailable
5. **Attribution**: Proper credit to data providers

## GPU Data Sources

### Primary Sources
- **NVIDIA Official**: https://www.nvidia.com/en-us/geforce/graphics-cards/
  - GPU specifications, architecture details, official TFLOPS ratings
  - Used for: RTX series, GTX series specifications

- **AMD Official**: https://www.amd.com/en/graphics/
  - GPU specifications, RDNA/GCN architecture details
  - Used for: Radeon series specifications

- **Intel Arc**: https://www.intel.com/content/www/us/en/products/details/discrete-gpus/arc.html
  - Arc GPU specifications
  - Used for: Intel Arc A770 and related GPUs

### Secondary Sources
- **TechPowerUp GPU Database**: https://www.techpowerup.com/gpu-specs/
  - Comprehensive historical GPU database
  - Cross-validation of specifications
  - Used for: Historical GPU data, die sizes, process nodes

- **AnandTech**: https://www.anandtech.com/
  - In-depth technical reviews and analysis
  - Used for: Performance validation, architectural details

- **Tom's Hardware**: https://www.tomshardware.com/
  - GPU reviews and specifications
  - Used for: Real-world performance data, pricing history

## Hardware Systems Data Sources

### Primary Sources
- **Computer History Museum**: https://computerhistory.org/
  - Historical system specifications
  - Used for: Pre-1990 systems, mainframe data

- **Intel Museum**: https://www.intel.com/content/www/us/en/history/museum-story-of-intel-4004.html
  - Intel processor history and specifications
  - Used for: Intel CPU historical data

- **AMD Corporate**: https://www.amd.com/en/corporate/history
  - AMD processor history
  - Used for: AMD Ryzen and historical CPU data

- **Apple Press Releases**: https://www.apple.com/newsroom/
  - Apple Silicon specifications and announcements
  - Used for: M1, M2 series specifications

### Secondary Sources
- **CPU World**: http://www.cpu-world.com/
  - Comprehensive CPU database
  - Used for: CPU specifications, cross-validation

- **Wikipedia**: Various CPU and computer system articles
  - Used for: Historical context, release dates
  - Note: Always cross-referenced with primary sources

## LLM Data Sources

### Primary Sources
- **OpenAI**: https://openai.com/research
  - GPT-3, GPT-4, o1 model papers and specifications
  - Used for: GPT series architecture, training details

- **Anthropic**: https://www.anthropic.com/research
  - Claude model papers and technical reports
  - Used for: Claude series specifications, capability benchmarks

- **Google DeepMind**: https://deepmind.google/research/
  - Gemini technical reports
  - Used for: Gemini specifications and capabilities

- **Meta AI**: https://ai.meta.com/llama/
  - LLaMA model cards and research papers
  - Used for: LLaMA series specifications

- **Mistral AI**: https://mistral.ai/
  - Mistral model specifications
  - Used for: Mistral 7B specifications

### Benchmark Sources
- **Papers with Code**: https://paperswithcode.com/
  - Standardized benchmark results
  - Used for: MMLU, HumanEval, GSM8K scores

- **Hugging Face**: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
  - Open LLM Leaderboard
  - Used for: Cross-validation of capability scores

- **Original Papers**: arXiv and conference proceedings
  - Model-specific technical papers
  - Used for: Training details, architecture specifications

### Pricing Sources
- **OpenAI Pricing**: https://openai.com/pricing
- **Anthropic Pricing**: https://www.anthropic.com/pricing
- **Google Cloud AI**: https://cloud.google.com/vertex-ai/pricing
- Updated: Quarterly or when major changes occur

## Cloud Instance Data Sources

### Primary Sources
- **AWS EC2 Pricing**: https://aws.amazon.com/ec2/pricing/
  - P3, P4, P5, G5, Inf2 instance specifications and pricing
  - Used for: AWS instance data

- **Azure Pricing**: https://azure.microsoft.com/en-us/pricing/details/virtual-machines/
  - NC, ND series specifications and pricing
  - Used for: Azure instance data

- **Google Cloud Pricing**: https://cloud.google.com/compute/all-pricing
  - A2, N1, G2 instance specifications and pricing
  - Used for: GCP instance data

### Documentation Sources
- **AWS P5 Documentation**: https://aws.amazon.com/ec2/instance-types/p5/
- **Azure ND-series**: https://learn.microsoft.com/en-us/azure/virtual-machines/nd-series
- **GCP GPU Documentation**: https://cloud.google.com/compute/docs/gpus

### Validation
- **Cloud Pricing Calculators**: Used for cross-validation
  - AWS Pricing Calculator
  - Azure Pricing Calculator
  - Google Cloud Pricing Calculator

## Benchmark and Reference Data Sources

### LLM Benchmarks
- **MMLU Paper**: "Measuring Massive Multitask Language Understanding" (Hendrycks et al., 2021)
- **HumanEval**: "Evaluating Large Language Models Trained on Code" (Chen et al., 2021)
- **GSM8K**: "Training Verifiers to Solve Math Word Problems" (Cobbe et al., 2021)

### GPU Benchmarks
- **MLPerf**: https://mlcommons.org/benchmarks/
  - Training and inference benchmarks
  - Industry standard for ML performance

- **3DMark**: https://www.3dmark.com/
  - Graphics and compute benchmarks

### Scaling Laws
- **Chinchilla Paper**: "Training Compute-Optimal Large Language Models" (Hoffmann et al., 2022)
  - Source for optimal training token calculations

- **Kaplan et al.**: "Scaling Laws for Neural Language Models" (2020)
  - Original GPT-3 scaling law formulations

## Theoretical Limits Sources

### Physics and Engineering
- **International Technology Roadmap for Semiconductors (ITRS)**: Industry consensus on semiconductor scaling
- **Landauer's Principle**: "Irreversibility and Heat Generation in the Computing Process" (Landauer, 1961)
- **Moore's Law**: Original and updated formulations from Intel publications

### Process Technology
- **TSMC Technology Symposium**: Annual updates on process node capabilities
- **IEEE International Electron Devices Meeting (IEDM)**: Latest research on transistor technology
- **Semiconductor Industry Association**: Industry reports and projections

## Data Update Schedule

| Dataset | Update Frequency | Last Updated | Next Update |
|---------|-----------------|--------------|-------------|
| GPU Data | Quarterly | 2024-10-29 | 2025-01-31 |
| Hardware Systems | Annually | 2024-10-29 | 2025-10-31 |
| LLM Models | Monthly | 2024-10-29 | 2024-11-30 |
| Cloud Instances | Quarterly | 2024-10-29 | 2025-01-31 |
| Benchmarks | Semi-Annually | 2024-10-29 | 2025-04-30 |
| Theoretical Limits | Annually | 2024-10-29 | 2025-10-31 |

## Data Quality Assurance

### Validation Process
1. **Primary Source Check**: Verify against official manufacturer data
2. **Cross-Reference**: Compare with at least 2 independent sources
3. **Reasonableness Check**: Verify metrics are within expected ranges
4. **Schema Validation**: Ensure data conforms to JSON schemas
5. **Trend Analysis**: Check for anomalies in year-over-year trends

### Known Data Quality Issues
- **Early GPU Data (1999-2004)**: Limited availability of detailed specifications
- **LLM Training Costs**: Many proprietary models don't disclose actual costs
- **Cloud Spot Pricing**: Highly variable; we use historical averages
- **Capability Scores**: Normalized across different benchmark methodologies

## Contributing Sources

If you have authoritative sources for missing or updated data:

1. Verify the source is official or widely recognized
2. Include publication date and retrieval date
3. Document methodology if data required calculation/estimation
4. Submit with references in SOURCES.md format

## Disclaimer

While we strive for accuracy, specifications may vary by:
- Manufacturing batch/revision
- Region and availability
- Configuration options
- Time of measurement

Always consult official sources for critical applications.

## Contact

For data source questions or corrections:
- GitHub Issues: https://github.com/anthropics/claude-code/issues
- Include: Dataset name, specific entry, proposed correction, and source

## License and Attribution

Data compiled from public sources. See individual source links for their respective licenses and terms of use. This compilation is provided for research and educational purposes.

**Last Updated**: 2024-10-29
**Version**: 2.1.0
