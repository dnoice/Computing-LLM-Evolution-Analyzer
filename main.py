#!/usr/bin/env python3
"""Main entry point for Computing & LLM Evolution Analyzer."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from llm_evolution.cli import main

if __name__ == "__main__":
    main()
