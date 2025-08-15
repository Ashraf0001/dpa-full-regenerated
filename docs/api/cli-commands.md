# CLI Commands Reference

Complete reference for all DPA command-line interface commands.

## Overview

DPA provides a comprehensive CLI with commands for data processing, profiling, validation, and more. All commands follow a consistent pattern:

```bash
./target/release/dpa <command> [options] <arguments>
```

## Global Options

All commands support these global options:

```bash
--help, -h          Show help for the command
--version, -V       Show version information
--config <file>     Use specified configuration file
--log-level <level> Set log level (debug, info, warn, error)
--quiet, -q         Suppress output
--verbose, -v       Increase verbosity
```

## Commands

### `schema` - Print Schema Information

Display the schema and structure of a data file.

```bash
./target/release/dpa schema <input>
```

**Arguments:**
- `input` - Input file path (CSV, Parquet, or JSON)

**Options:**
- `--format <format>` - Output format (table, json, yaml)
- `--detailed` - Show detailed column information

**Examples:**
```bash
# Basic schema
./target/release/dpa schema data.csv

# Detailed schema in JSON format
./target/release/dpa schema data.csv --format json --detailed

# Schema for Parquet file
./target/release/dpa schema data.parquet
```

**Output:**
```
Schema for data.csv:
┌─────────┬─────────┬─────────┬─────────┐
│ Column  │ Type    │ Nullable│ Count   │
├─────────┼─────────┼─────────┼─────────┤
│ id      │ Int64   │ false   │ 1000    │
│ name    │ String  │ false   │ 1000    │
│ age     │ Int64   │ true    │ 950     │
│ salary  │ Float64 │ true    │ 980     │
└─────────┴─────────┴─────────┴─────────┘
```

### `head` - Preview Data

Display the first N rows of a data file.

```bash
./target/release/dpa head [options] <input>
```

**Arguments:**
- `input` - Input file path

**Options:**
- `-n, --n <number>` - Number of rows to display (default: 10)
- `--format <format>` - Output format (table, csv, json)

**Examples:**
```bash
# Show first 10 rows
./target/release/dpa head data.csv

# Show first 5 rows
./target/release/dpa head data.csv -n 5

# Show in JSON format
./target/release/dpa head data.csv --format json
```

### `profile` - Data Profiling

Generate comprehensive data profiling reports.

```bash
./target/release/dpa profile [options] <input>
```

**Arguments:**
- `input` - Input file path

**Options:**
- `--detailed` - Include detailed statistics
- `--sample <size>` - Sample size for large datasets
- `--output <file>` - Save report to file
- `--format <format>` - Output format (table, json, html)

**Examples:**
```bash
# Basic profiling
./target/release/dpa profile data.csv

# Detailed profiling with sampling
./target/release/dpa profile data.csv --detailed --sample 10000

# Save report to file
./target/release/dpa profile data.csv --output report.json --format json
```

**Output:**
```
📊 Data Profile Report
=====================

📁 File: data.csv
📏 Shape: 10,000 rows × 5 columns
💾 Size: 2.3 MB
⏱️  Processing time: 0.8s

📈 Column Statistics:
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Column  │ Type    │ Null %  │ Unique  │ Min     │ Max     │
├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ id      │ Int64   │ 0.0%    │ 10,000  │ 1       │ 10,000  │
│ name    │ String  │ 0.0%    │ 9,850   │ -       │ -       │
│ age     │ Int64   │ 5.0%    │ 45      │ 18      │ 85      │
│ salary  │ Float64 │ 2.0%    │ 8,950   │ 25,000  │ 150,000 │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
```

### `validate` - Data Validation

Validate data against schemas and rules.

```bash
./target/release/dpa validate [options] <input>
```

**Arguments:**
- `input` - Input file path

**Options:**
- `--schema <file>` - Schema file for validation
- `--rules <file>` - Custom validation rules file
- `--output <file>` - Save validation report
- `--max-errors <number>` - Maximum errors to report (default: 1000)
- `--strict` - Fail on first error

**Examples:**
```bash
# Basic validation
./target/release/dpa validate data.csv

# Schema validation
./target/release/dpa validate data.csv --schema schema.json

# Custom rules validation
./target/release/dpa validate data.csv --rules rules.json

# Strict validation
./target/release/dpa validate data.csv --schema schema.json --strict
```

