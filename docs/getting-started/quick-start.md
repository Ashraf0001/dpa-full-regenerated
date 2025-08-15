# Quick Start Guide

Welcome to Data Processing Accelerator (DPA)! This guide will get you up and running in minutes.

## What is DPA?

DPA is a high-performance data processing tool built with Rust and Polars, featuring:

- **Lightning-fast performance** with Rust and Polars
- **Python API** for seamless integration
- **Command-line interface** for quick operations
- **Advanced data profiling** and validation
- **Multiple file formats** (CSV, Parquet, JSON)
- **Smart sampling** and data splitting

## Installation

### Prerequisites

- **Rust** (1.70 or later)
- **Python** (3.8 or later)
- **pip** for Python package management

### Quick Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/dpa-full-regenerated
   cd dpa-full-regenerated
   ```

2. **Build the Rust binary**:
   ```bash
   cargo build --release
   ```

3. **Install Python bindings**:
   ```bash
   pip install maturin
   maturin develop
   ```

4. **Install Python CLI**:
   ```bash
   cd python
   pip install .
   ```

## Your First DPA Operations

### 1. Data Profiling

Profile your data to understand its structure and quality:

```bash
# Basic profiling
./target/release/dpa profile data/transactions_small.csv

# Detailed profiling with statistics
./target/release/dpa profile data/transactions_small.csv --detailed
```

### 2. Data Validation

Validate your data against schemas and rules:

```bash
# Basic validation
./target/release/dpa validate data/transactions_small.csv

# Schema validation
./target/release/dpa validate data/transactions_small.csv --schema examples/schema.json
```

### 3. Data Sampling

Sample your data for analysis or testing:

```bash
# Random sampling
./target/release/dpa sample data/transactions_small.csv output.csv --method random --size 1000

# Stratified sampling
./target/release/dpa sample data/transactions_small.csv output.csv --method stratified --stratify category
```

### 4. Using Python API

```python
import dpa_core

# Profile data
stats = dpa_core.profile_py("data/transactions_small.csv")
print(stats)

# Sample data
dpa_core.sample_py("data/transactions_small.csv", "sample.csv", size=1000, method="random")

# Validate data
dpa_core.validate_py("data/transactions_small.csv")
```

## Next Steps

- Read the [Installation Guide](installation.md) for detailed setup instructions
- Explore [Features](../features/) to learn about all capabilities
- Check out [Examples](../examples/) for practical use cases
- See [Configuration](configuration.md) for advanced setup

## Getting Help

- **Documentation**: Browse the full documentation
- **Issues**: Report bugs on GitHub
- **Discussions**: Join community discussions
- **Support**: Contact the development team

---

**Ready to accelerate your data processing?**
