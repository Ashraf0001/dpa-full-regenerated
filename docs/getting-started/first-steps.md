# First Steps with DPA

Welcome to your first steps with Data Processing Accelerator (DPA)! This guide will walk you through your first data processing tasks.

## Prerequisites

Before starting, ensure you have:

- ✅ DPA installed (see [Installation Guide](installation.md))
- ✅ A sample dataset to work with
- ✅ Basic familiarity with command line or Python

## Getting Your First Dataset

### Option 1: Use Sample Data

DPA comes with sample datasets for testing:

```bash
# Check available sample data
ls data/
ls test_data/
```

### Option 2: Create Your Own

Create a simple CSV file for testing:

```bash
# Create a sample CSV file
cat > sample_data.csv << EOF
id,name,age,city,salary
1,Alice,25,New York,50000
2,Bob,30,San Francisco,75000
3,Charlie,35,Chicago,60000
4,Diana,28,Boston,65000
5,Eve,32,Seattle,70000
EOF
```

## Your First DPA Operations

### Step 1: Explore Your Data

Start by understanding your data structure:

```bash
# View the first few rows
./target/release/dpa head sample_data.csv -n 5

# Get schema information
./target/release/dpa schema sample_data.csv
```

### Step 2: Profile Your Data

Get comprehensive insights about your data:

```bash
# Basic profiling
./target/release/dpa profile sample_data.csv

# Detailed profiling with statistics
./target/release/dpa profile sample_data.csv --detailed
```

### Step 3: Validate Your Data

Check data quality and consistency:

```bash
# Basic validation
./target/release/dpa validate sample_data.csv

# Create a simple schema for validation
cat > schema.json << EOF
{
  "columns": {
    "id": {"type": "integer", "nullable": false},
    "name": {"type": "string", "nullable": false},
    "age": {"type": "integer", "min": 18, "max": 100},
    "city": {"type": "string", "nullable": false},
    "salary": {"type": "float", "min": 0}
  }
}
EOF

# Validate against schema
./target/release/dpa validate sample_data.csv --schema schema.json
```

### Step 4: Sample Your Data

Create smaller datasets for testing:

```bash
# Random sampling
./target/release/dpa sample sample_data.csv sample_random.csv --method random --size 3

# Stratified sampling (if you have categorical data)
./target/release/dpa sample sample_data.csv sample_stratified.csv --method stratified --stratify city
```

### Step 5: Transform Your Data

Convert between file formats:

```bash
# Convert CSV to Parquet
./target/release/dpa convert sample_data.csv sample_data.parquet

# Convert Parquet back to CSV
./target/release/dpa convert sample_data.parquet sample_data_new.csv
```

## Using Python API

### Basic Python Operations

```python
import dpa_core
import pandas as pd

# Profile data
stats = dpa_core.profile_py("sample_data.csv")
print("Data Statistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")

# Sample data
dpa_core.sample_py("sample_data.csv", "python_sample.csv", size=3, method="random")

# Validate data
try:
    dpa_core.validate_py("sample_data.csv")
    print("✅ Data validation passed!")
except Exception as e:
    print(f"❌ Validation failed: {e}")

# Filter data
dpa_core.filter_py("sample_data.csv", "age > 30", output="filtered_data.csv")

# Select columns
dpa_core.select_py("sample_data.csv", ["name", "age", "salary"], output="selected_data.csv")
```

### Working with Results

```python
# Read the results back into Python
import pandas as pd

# Read original data
df = pd.read_csv("sample_data.csv")
print("Original data shape:", df.shape)

# Read filtered data
filtered_df = pd.read_csv("filtered_data.csv")
print("Filtered data shape:", filtered_df.shape)

# Read sampled data
sampled_df = pd.read_csv("python_sample.csv")
print("Sampled data shape:", sampled_df.shape)
```

## Common Workflows

### Data Exploration Workflow

```bash
# 1. Quick overview
./target/release/dpa head your_data.csv -n 10

# 2. Schema inspection
./target/release/dpa schema your_data.csv

# 3. Detailed profiling
./target/release/dpa profile your_data.csv --detailed

# 4. Data validation
./target/release/dpa validate your_data.csv
```

### Data Preparation Workflow

```bash
# 1. Sample for development
./target/release/dpa sample your_data.csv dev_sample.csv --method random --size 1000

# 2. Validate sample
./target/release/dpa validate dev_sample.csv

# 3. Convert to efficient format
./target/release/dpa convert dev_sample.csv dev_sample.parquet

# 4. Create train/test split
./target/release/dpa split dev_sample.csv train.csv test.csv --test-size 0.2
```

### Quality Assurance Workflow

```python
import dpa_core

# 1. Profile data
stats = dpa_core.profile_py("your_data.csv")

# 2. Check for issues
if float(stats.get("null_percentage", 0)) > 0.1:
    print("⚠️  High null percentage detected")

# 3. Validate data
try:
    dpa_core.validate_py("your_data.csv")
    print("✅ Data quality check passed")
except Exception as e:
    print(f"❌ Quality issues found: {e}")

# 4. Create clean sample
dpa_core.sample_py("your_data.csv", "clean_sample.csv", size=1000, method="random")
```

## Tips for Beginners

### 1. Start Small
- Begin with small datasets to understand the tools
- Use the sample data provided with DPA
- Test commands on subsets before processing large files

### 2. Use Help Commands
```bash
# Get help for any command
./target/release/dpa --help
./target/release/dpa profile --help
./target/release/dpa sample --help
```

### 3. Check File Formats
- DPA supports CSV, Parquet, and JSON
- Use Parquet for large datasets (better compression)
- Use CSV for compatibility with other tools

### 4. Monitor Performance
- Start with small sample sizes
- Use `--detailed` flag sparingly on large datasets
- Monitor memory usage with large files

## Next Steps

Now that you've completed your first steps:

1. 🎯 **Explore Features**: Learn about [Data Profiling](../features/data-profiling.md), [Validation](../features/data-validation.md), and [Sampling](../features/data-sampling.md)
2. 📚 **Try Examples**: Work through [Basic Usage](../examples/basic-usage.md) examples
3. 🔧 **Learn Configuration**: Understand [Configuration Options](../getting-started/configuration.md)
4. 🚀 **Scale Up**: Move to larger datasets and more complex workflows

## Getting Help

- 📖 **Documentation**: Browse the full documentation
- 💡 **Examples**: Check the examples directory
- 🐛 **Issues**: Report problems on GitHub
- 💬 **Community**: Join discussions

---

**Congratulations! You've taken your first steps with DPA.** 🎉

Ready to accelerate your data processing journey!