**Output:**
```
✅ Data Validation Report
========================

📁 File: data.csv
🔍 Validation: PASSED
⏱️  Processing time: 0.3s

📊 Summary:
- ✅ Schema validation: PASSED
- ✅ Data type validation: PASSED
- ✅ Range validation: PASSED
- ⚠️  Custom rules: 2 warnings

⚠️  Warnings:
- Column 'age': 5 values outside expected range (18-65)
- Column 'salary': 3 negative values detected
```

### `sample` - Data Sampling

Create samples from datasets using various methods.

```bash
./target/release/dpa sample [options] <input> <output>
```

**Arguments:**
- `input` - Input file path
- `output` - Output file path

**Options:**
- `--method <method>` - Sampling method (random, stratified, head, tail)
- `--size <number>` - Sample size
- `--stratify <column>` - Column for stratified sampling
- `--seed <number>` - Random seed for reproducibility
- `--format <format>` - Output format (csv, parquet, json)

**Examples:**
```bash
# Random sampling
./target/release/dpa sample data.csv sample.csv --method random --size 1000

# Stratified sampling
./target/release/dpa sample data.csv sample.csv --method stratified --stratify category --size 500

# Head sampling
./target/release/dpa sample data.csv sample.csv --method head --size 100

# With seed for reproducibility
./target/release/dpa sample data.csv sample.csv --method random --size 1000 --seed 42
```

### `split` - Train/Test Split

Split datasets into training and test sets.

```bash
./target/release/dpa split [options] <input> <train_output> <test_output>
```

**Arguments:**
- `input` - Input file path
- `train_output` - Training set output file
- `test_output` - Test set output file

**Options:**
- `--test-size <fraction>` - Test set fraction (default: 0.2)
- `--stratify <column>` - Column for stratified splitting
- `--seed <number>` - Random seed for reproducibility
- `--format <format>` - Output format (csv, parquet, json)

**Examples:**
```bash
# Basic split
./target/release/dpa split data.csv train.csv test.csv

# Custom test size
./target/release/dpa split data.csv train.csv test.csv --test-size 0.3

# Stratified split
./target/release/dpa split data.csv train.csv test.csv --stratify category

# With seed
./target/release/dpa split data.csv train.csv test.csv --seed 42
```

### `filter` - Data Filtering

Filter data using SQL-like expressions.

```bash
./target/release/dpa filter [options] <input> <expression> [output]
```

**Arguments:**
- `input` - Input file path
- `expression` - Filter expression (SQL-like)
- `output` - Output file path (optional)

**Options:**
- `--select <columns>` - Select specific columns
- `--format <format>` - Output format (csv, parquet, json)

**Examples:**
```bash
# Basic filtering
./target/release/dpa filter data.csv "age > 30" filtered.csv

# Filter with column selection
./target/release/dpa filter data.csv "salary > 50000" --select "name,age,salary" filtered.csv

# Complex expression
./target/release/dpa filter data.csv "age > 25 AND salary > 40000 AND city = 'New York'" filtered.csv

# Output to different format
./target/release/dpa filter data.csv "age > 30" filtered.parquet --format parquet
```

### `select` - Column Selection

Select specific columns from datasets.

```bash
./target/release/dpa select [options] <input> <columns> [output]
```

**Arguments:**
- `input` - Input file path
- `columns` - Comma-separated list of columns
- `output` - Output file path (optional)

**Options:**
- `--format <format>` - Output format (csv, parquet, json)

**Examples:**
```bash
# Select specific columns
./target/release/dpa select data.csv "name,age,salary" selected.csv

# Select all columns except some
./target/release/dpa select data.csv "!id,!timestamp" selected.csv

# Output to different format
./target/release/dpa select data.csv "name,age" selected.parquet --format parquet
```

### `convert` - Format Conversion

Convert between different file formats.

```bash
./target/release/dpa convert <input> <output>
```

**Arguments:**
- `input` - Input file path
- `output` - Output file path

**Examples:**
```bash
# CSV to Parquet
./target/release/dpa convert data.csv data.parquet

# Parquet to CSV
./target/release/dpa convert data.parquet data.csv

# CSV to JSON
./target/release/dpa convert data.csv data.json

# JSON to Parquet
./target/release/dpa convert data.json data.parquet
```

