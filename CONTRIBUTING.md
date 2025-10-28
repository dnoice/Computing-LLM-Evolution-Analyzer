# Contributing to Computing & LLM Evolution Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/Computing-LLM-Evolution-Analyzer.git
   cd Computing-LLM-Evolution-Analyzer
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in Issues
- If not, create a new issue with:
  - Clear description of the bug
  - Steps to reproduce
  - Expected vs actual behavior
  - Your environment (Python version, OS, etc.)

### Suggesting Enhancements

- Open an issue describing the enhancement
- Explain why this enhancement would be useful
- Provide examples if possible

### Pull Requests

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes

4. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Adding Data

### Hardware Data

To add new hardware systems, edit `data/hardware/systems.json`:

```json
{
  "name": "System Name",
  "year": 2024,
  "manufacturer": "Manufacturer",
  "cpu_name": "CPU Name",
  "cpu_cores": 16,
  "cpu_transistors": 50000000000,
  ...
}
```

### LLM Data

To add new LLM models, edit `data/llm/models.json`:

```json
{
  "name": "Model Name",
  "year": 2024,
  "organization": "Organization",
  "parameters_billions": 100,
  "architecture_type": "Transformer",
  ...
}
```

## Testing

Before submitting a PR, ensure:
- Code runs without errors
- New features work as expected
- Existing functionality is not broken

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update examples if necessary

## Questions?

Feel free to open an issue for any questions or clarifications.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
