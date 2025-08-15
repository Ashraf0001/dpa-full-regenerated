# Basic Usage Examples

Learn how to use DPA for common data processing tasks with practical examples.

## Overview

This guide provides step-by-step examples for the most common DPA operations. Each example includes both CLI and Python API approaches.

## Prerequisites

Before running these examples, ensure you have:

- ✅ DPA installed (see [Installation Guide](../getting-started/installation.md))
- ✅ Sample data files (or create your own)
- ✅ Basic familiarity with command line or Python

## Example 1: Data Profiling

### Understanding Your Data

**Scenario**: You have a CSV file and want to understand its structure and quality.

#### CLI Approach

```bash
# Basic profiling
./target/release/dpa profile data/transactions.csv

# Detailed profiling with statistics
./target/release/dpa profile data/transactions.csv --detailed

# Save profile report to file
./target/release/dpa profile data/transactions.csv --output profile_report.json --format json
```

#### Python API Approach

```python
import dpa_core
import json

# Basic profiling
stats = dpa_core.profile_py("data/transactions.csv")
print(f"Total rows: {stats['total_rows']}")
print(f"Total columns: {stats['total_columns']}")
print(f"Memory usage: {stats['memory_usage']}")

# Access column-specific statistics
for col_name, col_stats in stats['columns'].items():
    print(f"\n{col_name}:")
    print(f"  Type: {col_stats['type']}")
    print(f"  Null percentage: {col_stats['null_percentage']}%")
    print(f"  Unique values: {col_stats['unique_count']}")

# Save detailed report
with open('profile_report.json', 'w') as f:
    json.dump(stats, f, indent=2)
```

**Expected Output:**
```
📊 Data Profile Report
=====================

📁 File: data/transactions.csv
📏 Shape: 10,000 rows × 5 columns
💾 Size: 2.3 MB
⏱️  Processing time: 0.8s

📈 Column Statistics:
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Column  │ Type    │ Null %  │ Unique  │ Min     │ Max     │
├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ id      │ Int64   │ 0.0%    │ 10,000  │ 1       │ 10,000  │
│ amount  │ Float64 │ 2.0%    │ 8,950   │ 10.50   │ 9999.99 │
│ date    │ String  │ 0.0%    │ 365     │ -       │ -       │
│ category│ String  │ 1.0%    │ 15      │ -       │ -       │
│ country │ String  │ 0.0%    │ 45      │ -       │ -       │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
```

## Example 2: Data Validation

### Ensuring Data Quality

**Scenario**: You want to validate your data against a schema and custom business rules.

#### Create Schema File

```json
{
  "columns": {
    "id": {
      "type": "integer",
      "nullable": false,
      "unique": true
    },
    "amount": {
      "type": "float",
      "nullable": true,
      "min": 0.0,
      "max": 10000.0
    },
    "date": {
      "type": "string",
      "nullable": false,
      "pattern": "\\d{4}-\\d{2}-\\d{2}"
    },
    "category": {
      "type": "string",
      "nullable": true,
      "allowed_values": ["electronics", "clothing", "books", "food"]
    },
    "country": {
      "type": "string",
      "nullable": false,
      "min_length": 2,
      "max_length": 3
    }
  }
}
```

#### Create Validation Rules

```json
[
  {
    "name": "high_value_transactions",
    "column": "amount",
    "rule_type": "sql",
    "expression": "amount > 5000",
    "message": "High value transactions detected",
    "severity": "warning"
  },
  {
    "name": "future_dates",
    "column": "date",
    "rule_type": "sql",
    "expression": "date > '2024-12-31'",
    "message": "Future dates detected",
    "severity": "error"
  }
]
```

#### CLI Approach

```bash
# Basic validation
./target/release/dpa validate data/transactions.csv

# Schema validation
./target/release/dpa validate data/transactions.csv --schema schema.json

# Custom rules validation
./target/release/dpa validate data/transactions.csv --rules validation_rules.json

# Combined validation
./target/release/dpa validate data/transactions.csv --schema schema.json --rules validation_rules.json

# Strict validation (fail on first error)
./target/release/dpa validate data/transactions.csv --schema schema.json --strict
```

#### Python API Approach