### `agg` - Aggregations

Perform groupby aggregations on data.

```bash
./target/release/dpa agg [options] <input> <group_by> <aggregations> [output]
```

**Arguments:**
- `input` - Input file path
- `group_by` - Column(s) to group by
- `aggregations` - Aggregation expressions
- `output` - Output file path (optional)

**Options:**
- `--format <format>` - Output format (csv, parquet, json)

**Examples:**
```bash
# Simple aggregation
./target/release/dpa agg data.csv "category" "count(), avg(salary), sum(revenue)" agg.csv

# Multiple group columns
./target/release/dpa agg data.csv "category,region" "count(), avg(age)" agg.csv

# Complex aggregations
./target/release/dpa agg data.csv "department" "count() as emp_count, avg(salary) as avg_salary, max(age) as max_age" agg.csv
```

### `join` - Data Joins

Join multiple datasets.

```bash
./target/release/dpa join [options] <left> <right> <on> [output]
```

**Arguments:**
- `left` - Left dataset file path
- `right` - Right dataset file path
- `on` - Join condition
- `output` - Output file path (optional)

**Options:**
- `--how <type>` - Join type (inner, left, right, outer)
- `--format <format>` - Output format (csv, parquet, json)

**Examples:**
```bash
# Inner join
./target/release/dpa join users.csv orders.csv "users.id = orders.user_id" joined.csv

# Left join
./target/release/dpa join users.csv orders.csv "users.id = orders.user_id" --how left joined.csv

# Multiple join conditions
./target/release/dpa join data1.csv data2.csv "data1.id = data2.id AND data1.date = data2.date" joined.csv
```

## Command Aliases

For convenience, DPA provides short aliases for common commands:

| Full Command | Alias | Description |
|--------------|-------|-------------|
| `filter` | `f` | Filter data |
| `select` | `s` | Select columns |
| `convert` | `c` | Convert formats |
| `profile` | `p` | Profile data |
| `validate` | `v` | Validate data |
| `agg` | `a` | Aggregations |
| `join` | `j` | Join datasets |

**Examples:**
```bash
# Using aliases
./target/release/dpa f data.csv "age > 30" filtered.csv
./target/release/dpa s data.csv "name,age" selected.csv
./target/release/dpa p data.csv
./target/release/dpa v data.csv
```

## Error Handling

### Common Error Messages

**File Not Found:**
```
Error: File 'data.csv' not found
```

**Invalid Expression:**
```
Error: Invalid filter expression 'age >'
```

**Schema Mismatch:**
```
Error: Schema validation failed for column 'age'
```

**Memory Error:**
```
Error: Insufficient memory for operation
```

### Debugging

Use the `--verbose` flag for detailed error information:

```bash
./target/release/dpa profile data.csv --verbose
```

## Performance Tips

### For Large Datasets

```bash
# Use sampling for profiling
./target/release/dpa profile large_data.csv --sample 10000

# Use Parquet format for better performance
./target/release/dpa convert large_data.csv large_data.parquet
./target/release/dpa profile large_data.parquet

# Use chunked processing
export DPA_CHUNK_SIZE=50000
./target/release/dpa profile large_data.csv
```

### Memory Optimization

```bash
# Reduce memory usage
export DPA_MAX_MEMORY=4GB
./target/release/dpa profile data.csv

# Use streaming for very large files
export DPA_USE_STREAMING=true
./target/release/dpa convert large_data.csv large_data.parquet
```

## Configuration

Commands can be configured using:

- **Environment variables**: `export DPA_LOG_LEVEL=debug`
- **Configuration file**: `--config config.toml`
- **Command-line options**: `--log-level debug`

See the [Configuration Guide](../getting-started/configuration.md) for details.

## Next Steps

- 📖 **Python API**: Learn about the [Python API Reference](python-api.md)
- 🎯 **Examples**: See practical examples in the [Examples](../examples/) section
- 🔧 **Configuration**: Understand [Configuration Options](configuration.md)
- 🚀 **Advanced Usage**: Explore [Best Practices](../user-guide/best-practices.md)

---

**Ready to use the CLI?** Start with the [Quick Start Guide](../getting-started/quick-start.md) to get familiar with the commands.
