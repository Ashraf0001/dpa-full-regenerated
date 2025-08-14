# Data Processing Accelerator (DPA)

A high-performance data processing tool built with Rust and Polars, featuring both CLI and Python API interfaces.

## Features

- **Fast Data Processing**: Built on Rust and Polars for optimal performance
- **Multiple Formats**: Support for CSV, Parquet, and JSON files
- **SQL-like Filtering**: Use SQL expressions for data filtering
- **Column Selection**: Select specific columns from datasets
- **Format Conversion**: Convert between different file formats
- **Data Profiling**: Get quick insights into your data
- **Dual Interface**: Both command-line and Python API available

## Installation

### Prerequisites

- Rust (1.70 or later)
- Python 3.8 or later
- pip

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
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

## Usage

### Command Line Interface

#### Basic Commands

```bash
# View schema of a file
./target/release/dpa schema data/transactions_small.csv

# Preview first 10 rows
./target/release/dpa head data/transactions_small.csv -n 10

# Profile data (sample and show statistics)
./target/release/dpa profile data/transactions_small.csv

# Convert CSV to Parquet
./target/release/dpa convert data/transactions_small.csv output.parquet

# Select specific columns
./target/release/dpa select data/transactions_small.csv -c "user_id,amount" -o selected.parquet

# Filter data with SQL expression
./target/release/dpa filter data/transactions_small.csv -w "amount > 100" -o filtered.parquet

# Filter and select columns
./target/release/dpa filter data/transactions_small.csv -w "amount > 100" -s "user_id,amount" -o result.parquet
```

#### Python CLI

```bash
# Same commands with Python interface
python3 -m dpa schema data/transactions_small.csv
python3 -m dpa profile data/transactions_small.csv
python3 -m dpa convert data/transactions_small.csv output.parquet
python3 -m dpa select data/transactions_small.csv -c "user_id,amount" -o selected.parquet
python3 -m dpa filter data/transactions_small.csv -w "amount > 100" -o filtered.parquet
```

### Python API

```python
import dpa_core

# Profile data
profile = dpa_core.profile_py("data/transactions_small.csv")
print(f"Rows: {profile['rows']}")
print(f"Columns: {[k for k in profile.keys() if k.startswith('dtype:')]}")

# Convert file format
dpa_core.convert_py("data/transactions_small.csv", "output.parquet")

# Select columns
dpa_core.select_py("data/transactions_small.csv", ["user_id", "amount"], "selected.parquet")

# Filter data
dpa_core.filter_py("data/transactions_small.csv", "amount > 100", None, "filtered.parquet")

# Filter with column selection
dpa_core.filter_py("data/transactions_small.csv", "amount > 100", ["user_id", "amount"], "result.parquet")
```

## Testing

### Run Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
python3 -m pytest tests/ -v

# Run specific test categories
python3 -m pytest tests/test_dpa_core.py -v  # Python API tests
python3 -m pytest tests/test_cli.py -v       # CLI tests

# Run with coverage
python3 -m pytest tests/ --cov=dpa_core --cov-report=html
```

### Test Coverage

The test suite includes:

- **Unit Tests**: Individual function testing
- **Integration Tests**: End-to-end workflow testing
- **Error Handling**: Invalid inputs and edge cases
- **CLI Tests**: Command-line interface validation
- **Python API Tests**: Direct function calls

## Development

### Project Structure

```
dpa-full-regenerated/
├── src/                    # Rust source code
│   ├── main.rs            # CLI entry point
│   ├── lib.rs             # Python bindings
│   ├── cli.rs             # CLI argument parsing
│   ├── engine/            # Core data processing logic
│   └── io/                # File I/O operations
├── python/                # Python package
│   ├── dpa/               # Python CLI implementation
│   └── pyproject.toml     # Python package configuration
├── tests/                 # Test suite
├── data/                  # Sample data files
└── Cargo.toml            # Rust project configuration
```

### Building

```bash
# Build Rust binary
cargo build --release

# Build Python bindings
maturin build --release

# Install in development mode
maturin develop
```

### Code Quality

```bash
# Rust formatting and linting
cargo fmt
cargo clippy

# Python formatting and linting
black python/ tests/
flake8 python/ tests/
mypy python/ tests/
```

## Performance

DPA is designed for high-performance data processing:

- **Rust Backend**: Compiled to native code for maximum speed
- **Polars Integration**: Leverages Polars' optimized data processing
- **Lazy Evaluation**: Efficient memory usage with lazy computation
- **Parallel Processing**: Automatic parallelization where possible

## Supported Formats

- **Input**: CSV, Parquet, JSON, JSONL
- **Output**: CSV, Parquet

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Roadmap

- [ ] Support for more file formats (Excel, Avro)
- [ ] Additional aggregation functions
- [ ] Data validation features
- [ ] Performance benchmarking tools
- [ ] Web interface
- [ ] Distributed processing support
