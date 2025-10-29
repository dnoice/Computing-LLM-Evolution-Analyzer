# Data Utility Scripts

This directory contains utility scripts for data validation, analysis, and quality assurance.

## Available Scripts

### 1. validate_data.py

Validates JSON data files against their schemas and performs quality checks.

**Usage:**
```bash
# Validate all datasets
python scripts/validate_data.py

# Validate specific dataset
python scripts/validate_data.py --dataset gpu
python scripts/validate_data.py --dataset hardware
python scripts/validate_data.py --dataset llm
python scripts/validate_data.py --dataset cloud

# Specify custom data directory
python scripts/validate_data.py --data-dir /path/to/data
```

**Features:**
- Schema validation using JSON Schema
- Duplicate detection
- Year ordering verification
- Missing field identification
- Comprehensive error and warning reporting
- Exit codes for CI/CD integration (0 = success, 1 = failure)

**Requirements:**
```bash
pip install jsonschema
```

**Example Output:**
```
============================================================
DATA VALIDATION REPORT
============================================================

============================================================
Validating GPU dataset
============================================================

✓ Schema validation: PASS
✓ Data records: 27

✓ All validation checks passed!

============================================================
VALIDATION SUMMARY
============================================================
GPU             ✓ PASS
HARDWARE        ✓ PASS
LLM             ✓ PASS
CLOUD           ✓ PASS

============================================================
✓ ALL DATASETS VALIDATED SUCCESSFULLY
============================================================
```

### 2. data_statistics.py

Generates comprehensive statistics and quality reports for all datasets.

**Usage:**
```bash
# Generate full statistics report
python scripts/data_statistics.py
```

**Features:**
- Dataset-specific statistics (GPU, Hardware, LLM, Cloud)
- Growth factor calculations
- Distribution analysis
- Pricing trends
- Capability score analytics
- Overall quality summary

**Output Includes:**
- Record counts and year ranges
- Manufacturer/provider distributions
- Performance and memory trends
- Growth factors and CAGR metrics
- Open source vs. closed source ratios
- Price ranges and spot savings
- Feature support statistics

**Example Output:**
```
======================================================================
DATA QUALITY AND STATISTICS REPORT
Generated: 2024-10-29 12:47:47
======================================================================

----------------------------------------------------------------------
GPU DATASET STATISTICS
----------------------------------------------------------------------
Total GPUs: 27
Year Range: 1999-2024
Manufacturers: NVIDIA(15), AMD(11), Intel(1)
Performance Range: 0.48 - 82.58 TFLOPS
...

======================================================================
OVERALL DATA QUALITY SUMMARY
======================================================================
Total Data Records: 89
Datasets: 4
Schemas: 4
Reference Files: 3
Documentation Files: 6

✓ Data infrastructure is comprehensive and production-ready
======================================================================
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Data Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install jsonschema

      - name: Validate data
        run: python scripts/validate_data.py

      - name: Generate statistics
        run: python scripts/data_statistics.py
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python scripts/validate_data.py
if [ $? -ne 0 ]; then
    echo "Data validation failed. Commit aborted."
    exit 1
fi
```

## Development Workflow

### Before Committing Data Changes

1. **Validate data:**
   ```bash
   python scripts/validate_data.py --dataset <dataset>
   ```

2. **Check statistics:**
   ```bash
   python scripts/data_statistics.py
   ```

3. **Review warnings** and fix any issues

4. **Ensure all checks pass** before committing

### Adding New Data

1. Follow the schema in `data/schemas/<dataset>_schema.json`
2. Add new entries maintaining year order
3. Validate: `python scripts/validate_data.py --dataset <dataset>`
4. Update `data/CHANGELOG.md` if adding new records
5. Commit changes

### Modifying Schemas

1. Update schema in `data/schemas/<dataset>_schema.json`
2. Ensure backward compatibility or update all data
3. Run validation on all datasets
4. Document breaking changes in `data/CHANGELOG.md`
5. Update schema version in dataset documentation

## Troubleshooting

### Schema Validation Errors

**Problem:** `Schema validation failed`

**Solution:**
- Check the error message for the specific field
- Review schema requirements in `data/schemas/`
- Ensure data types match (string, integer, number, boolean)
- Verify required fields are present

### Missing Dependencies

**Problem:** `jsonschema library not installed`

**Solution:**
```bash
pip install jsonschema
```

### Data Not Sorted by Year

**Warning:** `Data not sorted by year`

**Solution:**
- Sort your dataset by year field
- This is a warning, not an error, but maintaining order is best practice

### Duplicate Entries

**Warning:** `Duplicate GPU names found`

**Solution:**
- Check for accidentally duplicated entries
- Ensure each entry has a unique identifier
- Use different naming for variants (e.g., "RTX 4090" vs "RTX 4090 Ti")

## Best Practices

1. **Always validate before committing** - Run `validate_data.py` to catch issues early

2. **Keep data sorted** - Maintain chronological order by year for easier analysis

3. **Use consistent formats:**
   - Dates: `YYYY-MM`
   - Booleans: `true`/`false` (not `1`/`0` or `"yes"`/`"no"`)
   - Nulls: `null` (not `0` or empty string)
   - Field names: `snake_case`

4. **Document changes** - Update `data/CHANGELOG.md` for significant additions

5. **Verify sources** - Cross-check data with official sources listed in `data/SOURCES.md`

6. **Test locally** - Run both validation and statistics scripts before pushing

## Script Maintenance

### Adding New Quality Checks

To add custom validation logic to `validate_data.py`:

```python
def check_data_quality(self, data: List[Dict], dataset_name: str) -> None:
    """Perform quality checks on the data."""
    # ... existing checks ...

    # Add your custom check
    if dataset_name == 'gpu':
        for item in data:
            if item.get('tflops_fp32', 0) > 1000:
                self.warnings.append(
                    f"GPU {item['name']} has unusually high TFLOPS: {item['tflops_fp32']}"
                )
```

### Adding New Statistics

To add custom statistics to `data_statistics.py`:

```python
def analyze_gpu_data(self) -> Dict[str, Any]:
    """Analyze GPU dataset."""
    data = self.load_dataset('gpu', 'gpus.json')

    # Add your custom analysis
    efficiency = [
        item['tflops_fp32'] / item['tdp_watts']
        for item in data
        if item.get('tflops_fp32') and item.get('tdp_watts')
    ]

    return {
        # ... existing stats ...
        'efficiency': {
            'max_tflops_per_watt': max(efficiency) if efficiency else 0,
        }
    }
```

## Dependencies

- **Python 3.7+** - Required for type hints and modern syntax
- **jsonschema** - For JSON Schema validation

Install all dependencies:
```bash
pip install -r requirements.txt  # If requirements.txt exists
# Or individually:
pip install jsonschema
```

## Contributing

When contributing new scripts:

1. Follow Python best practices (PEP 8)
2. Add type hints
3. Include docstrings for functions and classes
4. Make scripts executable: `chmod +x script_name.py`
5. Add usage examples to this README
6. Test thoroughly before committing

## Support

For issues or questions:
- Check existing documentation in `data/README.md`
- Review `data/SOURCES.md` for data-related questions
- See `data/CHANGELOG.md` for version history
- Open an issue on GitHub

---

**Last Updated:** 2024-10-29
**Maintainer:** Computing-LLM-Evolution-Analyzer Project