```python
import dpa_core

# Basic validation
try:
    dpa_core.validate_py("data/transactions.csv")
    print("✅ Basic validation passed!")
except RuntimeError as e:
    print(f"❌ Validation failed: {e}")

# Schema validation
try:
    dpa_core.validate_py("data/transactions.csv", schema="schema.json")
    print("✅ Schema validation passed!")
except RuntimeError as e:
    print(f"❌ Schema validation failed: {e}")

# Custom rules validation
try:
    dpa_core.validate_py("data/transactions.csv", rules="validation_rules.json")
    print("✅ Rules validation passed!")
except RuntimeError as e:
    print(f"❌ Rules validation failed: {e}")

# Combined validation
try:
    dpa_core.validate_py("data/transactions.csv", schema="schema.json", rules="validation_rules.json")
    print("✅ All validations passed!")
except RuntimeError as e:
    print(f"❌ Validation failed: {e}")
```

## Example 3: Data Sampling

### Creating Representative Samples

**Scenario**: You have a large dataset and want to create smaller samples for analysis or testing.

#### CLI Approach

```bash
# Random sampling
./target/release/dpa sample data/transactions.csv sample_random.csv --method random --size 1000

# Stratified sampling by category
./target/release/dpa sample data/transactions.csv sample_stratified.csv --method stratified --stratify category --size 500

# Head sampling (first N rows)
./target/release/dpa sample data/transactions.csv sample_head.csv --method head --size 100

# Tail sampling (last N rows)
./target/release/dpa sample data/transactions.csv sample_tail.csv --method tail --size 100

# Reproducible sampling with seed
./target/release/dpa sample data/transactions.csv sample_seeded.csv --method random --size 1000 --seed 42
```

#### Python API Approach

```python
import dpa_core

# Random sampling
dpa_core.sample_py("data/transactions.csv", "sample_random.csv", size=1000, method="random")

# Stratified sampling
dpa_core.sample_py("data/transactions.csv", "sample_stratified.csv", size=500, method="stratified", stratify="category")

# Head sampling
dpa_core.sample_py("data/transactions.csv", "sample_head.csv", size=100, method="head")

# Tail sampling
dpa_core.sample_py("data/transactions.csv", "sample_tail.csv", size=100, method="tail")

# Reproducible sampling
dpa_core.sample_py("data/transactions.csv", "sample_seeded.csv", size=1000, method="random", seed=42)

# Verify sample sizes
import pandas as pd
original = pd.read_csv("data/transactions.csv")
sample = pd.read_csv("sample_random.csv")
print(f"Original: {len(original)} rows")
print(f"Sample: {len(sample)} rows")
```

## Example 4: Train/Test Split

### Preparing Data for Machine Learning

**Scenario**: You want to split your data into training and test sets for machine learning.

#### CLI Approach

```bash
# Basic split (80% train, 20% test)
./target/release/dpa split data/transactions.csv train.csv test.csv

# Custom split ratio (70% train, 30% test)
./target/release/dpa split data/transactions.csv train.csv test.csv --test-size 0.3

# Stratified split by category
./target/release/dpa split data/transactions.csv train.csv test.csv --stratify category

# Reproducible split with seed
./target/release/dpa split data/transactions.csv train.csv test.csv --seed 42

# Combined options
./target/release/dpa split data/transactions.csv train.csv test.csv --test-size 0.25 --stratify category --seed 42
```

#### Python API Approach

```python
import dpa_core
import pandas as pd

# Basic split
dpa_core.split_py("data/transactions.csv", "train.csv", "test.csv")

# Custom test size
dpa_core.split_py("data/transactions.csv", "train.csv", "test.csv", test_size=0.3)

# Stratified split
dpa_core.split_py("data/transactions.csv", "train.csv", "test.csv", stratify="category")

# Reproducible split
dpa_core.split_py("data/transactions.csv", "train.csv", "test.csv", seed=42)

# Verify split
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")
print(f"Training set: {len(train_df)} rows")
print(f"Test set: {len(test_df)} rows")
print(f"Total: {len(train_df) + len(test_df)} rows")

# Check stratification
if 'category' in train_df.columns:
    print("\nCategory distribution in training set:")
    print(train_df['category'].value_counts())
    print("\nCategory distribution in test set:")
    print(test_df['category'].value_counts())
```

## Example 5: Data Filtering

### Extracting Subsets of Data

**Scenario**: You want to filter your data based on specific conditions.

#### CLI Approach

```bash
# Basic filtering
./target/release/dpa filter data/transactions.csv "amount > 1000" filtered_high.csv

# Multiple conditions
./target/release/dpa filter data/transactions.csv "amount > 500 AND category = 'electronics'" filtered_electronics.csv

# Select specific columns with filtering
./target/release/dpa filter data/transactions.csv "country = 'US'" --select "id,amount,date,category" filtered_us.csv

# Complex conditions
./target/release/dpa filter data/transactions.csv "amount BETWEEN 100 AND 1000 AND date >= '2024-01-01'" filtered_range.csv

# Output to different format
./target/release/dpa filter data/transactions.csv "amount > 500" filtered.parquet --format parquet
```

