# Data Sampling

DPA provides powerful data sampling capabilities for data exploration, testing, and machine learning workflows. The sampling feature supports multiple methods including random sampling, stratified sampling, and systematic sampling.

## Overview

The data sampling feature includes:

- **Random Sampling**: Simple random sampling with optional seeding
- **Stratified Sampling**: Maintains distribution of key columns
- **Systematic Sampling**: Head, tail, and systematic sampling
- **Reproducible Results**: Seeded random sampling for consistent results
- **Performance Optimized**: Efficient sampling for large datasets

## Command Line Usage

### Basic Sampling

```bash
# Random sampling (default)
dpa sample data/transactions.csv -o sample.csv --size 1000

# Stratified sampling
dpa sample data/transactions.csv -o sample.csv --method stratified --stratify country --size 500

# Head sampling (first N rows)
dpa sample data/transactions.csv -o sample.csv --method head --size 100

# Tail sampling (last N rows)
dpa sample data/transactions.csv -o sample.csv --method tail --size 100
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--size, -s` | Sample size | 1000 |
| `--method, -m` | Sampling method: random, stratified, head, tail | random |
| `--stratify` | Column to stratify by (required for stratified) | None |
| `--seed` | Random seed for reproducible sampling | None |

## Python API

```python
import dpa_core

# Random sampling
dpa_core.sample_py("data/transactions.csv", "sample.csv", size=1000)

# Stratified sampling
dpa_core.sample_py("data/transactions.csv", "sample.csv", method="stratified", stratify="country", size=500)

# With seed for reproducibility
dpa_core.sample_py("data/transactions.csv", "sample.csv", size=1000, seed=42)
```

## Sampling Methods

### 1. Random Sampling

Simple random sampling without replacement:

```bash
# Basic random sampling
dpa sample data/transactions.csv -o random_sample.csv --size 1000

# With seed for reproducibility
dpa sample data/transactions.csv -o random_sample.csv --size 1000 --seed 42
```

### 2. Stratified Sampling

Maintains the distribution of a categorical column:

```bash
# Stratified by country
dpa sample data/transactions.csv -o stratified_sample.csv --method stratified --stratify country --size 500

# Stratified by channel
dpa sample data/transactions.csv -o stratified_sample.csv --method stratified --stratify channel --size 300
```

### 3. Head Sampling

Takes the first N rows:

```bash
# First 100 rows
dpa sample data/transactions.csv -o head_sample.csv --method head --size 100
```

### 4. Tail Sampling

Takes the last N rows:

```bash
# Last 100 rows
dpa sample data/transactions.csv -o tail_sample.csv --method tail --size 100
```

## Data Splitting

DPA also provides data splitting functionality for machine learning workflows:

### Train/Test Split

```bash
# Basic 80/20 split
dpa split data/transactions.csv --train train.csv --test test.csv --test-size 0.2

# Stratified split
dpa split data/transactions.csv --train train.csv --test test.csv --test-size 0.2 --stratify country

# With seed for reproducibility
dpa split data/transactions.csv --train train.csv --test test.csv --test-size 0.2 --seed 42
```

### Split Options

| Option | Description | Default |
|--------|-------------|---------|
| `--train` | Output file for training data | Required |
| `--test` | Output file for test data | Required |
| `--test-size, -t` | Proportion for test set (0.0-1.0) | 0.2 |
| `--stratify` | Column to stratify by | None |
| `--seed` | Random seed for reproducible split | None |

## Use Cases

### 1. Data Exploration

```bash
# Quick exploration with small sample
dpa sample large_dataset.csv -o explore_sample.csv --size 1000
dpa profile explore_sample.csv --detailed
```

### 2. Machine Learning

```bash
# Stratified sampling for balanced dataset
dpa sample imbalanced_data.csv -o balanced_sample.csv --method stratified --stratify target --size 5000

# Train/test split
dpa split ml_data.csv --train train.csv --test test.csv --test-size 0.2 --stratify target
```

### 3. Testing and Development

```bash
# Small sample for testing
dpa sample production_data.csv -o test_data.csv --size 100 --seed 123

# Reproducible development data
dpa sample large_file.csv -o dev_sample.csv --size 1000 --seed 42
```

### 4. Performance Testing

```bash
# Different sample sizes for performance testing
for size in 1000 5000 10000 50000; do
    dpa sample large_file.csv -o "sample_${size}.csv" --size $size
done
```

## Best Practices

### 1. Choose Appropriate Sample Size

