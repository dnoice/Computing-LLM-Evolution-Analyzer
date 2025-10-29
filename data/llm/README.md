# LLM Evolution Data

This directory contains comprehensive data on Large Language Model evolution from 2018 to 2024.

## Dataset: models.json

### Overview

Tracks the rapid evolution of Large Language Models over 6 years, documenting the explosive growth in model scale, capabilities, and adoption during the generative AI revolution.

### Key Milestones Covered

- **2018**: BERT introduces bidirectional transformers
- **2019**: GPT-2 demonstrates zero-shot capabilities
- **2020**: GPT-3 achieves few-shot learning at scale
- **2023**: GPT-4 reaches multimodal capabilities; Claude 2 achieves 100K context
- **2024**: Multiple frontier models; o1 brings extended reasoning; Gemini reaches 2M context

### Data Schema

Each LLM record contains:

```json
{
  "name": "string",                           // Model name
  "year": integer,                            // Release year
  "organization": "string",                   // OpenAI | Anthropic | Google | Meta | Mistral AI

  // Model architecture
  "parameters_billions": number,              // Parameters in billions
  "architecture_type": "string",              // Transformer variant
  "num_layers": integer,                      // Number of layers
  "hidden_size": integer,                     // Hidden dimension size
  "attention_heads": integer,                 // Number of attention heads

  // Training specifications
  "training_tokens_billions": number,         // Training tokens in billions
  "training_compute_flops": number,          // Total compute in FLOPS
  "training_days": integer,                   // Training duration

  // Context and output
  "context_window": integer,                  // Maximum context length
  "max_output_tokens": integer,              // Maximum output length

  // Capability scores (0-100)
  "capability_score_reasoning": integer,      // Reasoning ability
  "capability_score_coding": integer,         // Coding ability
  "capability_score_math": integer,           // Mathematical reasoning
  "capability_score_knowledge": integer,      // Knowledge breadth
  "capability_score_multilingual": integer,   // Multilingual capability

  // Economics
  "cost_per_1m_input_tokens": number,        // API cost per 1M input tokens
  "cost_per_1m_output_tokens": number,       // API cost per 1M output tokens

  // Metadata
  "release_date": "YYYY-MM",                 // Release date
  "model_type": "string",                    // text | multimodal
  "open_source": boolean,                    // Open source availability
  "notes": "string"                          // Key features/innovations
}
```

### Data Collection Methodology

Data sourced from:
1. Official model cards and papers
2. OpenAI, Anthropic, Google, Meta technical reports
3. Academic benchmarks (MMLU, HumanEval, GSM8K, etc.)
4. API documentation and pricing pages
5. Third-party evaluations and leaderboards

### Coverage Statistics

- **Total Models**: 22
- **Organizations**: OpenAI (5), Anthropic (4), Google (3), Meta (4), Mistral AI (1), Intel (1)
- **Time Span**: 2018-2024 (6 years)
- **Open Source**: 9 models (41%)
- **Multimodal**: 8 models (36%)

### Scaling Trends

| Metric | 2018 (BERT) | 2024 (GPT-4o) | Growth Factor | CAGR |
|--------|------------|---------------|---------------|------|
| Parameters | 0.11B | 1,760B | 16,000x | 330% |
| Training Tokens | 3.3B | 20T | 6,061x | 282% |
| Training Compute | 9.2e18 | 3.2e25 | 3.5M x | 458% |
| Context Window | 512 | 128,000 | 250x | 138% |
| Avg Capability | 36 | 92 | 2.6x | 17.6% |

**⚠️ Reality Check**: These growth rates represent a temporary scaling phase and are NOT sustainable long-term. Expected future: 20-50% CAGR as the field matures.

### Chinchilla Optimal Analysis

The Chinchilla paper (2022) established optimal training token-to-parameter ratios:
- **Optimal**: ~20 tokens per parameter
- **Undertrained**: < 10 tokens per parameter
- **Overtrained**: > 40 tokens per parameter

Our dataset includes analysis of which models follow Chinchilla-optimal training.

### Usage Examples

#### Load and analyze LLM data

```python
from llm_evolution.llm_analyzer import LLMAnalyzer

analyzer = LLMAnalyzer()

# Get all models
models = analyzer.models

# Calculate CAGR for all metrics
cagr_results = analyzer.calculate_all_cagrs()
for metric, result in cagr_results.items():
    print(f"{metric}: {result.cagr_percent:.2f}% CAGR")

# Chinchilla optimal analysis
chinchilla_analysis = analyzer.analyze_chinchilla_optimal()

# Cost efficiency ranking
cost_efficiency = analyzer.analyze_cost_efficiency()
```