#### Python API Approach

```python
import dpa_core

# Basic filtering
output = dpa_core.filter_py("data/transactions.csv", "amount > 1000", output="filtered_high.csv")

# Multiple conditions
output = dpa_core.filter_py("data/transactions.csv", "amount > 500 AND category = 'electronics'", output="filtered_electronics.csv")

# Select specific columns
output = dpa_core.filter_py(
    "data/transactions.csv", 
    "country = 'US'", 
    select=["id", "amount", "date", "category"], 
    output="filtered_us.csv"
)

# Complex conditions
output = dpa_core.filter_py(
    "data/transactions.csv", 
    "amount BETWEEN 100 AND 1000 AND date >= '2024-01-01'", 
    output="filtered_range.csv"
)

# Verify results
import pandas as pd
original = pd.read_csv("data/transactions.csv")
filtered = pd.read_csv("filtered_high.csv")
print(f"Original: {len(original)} rows")
print(f"Filtered: {len(filtered)} rows")
print(f"Filter ratio: {len(filtered)/len(original)*100:.1f}%")
```

## Example 6: Column Selection

### Working with Specific Columns

**Scenario**: You want to select only specific columns from your dataset.

#### CLI Approach

```bash
# Select specific columns
./target/release/dpa select data/transactions.csv "id,amount,date" selected_columns.csv

# Select all columns except some
./target/release/dpa select data/transactions.csv "!id,!timestamp" selected_except.csv

# Output to different format
./target/release/dpa select data/transactions.csv "amount,date,category" selected.parquet --format parquet
```

#### Python API Approach

```python
import dpa_core

# Select specific columns
output = dpa_core.select_py("data/transactions.csv", ["id", "amount", "date"], output="selected_columns.csv")

# Select all columns except some (using negative selection)
output = dpa_core.select_py("data/transactions.csv", ["!id", "!timestamp"], output="selected_except.csv")

# Verify column selection
import pandas as pd
original = pd.read_csv("data/transactions.csv")
selected = pd.read_csv("selected_columns.csv")
print(f"Original columns: {list(original.columns)}")
print(f"Selected columns: {list(selected.columns)}")
```

## Example 7: Format Conversion

### Converting Between File Formats

**Scenario**: You want to convert your data between different file formats for better performance or compatibility.

#### CLI Approach

```bash
# CSV to Parquet (better performance)
./target/release/dpa convert data/transactions.csv data/transactions.parquet

# Parquet to CSV (for compatibility)
./target/release/dpa convert data/transactions.parquet data/transactions_new.csv

# CSV to JSON
./target/release/dpa convert data/transactions.csv data/transactions.json

# JSON to Parquet
./target/release/dpa convert data/transactions.json data/transactions_from_json.parquet
```

#### Python API Approach

```python
import dpa_core
import time

# CSV to Parquet
start_time = time.time()
output = dpa_core.convert_py("data/transactions.csv", "data/transactions.parquet")
csv_to_parquet_time = time.time() - start_time

# Parquet to CSV
start_time = time.time()
output = dpa_core.convert_py("data/transactions.parquet", "data/transactions_new.csv")
parquet_to_csv_time = time.time() - start_time

print(f"CSV to Parquet: {csv_to_parquet_time:.2f}s")
print(f"Parquet to CSV: {parquet_to_csv_time:.2f}s")

# Compare file sizes
import os
csv_size = os.path.getsize("data/transactions.csv") / 1024 / 1024  # MB
parquet_size = os.path.getsize("data/transactions.parquet") / 1024 / 1024  # MB
print(f"CSV size: {csv_size:.2f} MB")
print(f"Parquet size: {parquet_size:.2f} MB")
print(f"Compression ratio: {csv_size/parquet_size:.1f}x")
```

## Example 8: Complete Data Pipeline

### End-to-End Data Processing

**Scenario**: You want to create a complete data processing pipeline from raw data to ML-ready datasets.

#### Pipeline Steps

1. **Profile the data** to understand its structure
2. **Validate the data** against schemas and rules
3. **Clean the data** by filtering invalid records
4. **Sample the data** for faster processing
5. **Split the data** for machine learning
6. **Convert formats** for optimal performance

#### CLI Pipeline