```bash
# For exploration: 1K-10K rows
dpa sample data.csv -o explore.csv --size 5000

# For testing: 100-1K rows
dpa sample data.csv -o test.csv --size 500

# For ML: 5K-50K rows
dpa sample data.csv -o ml_sample.csv --size 20000
```

### 2. Use Stratified Sampling for Imbalanced Data

```bash
# Maintain class distribution
dpa sample imbalanced.csv -o balanced.csv --method stratified --stratify class --size 5000
```

### 3. Use Seeds for Reproducibility

```bash
# Always use seeds in production
dpa sample data.csv -o sample.csv --size 1000 --seed 42
```

### 4. Validate Sample Quality

```bash
# Check sample distribution
dpa sample data.csv -o sample.csv --method stratified --stratify country --size 1000
dpa profile sample.csv --detailed
```

## Performance Considerations

### 1. Large File Sampling

```bash
# For very large files, use smaller samples
dpa sample huge_file.csv -o sample.csv --size 10000
```

### 2. Memory Usage

```bash
# Check memory before sampling large files
dpa profile large_file.csv | grep "Memory"
```

### 3. Stratified Sampling Performance

```bash
# Stratified sampling is slower but more accurate
# Use for important analyses, not for quick exploration
dpa sample data.csv -o sample.csv --method stratified --stratify category --size 1000
```

## Integration Examples

### Jupyter Notebooks

```python
import dpa_core
import pandas as pd

# Sample data for analysis
dpa_core.sample_py("large_data.csv", "sample.csv", size=5000, seed=42)

# Load sample for analysis
sample_df = pd.read_csv("sample.csv")
print(f"Sample shape: {sample_df.shape}")

# Analyze sample
dpa_core.profile_py("sample.csv")
```

### Machine Learning Pipeline

```python
import dpa_core
from sklearn.model_selection import train_test_split

# Create train/test split
dpa_core.split_py("ml_data.csv", "train.csv", "test.csv", test_size=0.2, stratify="target", seed=42)

# Load data
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

print(f"Train: {len(train_df)}, Test: {len(test_df)}")
```

### Automated Sampling

```bash
#!/bin/bash
# Automated sampling pipeline
for file in data/*.csv; do
    basename=$(basename "$file" .csv)
    
    # Create samples of different sizes
    for size in 1000 5000 10000; do
        dpa sample "$file" -o "samples/${basename}_sample_${size}.csv" --size $size --seed 42
    done
    
    # Create stratified sample
    dpa sample "$file" -o "samples/${basename}_stratified.csv" --method stratified --stratify country --size 5000 --seed 42
done
```

## Troubleshooting

### Common Issues

1. **Stratified Sampling Errors**
   ```bash
   # Ensure stratification column exists
   dpa schema data.csv | grep country
   ```

2. **Sample Size Too Large**
   ```bash
   # Check total rows first
   dpa profile data.csv | grep "Total Rows"
   ```

3. **Memory Issues**
   ```bash
   # Use smaller samples for large files
   dpa sample large_file.csv -o sample.csv --size 1000
   ```

### Error Messages

- `"--stratify column required"`: Specify stratification column
- `"Sample size exceeds total rows"`: Reduce sample size
- `"Column not found"`: Check column names

## Advanced Features

### Custom Sampling Scripts

```python
import dpa_core
import pandas as pd

def progressive_sampling(file_path, sizes=[1000, 5000, 10000]):
    """Create progressive samples for analysis"""
    samples = {}
    
    for size in sizes:
        output_file = f"sample_{size}.csv"
        dpa_core.sample_py(file_path, output_file, size=size, seed=42)
        samples[size] = pd.read_csv(output_file)
    
    return samples

# Usage
samples = progressive_sampling("data.csv")
for size, df in samples.items():
    print(f"Sample {size}: {len(df)} rows")
```

### Quality Assessment

```python
import dpa_core

def assess_sample_quality(original_file, sample_file, stratify_col=None):
    """Assess sample quality compared to original"""
    
    # Profile both files
    original_profile = dpa_core.profile_py(original_file)
    sample_profile = dpa_core.profile_py(sample_file)
    
    # Compare distributions
    if stratify_col:
        print(f"Original {stratify_col} distribution:")
        # Add distribution comparison logic
        
    print(f"Sample represents {sample_profile['rows']}/{original_profile['rows']} rows")
    
    return sample_profile

# Usage
assess_sample_quality("data.csv", "sample.csv", "country")
```

This comprehensive sampling system provides the tools needed for effective data exploration, testing, and machine learning workflows.