#### Compare capabilities

```python
# Get latest models
latest_models = sorted(models, key=lambda m: m.year, reverse=True)[:5]

# Compare capability scores
for model in latest_models:
    avg_score = (
        model.capability_score_reasoning +
        model.capability_score_coding +
        model.capability_score_math +
        model.capability_score_knowledge +
        model.capability_score_multilingual
    ) / 5
    print(f"{model.name}: {avg_score:.1f} avg capability")

# Find best coding model
best_coder = max(models, key=lambda m: m.capability_score_coding)
print(f"Best coding: {best_coder.name} ({best_coder.capability_score_coding}/100)")
```

#### Analyze training efficiency

```python
# Calculate FLOPS per parameter
for model in models[-10:]:  # Last 10 models
    flops_per_param = model.training_compute_flops / (model.parameters_billions * 1e9)
    tokens_per_param = model.training_tokens_billions / model.parameters_billions
    print(f"{model.name}:")
    print(f"  FLOPS/param: {flops_per_param:.0f}")
    print(f"  Tokens/param: {tokens_per_param:.0f}")
```

### Data Quality Notes

- **Capability Scores**: Based on public benchmarks; normalized to 0-100 scale
- **Training Metrics**: Some values estimated from public information
- **Pricing**: Current as of last update; subject to change
- **Architecture Details**: Simplified for comparability; see papers for full details
- **Completeness**: Some proprietary details unavailable for closed models

### Context Window Evolution

| Year | Max Context | Model | Notes |
|------|------------|-------|-------|
| 2018 | 512 | BERT | Standard transformer |
| 2020 | 2,048 | GPT-3 | Dense attention |
| 2023 | 100,000 | Claude 2 | Breakthrough in long context |
| 2024 | 2,000,000 | Gemini 1.5 Pro | Current record |

### Open Source vs Closed

| Category | Count | Avg Parameters | Avg Context |
|----------|-------|----------------|-------------|
| Open Source | 9 | 65B | 6,827 tokens |
| Closed Source | 13 | 465B | 86,646 tokens |

### Scaling Laws and Limits

The dataset reveals important trends:

1. **Parameter Scaling**: Growing ~10x every 2 years (2018-2023)
2. **Compute Scaling**: Growing ~100x every 2 years (unsustainable)
3. **Context Scaling**: 100x growth in 2023-2024 (architectural innovation)
4. **Capability Gains**: Slowing returns per parameter increase
5. **Cost**: Declining per token as competition increases

### Update History

- **v2.1.0 (2024-10-29)**: Added o1-preview, Claude 3.5 Sonnet v2, updated Gemini 1.5
- **v2.0.0 (2024-06)**: Restructured capability scoring system
- **v1.5.0 (2024-03)**: Added Claude 3 family, Gemini Pro
- **v1.0.0 (2023-09)**: Initial dataset with 15 models

### Related Data

- See `../cloud/instances.json` for training cost estimation
- See `../gpu/gpus.json` for hardware requirements
- See `../reference/benchmarks.json` for standardized evaluations

### Known Limitations

1. **Capability Scores**: Subjective normalization across different benchmarks
2. **Training Details**: Many proprietary models don't disclose full training details
3. **Architecture**: Simplified representations of complex architectures
4. **Multimodal**: Vision capabilities not fully captured in scores
5. **Temporal**: Scores represent capability at release, not current fine-tuned versions

### Important Notes on Growth Rates

**The extreme CAGR values in LLM metrics (200-400%+) are NOT comparable to hardware trends because:**

1. **Time Period**: 6 years vs 25-59 years for hardware
2. **Temporary Phase**: Initial research phase, not steady-state
3. **Different Constraints**: Data/economic limits vs physical limits
4. **Expected Slowdown**: Predicted to normalize to 20-50% CAGR

### Contributing

To add an LLM:
1. Follow the schema exactly
2. Use official technical reports for specs
3. Normalize capability scores against public benchmarks
4. Include model card link in notes
5. Validate with `python scripts/validate_data.py --dataset llm`

### References

- Model Papers: arXiv links in notes field
- OpenAI Models: https://platform.openai.com/docs/models
- Anthropic Claude: https://www.anthropic.com/claude
- Google Gemini: https://deepmind.google/technologies/gemini/
- Meta Llama: https://llama.meta.com/
- Hugging Face Leaderboard: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