```bash
#!/bin/bash

echo "Starting DPA Data Pipeline"

# 1. Profile the data
echo "Profiling data..."
./target/release/dpa profile data/raw_transactions.csv --output profile_report.json --format json

# 2. Validate the data
echo "Validating data..."
./target/release/dpa validate data/raw_transactions.csv --schema schema.json --rules validation_rules.json

# 3. Filter out invalid records
echo "Cleaning data..."
./target/release/dpa filter data/raw_transactions.csv "amount > 0 AND date IS NOT NULL" data/clean_transactions.csv

# 4. Sample for faster processing
echo "Sampling data..."
./target/release/dpa sample data/clean_transactions.csv data/sample_transactions.csv --method stratified --stratify category --size 10000

# 5. Split for machine learning
echo "Splitting data..."
./target/release/dpa split data/sample_transactions.csv data/train.csv data/test.csv --test-size 0.2 --stratify category

# 6. Convert to efficient format
echo "Converting formats..."
./target/release/dpa convert data/train.csv data/train.parquet
./target/release/dpa convert data/test.csv data/test.parquet

echo "Pipeline completed successfully!"
```

#### Python Pipeline

```python
import dpa_core
import json
import time
from pathlib import Path

def data_pipeline():
    """Complete data processing pipeline."""
    
    print("Starting DPA Data Pipeline")
    
    # Create output directory
    Path("data/processed").mkdir(exist_ok=True)
    
    # 1. Profile the data
    print("Profiling data...")
    start_time = time.time()
    stats = dpa_core.profile_py("data/raw_transactions.csv")
    profile_time = time.time() - start_time
    
    with open("data/processed/profile_report.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    print(f"   Profiling completed in {profile_time:.2f}s")
    print(f"   Found {stats['total_rows']} rows and {stats['total_columns']} columns")
    
    # 2. Validate the data
    print("Validating data...")
    try:
        dpa_core.validate_py("data/raw_transactions.csv", schema="schema.json", rules="validation_rules.json")
        print("   Validation passed!")
    except RuntimeError as e:
        print(f"   Validation warnings: {e}")
    
    # 3. Clean the data
    print("Cleaning data...")
    dpa_core.filter_py("data/raw_transactions.csv", "amount > 0 AND date IS NOT NULL", output="data/processed/clean_transactions.csv")
    
    # 4. Sample the data
    print("Sampling data...")
    dpa_core.sample_py("data/processed/clean_transactions.csv", "data/processed/sample_transactions.csv", 
                      size=10000, method="stratified", stratify="category")
    
    # 5. Split for ML
    print("Splitting data...")
    dpa_core.split_py("data/processed/sample_transactions.csv", 
                     "data/processed/train.csv", "data/processed/test.csv", 
                     test_size=0.2, stratify="category")
    
    # 6. Convert to efficient format
    print("Converting formats...")
    dpa_core.convert_py("data/processed/train.csv", "data/processed/train.parquet")
    dpa_core.convert_py("data/processed/test.csv", "data/processed/test.parquet")
    
    # Generate summary report
    summary = {
        "pipeline_completed": True,
        "processing_time": time.time() - start_time,
        "output_files": [
            "data/processed/profile_report.json",
            "data/processed/clean_transactions.csv",
            "data/processed/sample_transactions.csv",
            "data/processed/train.csv",
            "data/processed/test.csv",
            "data/processed/train.parquet",
            "data/processed/test.parquet"
        ],
        "statistics": stats
    }
    
    with open("data/processed/pipeline_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("Pipeline completed successfully!")
    print(f"Total processing time: {summary['processing_time']:.2f}s")
    
    return summary

# Run the pipeline
if __name__ == "__main__":
    result = data_pipeline()
```

## Best Practices

### 1. Start Small
- Begin with small datasets to understand the tools
- Use sampling for large files during development
- Test commands on subsets before processing large files

### 2. Use Appropriate Formats
- Use **Parquet** for large datasets (better compression and performance)
- Use **CSV** for compatibility with other tools
- Use **JSON** for web APIs and configuration

### 3. Monitor Performance
- Use the `--detailed` flag sparingly on large datasets
- Monitor memory usage with large files
- Use sampling for profiling large datasets

### 4. Validate Your Data
- Always validate data before processing
- Use schemas to ensure data quality
- Create custom validation rules for business logic

### 5. Reproducible Results
- Use seeds for random operations
- Document your pipeline steps
- Save intermediate results for debugging

## Next Steps

- **Advanced Examples**: Explore [Data Quality](data-quality.md) examples
- **ML Integration**: See [Machine Learning](machine-learning.md) examples
- **Performance**: Learn [Performance Optimization](performance-optimization.md) techniques
- **API Reference**: Check the complete [API documentation](../api/cli-commands.md)

---

**Ready to build your own data processing pipelines?** Start with these examples and customize them for your specific needs!
