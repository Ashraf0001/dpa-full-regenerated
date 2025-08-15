# Data Profiling

DPA provides comprehensive data profiling capabilities that go beyond simple statistics to give you deep insights into your data quality, structure, and characteristics.

## Overview

The enhanced profiling feature analyzes your data and provides:

- **Basic Statistics**: Row/column counts, memory usage, data types
- **Data Quality Metrics**: Null percentages, unique value counts
- **Statistical Summaries**: Min, max, mean, standard deviation, percentiles
- **Value Distributions**: Most common values, average string lengths
- **Outlier Detection**: Statistical outliers and anomalies

## Command Line Usage

### Basic Profiling

```bash
# Basic profile with default settings
dpa profile data/transactions.csv

# Profile with custom sample size
dpa profile data/transactions.csv --sample 500000

# Detailed profiling with statistics
dpa profile data/transactions.csv --detailed
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--sample, -s` | Sample size for profiling | 1,000,000 |
| `--detailed, -d` | Show detailed statistics | false |

## Python API

```python
import dpa_core

# Basic profiling
profile = dpa_core.profile_py("data/transactions.csv")

# Access profiling results
print(f"Rows: {profile['rows']}")
print(f"Columns: {profile['columns']}")
print(f"Memory Usage: {profile['memory_mb']} MB")
print(f"Null Percentage: {profile['null_percentage']}%")

# Column-specific information
for col in ['user_id', 'amount', 'country']:
    dtype_key = f"dtype:{col}"
    nulls_key = f"nulls:{col}"
    unique_key = f"unique:{col}"
    
    if dtype_key in profile:
        print(f"{col}: {profile[dtype_key]}, nulls={profile[nulls_key]}, unique={profile[unique_key]}")
```

## Output Format

### Basic Profile Output

```
📊 Data Profile Report
==================================================
📁 File: data/transactions.csv
📈 Total Rows: 501
📋 Total Columns: 5
💾 Memory Usage: ~0.02 MB

📋 Column Overview:
Column               Type         Nulls      Null %    Unique    
----------------------------------------------------------------------
user_id             Int64        0          0.0%      501       
amount              Float64      0          0.0%      501       
country             Utf8         0          0.0%      6         
timestamp           Int64        0          0.0%      501       
channel             Utf8         0          0.0%      3         

🔍 Data Quality Summary:
==================================================
📊 Overall Null Percentage: 0.00%
🔢 Total Null Values: 0
✅ Complete Rows: 501
```

### Detailed Profile Output

When using `--detailed`, you get additional statistical information:

```
📊 Detailed Statistics:
==================================================

🔢 amount (Numeric):
   Min: 2.9400
   Max: 167.5800
   Mean: 37.2347
   Std: 32.4567
   Q1 (25%): 15.5300
   Q3 (75%): 51.4100
   IQR: 35.8800

📝 country (Text):
   Avg Length: 2.0 chars
   Top 5 Values:
     'US': 125 times
     'IT': 98 times
     'DE': 87 times
     'ES': 85 times
     'NL': 67 times
```

## Use Cases

### 1. Data Quality Assessment

```bash
# Quick quality check
dpa profile data/dataset.csv | grep "Null %"
```

### 2. Memory Usage Optimization

```bash
# Check memory usage before processing large files
dpa profile large_file.csv | grep "Memory Usage"
```

### 3. Schema Discovery

```bash
# Understand data structure
dpa profile new_dataset.csv --detailed
```

### 4. Outlier Detection

```bash
# Find potential data issues
dpa profile data.csv --detailed | grep -A 10 "outliers"
```

## Performance Considerations

- **Sampling**: Large files are automatically sampled (default: 1M rows)
- **Memory Efficient**: Uses lazy evaluation for large datasets
- **Parallel Processing**: Statistical calculations are parallelized

## Tips and Best Practices

### 1. Choose Appropriate Sample Size

```bash
# For large files, use smaller samples for quick analysis
dpa profile huge_file.csv --sample 100000

# For small files, use full dataset
dpa profile small_file.csv --sample 1000000
```

### 2. Use Detailed Mode for Analysis

```bash
# Always use --detailed for data exploration
dpa profile data.csv --detailed > profile_report.txt
```

### 3. Monitor Memory Usage

```bash
# Check memory before processing
dpa profile data.csv | grep "Memory"
```

### 4. Validate Data Types

```bash
# Check for mixed data types
dpa profile data.csv --detailed | grep "mixed_types"
```

## Integration with Other Tools

### Jupyter Notebooks

```python
import dpa_core
import pandas as pd

# Profile data and create pandas DataFrame
profile = dpa_core.profile_py("data.csv")
profile_df = pd.DataFrame(list(profile.items()), columns=['Metric', 'Value'])
profile_df
```

### Data Validation Pipeline

```bash
# Profile first, then validate
dpa profile data.csv --detailed
dpa validate data.csv --schema schema.json
```

### ETL Workflows

```bash
# Profile before and after transformations
dpa profile raw_data.csv > before_profile.txt
dpa filter raw_data.csv -w "amount > 0" -o clean_data.csv
dpa profile clean_data.csv > after_profile.txt
```

## Troubleshooting

### Common Issues

1. **Memory Errors**: Reduce sample size
   ```bash
   dpa profile large_file.csv --sample 100000
   ```

2. **Slow Performance**: Use basic profiling for large files
   ```bash
   dpa profile large_file.csv  # Skip --detailed
   ```

3. **Encoding Issues**: Ensure proper file encoding
   ```bash
   # Check file encoding first
   file -i data.csv
   ```

### Error Messages

- `"File not found"`: Check file path and permissions
- `"Invalid sample size"`: Use positive integers
- `"Memory allocation failed"`: Reduce sample size or use smaller files

## Advanced Features

### Custom Profiling Scripts

```python
import dpa_core
import json

def custom_profile(file_path):
    """Custom profiling with specific metrics"""
    profile = dpa_core.profile_py(file_path)
    
    # Extract specific metrics
    metrics = {
        'file_size_mb': profile.get('memory_mb', 0),
        'total_rows': int(profile.get('rows', 0)),
        'null_percentage': float(profile.get('null_percentage', 0)),
        'columns': int(profile.get('columns', 0))
    }
    
    return metrics

# Usage
metrics = custom_profile("data.csv")
print(json.dumps(metrics, indent=2))
```

### Batch Profiling

```bash
#!/bin/bash
# Profile multiple files
for file in data/*.csv; do
    echo "Profiling $file..."
    dpa profile "$file" --detailed > "profiles/$(basename "$file" .csv)_profile.txt"
done
```

This enhanced profiling feature provides the foundation for understanding your data quality and structure, enabling better decision-making in data processing workflows.

