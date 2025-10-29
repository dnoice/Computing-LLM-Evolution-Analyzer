#!/usr/bin/env python3
"""
Data Validation Script

Validates JSON data files against their schemas and performs quality checks.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("Error: jsonschema library not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)


class DataValidator:
    """Validates data files against schemas and performs quality checks."""

    def __init__(self, data_dir: Path):
        """Initialize validator with data directory path."""
        self.data_dir = data_dir
        self.schemas_dir = data_dir / "schemas"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_schema(self, schema_name: str) -> Optional[Dict]:
        """Load a JSON schema file."""
        schema_path = self.schemas_dir / f"{schema_name}_schema.json"

        if not schema_path.exists():
            self.errors.append(f"Schema not found: {schema_path}")
            return None

        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.errors.append(f"Error loading schema {schema_name}: {e}")
            return None

    def load_data(self, dataset_name: str) -> Optional[Any]:
        """Load a JSON data file."""
        # Map dataset names to their file paths
        dataset_paths = {
            'gpu': self.data_dir / 'gpu' / 'gpus.json',
            'hardware': self.data_dir / 'hardware' / 'systems.json',
            'llm': self.data_dir / 'llm' / 'models.json',
            'cloud': self.data_dir / 'cloud' / 'instances.json'
        }

        data_path = dataset_paths.get(dataset_name)
        if not data_path:
            self.errors.append(f"Unknown dataset: {dataset_name}")
            return None

        if not data_path.exists():
            self.errors.append(f"Data file not found: {data_path}")
            return None

        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.errors.append(f"Error loading data {dataset_name}: {e}")
            return None

    def validate_against_schema(self, data: Any, schema: Dict, dataset_name: str) -> bool:
        """Validate data against its schema."""
        try:
            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            self.errors.append(f"Schema validation failed for {dataset_name}: {e.message}")
            if e.path:
                self.errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")
            return False

    def check_data_quality(self, data: List[Dict], dataset_name: str) -> None:
        """Perform quality checks on the data."""
        if not isinstance(data, list):
            self.errors.append(f"{dataset_name}: Data should be a list")
            return

        if len(data) == 0:
            self.warnings.append(f"{dataset_name}: Dataset is empty")
            return

        # Check for duplicate entries
        if dataset_name == 'gpu':
            names = [item.get('name') for item in data]
            duplicates = [name for name in names if names.count(name) > 1]
            if duplicates:
                self.warnings.append(f"{dataset_name}: Duplicate GPU names found: {set(duplicates)}")

        # Check year ordering
        years = [item.get('year') for item in data if item.get('year')]
        if years and years != sorted(years):
            self.warnings.append(f"{dataset_name}: Data not sorted by year")

        # Check for missing required fields
        first_item = data[0]
        required_fields = list(first_item.keys())

        for i, item in enumerate(data):
            item_fields = set(item.keys())
            missing = set(required_fields) - item_fields
            if missing:
                self.warnings.append(
                    f"{dataset_name}: Entry {i} missing fields: {missing}"
                )

    def validate_dataset(self, dataset_name: str) -> bool:
        """Validate a specific dataset."""
        print(f"\n{'=' * 60}")
        print(f"Validating {dataset_name.upper()} dataset")
        print(f"{'=' * 60}")

        # Load schema
        schema = self.load_schema(dataset_name)
        if not schema:
            return False

        # Load data
        data = self.load_data(dataset_name)
        if data is None:
            return False

        # Validate against schema
        schema_valid = self.validate_against_schema(data, schema, dataset_name)

        # Perform quality checks
        self.check_data_quality(data, dataset_name)

        # Print results
        print(f"\n✓ Schema validation: {'PASS' if schema_valid else 'FAIL'}")
        print(f"✓ Data records: {len(data)}")

        if self.warnings:
            print(f"\n⚠ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
            self.warnings.clear()

        if self.errors:
            print(f"\n✗ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
            errors_found = len(self.errors)
            self.errors.clear()
            return errors_found == 0

        print("\n✓ All validation checks passed!")
        return True

    def validate_all(self) -> bool:
        """Validate all datasets."""
        datasets = ['gpu', 'hardware', 'llm', 'cloud']
        results = {}

        print("\n" + "=" * 60)
        print("DATA VALIDATION REPORT")
        print("=" * 60)

        for dataset in datasets:
            results[dataset] = self.validate_dataset(dataset)

        # Print summary
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        for dataset, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{dataset.upper():15} {status}")

        all_passed = all(results.values())

        print("\n" + "=" * 60)
        if all_passed:
            print("✓ ALL DATASETS VALIDATED SUCCESSFULLY")
        else:
            print("✗ SOME DATASETS FAILED VALIDATION")
        print("=" * 60 + "\n")

        return all_passed


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate data files against their JSON schemas"
    )
    parser.add_argument(
        '--dataset',
        choices=['gpu', 'hardware', 'llm', 'cloud', 'all'],
        default='all',
        help='Dataset to validate (default: all)'
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'data',
        help='Path to data directory (default: ../data)'
    )

    args = parser.parse_args()

    # Initialize validator
    validator = DataValidator(args.data_dir)

    # Validate
    if args.dataset == 'all':
        success = validator.validate_all()
    else:
        success = validator.validate_dataset(args.dataset)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
