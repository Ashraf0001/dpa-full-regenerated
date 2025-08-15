# Python API Reference

Complete reference for the DPA Python API with PyO3 bindings.

## Overview

DPA provides a comprehensive Python API through PyO3 bindings, offering high-performance data processing functions that can be seamlessly integrated into Python workflows.

## Installation

### From Source

```bash
# Install maturin
pip install maturin

# Build and install Python bindings
maturin develop
```

### Import

```python
import dpa_core
```

## Core Functions

### `profile_py()` - Data Profiling

Generate comprehensive data profiling reports.

```python
dpa_core.profile_py(input: str) -> dict
```

**Parameters:**
- `input` (str): Path to input file (CSV, Parquet, or JSON)

**Returns:**
- `dict`: Dictionary containing profiling statistics

**Example:**
```python
import dpa_core

# Basic profiling
stats = dpa_core.profile_py("data.csv")
print(stats)

# Access specific statistics
print(f"Total rows: {stats['total_rows']}")
print(f"Total columns: {stats['total_columns']}")
print(f"Memory usage: {stats['memory_usage']}")
```

**Return Value Structure:**
```python
{
    'total_rows': 10000,
    'total_columns': 5,
    'memory_usage': '2.3 MB',
    'file_size': '1.8 MB',
    'processing_time': '0.8s',
    'columns': {
        'id': {
            'type': 'Int64',
            'null_count': 0,
            'null_percentage': 0.0,
            'unique_count': 10000,
            'min': 1,
            'max': 10000,
            'mean': 5000.5,
            'std': 2886.9
        },
        'name': {
            'type': 'String',
            'null_count': 0,
            'null_percentage': 0.0,
            'unique_count': 9850,
            'avg_length': 12.3
        }
        # ... more columns
    }
}
```

### `validate_py()` - Data Validation

Validate data against schemas and rules.

```python
dpa_core.validate_py(
    input: str,
    schema: Optional[str] = None,
    rules: Optional[str] = None
) -> None
```

**Parameters:**
- `input` (str): Path to input file
- `schema` (str, optional): Path to schema file
- `rules` (str, optional): Path to validation rules file

**Raises:**
- `RuntimeError`: If validation fails

**Example:**
```python
import dpa_core

# Basic validation
try:
    dpa_core.validate_py("data.csv")
    print("✅ Validation passed!")
except RuntimeError as e:
    print(f"❌ Validation failed: {e}")

# Schema validation
try:
    dpa_core.validate_py("data.csv", schema="schema.json")
    print("✅ Schema validation passed!")
except RuntimeError as e:
    print(f"❌ Schema validation failed: {e}")

# Custom rules validation
try:
    dpa_core.validate_py("data.csv", rules="rules.json")
    print("✅ Rules validation passed!")
except RuntimeError as e:
    print(f"❌ Rules validation failed: {e}")
```

### `sample_py()` - Data Sampling

Create samples from datasets using various methods.

```python
dpa_core.sample_py(
    input: str,
    output: str,
    size: Optional[int] = None,
    method: Optional[str] = None,
    stratify: Optional[str] = None,
    seed: Optional[int] = None
) -> None
```

**Parameters:**
- `input` (str): Path to input file
- `output` (str): Path to output file
- `size` (int, optional): Sample size (default: 1000)
- `method` (str, optional): Sampling method - "random", "stratified", "head", "tail" (default: "random")
- `stratify` (str, optional): Column for stratified sampling
- `seed` (int, optional): Random seed for reproducibility

**Example:**
```python
import dpa_core

# Random sampling
dpa_core.sample_py("data.csv", "sample.csv", size=1000, method="random")

# Stratified sampling
dpa_core.sample_py("data.csv", "sample.csv", size=500, method="stratified", stratify="category")

# Head sampling
dpa_core.sample_py("data.csv", "sample.csv", size=100, method="head")

# With seed for reproducibility
dpa_core.sample_py("data.csv", "sample.csv", size=1000, method="random", seed=42)
```

### `split_py()` - Train/Test Split

Split datasets into training and test sets.

```python
dpa_core.split_py(
    input: str,
    train_output: str,
    test_output: str,
    test_size: Optional[float] = None,
    stratify: Optional[str] = None,
    seed: Optional[int] = None
) -> None
```

**Parameters:**
- `input` (str): Path to input file
- `train_output` (str): Path to training set output file
- `test_output` (str): Path to test set output file
- `test_size` (float, optional): Test set fraction (default: 0.2)
- `stratify` (str, optional): Column for stratified splitting
- `seed` (int, optional): Random seed for reproducibility

**Example:**
```python
import dpa_core

# Basic split
dpa_core.split_py("data.csv", "train.csv", "test.csv")

# Custom test size
dpa_core.split_py("data.csv", "train.csv", "test.csv", test_size=0.3)

# Stratified split
dpa_core.split_py("data.csv", "train.csv", "test.csv", stratify="category")

# With seed
dpa_core.split_py("data.csv", "train.csv", "test.csv", seed=42)
```

### `filter_py()` - Data Filtering

Filter data using SQL-like expressions.

