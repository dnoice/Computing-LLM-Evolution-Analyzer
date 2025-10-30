"""Setup configuration for Computing & LLM Evolution Analyzer."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = []

setup(
    name="llm-evolution-analyzer",
    version="2.1.0",
    author="Computing Evolution Team",
    author_email="contact@example.com",
    description="Comprehensive analysis tool for computing hardware and LLM evolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Computing-LLM-Evolution-Analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "llm-evolution-analyzer=llm_evolution.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/**/*.json"],
    },
    keywords="llm hardware evolution analysis moore's-law cagr computing",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/Computing-LLM-Evolution-Analyzer/issues",
        "Source": "https://github.com/yourusername/Computing-LLM-Evolution-Analyzer",
        "Documentation": "https://github.com/yourusername/Computing-LLM-Evolution-Analyzer/blob/main/README.md",
    },
)