```python
dpa_core.filter_py(
    input: str,
    where_expr: str,
    select: Optional[List[str]] = None,
    output: Optional[str] = None
) -> str
```

**Parameters:**
- `input` (str): Path to input file
- `where_expr` (str): Filter expression (SQL-like)
- `select` (List[str], optional): List of columns to select
- `output` (str, optional): Path to output file

**Returns:**
- `str`: Path to output file

**Example:**
```python
import dpa_core

# Basic filtering
output = dpa_core.filter_py("data.csv", "age > 30", output="filtered.csv")

# Filter with column selection
output = dpa_core.filter_py(
    "data.csv", 
    "salary > 50000", 
    select=["name", "age", "salary"], 
    output="filtered.csv"
)

# Complex expression
output = dpa_core.filter_py(
    "data.csv", 
    "age > 25 AND salary > 40000 AND city = 'New York'", 
    output="filtered.csv"
)
```

### `select_py()` - Column Selection

Select specific columns from datasets.

```python
dpa_core.select_py(
    input: str,
    columns: List[str],
    output: Optional[str] = None
) -> str
```

**Parameters:**
- `input` (str): Path to input file
- `columns` (List[str]): List of column names to select
- `output` (str, optional): Path to output file

**Returns:**
- `str`: Path to output file

**Example:**
```python
import dpa_core

# Select specific columns
output = dpa_core.select_py("data.csv", ["name", "age", "salary"], output="selected.csv")

# Select all columns except some (using negative selection)
output = dpa_core.select_py("data.csv", ["!id", "!timestamp"], output="selected.csv")
```

### `convert_py()` - Format Conversion

Convert between different file formats.

```python
dpa_core.convert_py(input: str, output: str) -> str
```

**Parameters:**
- `input` (str): Path to input file
- `output` (str): Path to output file

**Returns:**
- `str`: Path to output file

**Example:**
```python
import dpa_core

# CSV to Parquet
output = dpa_core.convert_py("data.csv", "data.parquet")

# Parquet to CSV
output = dpa_core.convert_py("data.parquet", "data.csv")

# CSV to JSON
output = dpa_core.convert_py("data.csv", "data.json")

# JSON to Parquet
output = dpa_core.convert_py("data.json", "data.parquet")
```

## Advanced Usage

### Error Handling

```python
import dpa_core

def safe_validate(file_path: str, schema_path: str = None) -> bool:
    """Safely validate a file with optional schema."""
    try:
        if schema_path:
            dpa_core.validate_py(file_path, schema=schema_path)
        else:
            dpa_core.validate_py(file_path)
        return True
    except RuntimeError as e:
        print(f"Validation failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Usage
if safe_validate("data.csv", "schema.json"):
    print("Data is valid!")
else:
    print("Data validation failed!")
```

### Batch Processing

```python
import dpa_core
import os
from pathlib import Path

def process_directory(input_dir: str, output_dir: str):
    """Process all CSV files in a directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for csv_file in input_path.glob("*.csv"):
        # Profile each file
        stats = dpa_core.profile_py(str(csv_file))
        print(f"Processed {csv_file.name}: {stats['total_rows']} rows")
        
        # Sample each file
        sample_file = output_path / f"sample_{csv_file.name}"
        dpa_core.sample_py(str(csv_file), str(sample_file), size=1000)
        
        # Convert to Parquet
        parquet_file = output_path / f"{csv_file.stem}.parquet"
        dpa_core.convert_py(str(csv_file), str(parquet_file))

# Usage
process_directory("raw_data", "processed_data")
```

### Data Quality Pipeline

```python
import dpa_core
import pandas as pd

def data_quality_pipeline(input_file: str, output_dir: str):
    """Complete data quality assessment pipeline."""
    
    # 1. Profile the data
    print("📊 Profiling data...")
    stats = dpa_core.profile_py(input_file)
    
    # 2. Check for quality issues
    quality_issues = []
    for col, col_stats in stats['columns'].items():
        if col_stats['null_percentage'] > 0.1:
            quality_issues.append(f"High null percentage in {col}: {col_stats['null_percentage']}%")
    
    # 3. Validate the data
    print("🔍 Validating data...")
    try:
        dpa_core.validate_py(input_file)
        print("✅ Data validation passed!")
    except RuntimeError as e:
        quality_issues.append(f"Validation failed: {e}")
    
    # 4. Create clean sample
    print("🎯 Creating sample...")
    sample_file = f"{output_dir}/clean_sample.csv"
    dpa_core.sample_py(input_file, sample_file, size=1000, method="random")
    
    # 5. Create train/test split
    print("✂️  Creating train/test split...")
    train_file = f"{output_dir}/train.csv"
    test_file = f"{output_dir}/test.csv"
    dpa_core.split_py(sample_file, train_file, test_file, test_size=0.2)
    
    # 6. Generate report
    report = {
        'input_file': input_file,
        'total_rows': stats['total_rows'],
        'total_columns': stats['total_columns'],
        'quality_issues': quality_issues,
        'sample_file': sample_file,
        'train_file': train_file,
        'test_file': test_file
    }
    
    return report

# Usage
report = data_quality_pipeline("data.csv", "output")
print("Pipeline completed!")
print(f"Quality issues found: {len(report['quality_issues'])}")
```

### Performance Monitoring

```python
import dpa_core
import time
import psutil

def monitor_performance(func, *args, **kwargs):
    """Monitor performance of DPA operations."""
    process = psutil.Process()
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.time()
    
    try:
        result = func(*args, **kwargs)
        success = True
    except Exception as e:
        result = e
        success = False
    
    end_time = time.time()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    performance = {
        'success': success,
        'execution_time': end_time - start_time,
        'memory_used': end_memory - start_memory,
        'result': result
    }
    
    return performance

# Usage
perf = monitor_performance(dpa_core.profile_py, "large_data.csv")
print(f"Execution time: {perf['execution_time']:.2f}s")
print(f"Memory used: {perf['memory_used']:.2f}MB")
```

## Integration Examples

### With Pandas

```python
import dpa_core
import pandas as pd

# Use DPA for heavy operations, Pandas for analysis
def hybrid_processing(data_file: str):
    # Use DPA for profiling
    stats = dpa_core.profile_py(data_file)
    
    # Use DPA for sampling large files
    dpa_core.sample_py(data_file, "sample.csv", size=10000)
    
    # Use Pandas for analysis
    df = pd.read_csv("sample.csv")
    
    # Continue with Pandas operations
    summary = df.describe()
    correlations = df.corr()
    
    return stats, summary, correlations
```

### With NumPy

```python
import dpa_core
import numpy as np
import pandas as pd

def statistical_analysis(data_file: str):
    # Get basic stats from DPA
    stats = dpa_core.profile_py(data_file)
    
    # Load data for detailed analysis
    df = pd.read_csv(data_file)
    
    # Use NumPy for advanced statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    advanced_stats = {}
    for col in numeric_cols:
        values = df[col].dropna()
        advanced_stats[col] = {
            'skewness': float(np.corrcoef(values, np.arange(len(values)))[0, 1]),
            'kurtosis': float(np.corrcoef(values, np.arange(len(values))**2)[0, 1]),
            'percentiles': np.percentile(values, [25, 50, 75]).tolist()
        }
    
    return stats, advanced_stats
```

### With Scikit-learn

```python
import dpa_core
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def ml_pipeline(data_file: str):
    # Use DPA for data preparation
    dpa_core.sample_py(data_file, "sample.csv", size=10000, method="stratified", stratify="target")
    dpa_core.split_py("sample.csv", "train.csv", "test.csv", test_size=0.2, stratify="target")
    
    # Load data for ML
    train_df = pd.read_csv("train.csv")
    test_df = pd.read_csv("test.csv")
    
    # Prepare features
    X_train = train_df.drop('target', axis=1)
    y_train = train_df['target']
    X_test = test_df.drop('target', axis=1)
    y_test = test_df['target']
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    score = model.score(X_test, y_test)
    
    return model, score
```

## Best Practices

### 1. Error Handling

```python
def robust_dpa_operation(operation_func, *args, **kwargs):
    """Wrapper for robust DPA operations."""
    try:
        return operation_func(*args, **kwargs)
    except RuntimeError as e:
        print(f"DPA operation failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

### 2. Memory Management

```python
import gc

def memory_efficient_processing(data_file: str):
    """Memory-efficient data processing."""
    # Process in chunks
    dpa_core.sample_py(data_file, "sample.csv", size=5000)
    
    # Force garbage collection
    gc.collect()
    
    # Continue processing
    stats = dpa_core.profile_py("sample.csv")
    
    return stats
```

### 3. Configuration

```python
import os

def configure_dpa():
    """Configure DPA for optimal performance."""
    os.environ['DPA_MAX_MEMORY'] = '4GB'
    os.environ['DPA_NUM_THREADS'] = '4'
    os.environ['DPA_LOG_LEVEL'] = 'info'
```

## Troubleshooting

### Common Issues

**1. Import Error**
```python
# Solution: Reinstall Python bindings
# pip install maturin
# maturin develop --force-reinstall
```

**2. Memory Error**
```python
# Solution: Reduce memory usage
import os
os.environ['DPA_MAX_MEMORY'] = '2GB'
```

**3. File Not Found**
```python
# Solution: Check file paths
import os
if not os.path.exists("data.csv"):
    print("File not found!")
```

### Debugging

```python
import dpa_core
import traceback

def debug_dpa_operation(operation_func, *args, **kwargs):
    """Debug DPA operations with detailed error information."""
    try:
        return operation_func(*args, **kwargs)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None
```

## Next Steps

- 📖 **CLI Commands**: Learn about [CLI Commands](cli-commands.md)
- 🎯 **Examples**: See practical examples in the [Examples](../examples/) section
- 🔧 **Configuration**: Understand [Configuration Options](configuration.md)
- 🚀 **Advanced Usage**: Explore [Best Practices](../user-guide/best-practices.md)

---

**Ready to use the Python API?** Start with the [Quick Start Guide](../getting-started/quick-start.md) to get familiar with the functions.
