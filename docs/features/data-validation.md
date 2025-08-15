# Data Validation

DPA provides comprehensive data validation capabilities to ensure data quality, schema compliance, and business rule enforcement. The validation system can detect issues ranging from simple data type mismatches to complex business logic violations.

## Overview

The data validation feature includes:

- **Schema Validation**: Verify column types and structure
- **Data Type Validation**: Detect mixed data types and type inconsistencies
- **Range Validation**: Check numeric ranges and detect outliers
- **Custom Rules**: User-defined validation rules using SQL expressions
- **Quality Reporting**: Detailed reports with error and warning counts

## Command Line Usage

### Basic Validation

```bash
# Basic validation (automatic checks)
dpa validate data/transactions.csv

# Validation with schema file
dpa validate data/transactions.csv --schema schema.json

# Validation with custom rules
dpa validate data/transactions.csv --rules validation_rules.json

# Complete validation with output
dpa validate data/transactions.csv --schema schema.json --rules rules.json -o invalid_rows.csv
```

### Options

| Option | Description | Required |
|--------|-------------|----------|
| `--schema` | JSON file with expected column types | No |
| `--rules` | JSON file with custom validation rules | No |
| `--output, -o` | Output file for invalid rows | No |

## Python API

```python
import dpa_core

# Basic validation
dpa_core.validate_py("data/transactions.csv")

# Validation with schema and rules
dpa_core.validate_py("data/transactions.csv", "schema.json", "rules.json")
```

## Schema Validation

### Schema File Format

Create a JSON file defining expected column types:

```json
{
  "user_id": "Int64",
  "amount": "Float64",
  "country": "Utf8",
  "timestamp": "Int64",
  "channel": "Utf8"
}
```

### Usage

```bash
# Validate against schema
dpa validate data/transactions.csv --schema expected_schema.json
```

## Custom Validation Rules

### Rules File Format

Create a JSON file with custom validation rules:

```json
[
  {
    "name": "positive_amounts",
    "column": "amount",
    "rule_type": "sql",
    "expression": "amount <= 0",
    "message": "Amount must be positive",
    "severity": "error"
  },
  {
    "name": "valid_countries",
    "column": "country",
    "rule_type": "sql",
    "expression": "country NOT IN ('US', 'IT', 'DE', 'ES', 'NL', 'GB', 'FR')",
    "message": "Invalid country code",
    "severity": "error"
  },
  {
    "name": "amount_range",
    "column": "amount",
    "rule_type": "range",
    "expression": "0.01,1000.0",
    "message": "Amount must be between 0.01 and 1000.0",
    "severity": "warning"
  }
]
```

### Rule Types

#### 1. SQL Rules

Use SQL expressions to validate data:

```json
{
  "name": "future_timestamps",
  "column": "timestamp",
  "rule_type": "sql",
  "expression": "timestamp > 1750000000",
  "message": "Timestamp is in the future",
  "severity": "error"
}
```

#### 2. Range Rules

Validate numeric ranges:

```json
{
  "name": "age_range",
  "column": "age",
  "rule_type": "range",
  "expression": "0,120",
  "message": "Age must be between 0 and 120",
  "severity": "error"
}
```

## Output Format

### Validation Report

```
🔍 Data Validation Report
============================================================
❌ Errors (2):
   • amount: 5 negative values found in column that should be positive (5 invalid values)
   • country: Invalid country code (3 invalid values)

⚠️  Warnings (1):
   • amount: 12 outliers detected (beyond 3σ from mean) (12 affected values)

📊 Summary: 2 errors, 1 warnings
```

### Success Report

```
✅ All validations passed!
```

## Automatic Validations

DPA automatically performs these validations:

### 1. Data Type Detection

- **Mixed Types**: Detects when string columns contain mostly numeric or date values
- **Type Suggestions**: Recommends appropriate data types

### 2. Range Validation

- **Outlier Detection**: Identifies statistical outliers (beyond 3σ)
- **Negative Values**: Checks for negative values in columns that should be positive
- **Domain Validation**: Validates against common business rules

### 3. Data Quality Checks

- **Null Analysis**: Reports null percentages and patterns
- **Unique Value Analysis**: Identifies potential issues with cardinality
- **Value Distribution**: Analyzes value distributions for anomalies

## Use Cases

### 1. Data Quality Assurance

```bash
# Validate incoming data
dpa validate new_data.csv --schema production_schema.json --rules business_rules.json
```

### 2. ETL Pipeline Validation

```bash
# Validate transformed data
dpa validate cleaned_data.csv --rules transformation_rules.json -o validation_errors.csv
```

### 3. Schema Migration

```bash
# Validate data against new schema
dpa validate legacy_data.csv --schema new_schema.json
```

### 4. Data Monitoring

```bash
# Daily data quality check
dpa validate daily_export.csv --rules monitoring_rules.json
```

## Best Practices

### 1. Schema Design

```json
{
  "user_id": "Int64",
  "email": "Utf8",
  "created_at": "Int64",
  "status": "Utf8",
  "score": "Float64"
}
```

### 2. Rule Design

```json
[
  {
    "name": "email_format",
    "column": "email",
    "rule_type": "sql",
    "expression": "email NOT LIKE '%@%.%'",
    "message": "Invalid email format",
    "severity": "error"
  },
  {
    "name": "positive_scores",
    "column": "score",
    "rule_type": "range",
    "expression": "0.0,100.0",
    "message": "Score must be between 0 and 100",
    "severity": "error"
  }
]
```

### 3. Severity Levels

- **Error**: Critical issues that must be fixed
- **Warning**: Issues that should be investigated

### 4. Performance Optimization

```bash
# Use sampling for large files
dpa profile large_file.csv --sample 100000
dpa validate large_file.csv --rules rules.json
```

## Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/validate.yml
name: Data Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Data
        run: |
          dpa validate data/production.csv --schema schema.json --rules rules.json
```

### Automated Monitoring

```python
import dpa_core
import smtplib
from email.mime.text import MIMEText

def validate_and_alert():
    try:
        dpa_core.validate_py("daily_data.csv", "schema.json", "rules.json")
        print("Validation passed")
    except Exception as e:
        # Send alert
        send_alert("Data validation failed", str(e))

def send_alert(subject, message):
    # Email alert implementation
    pass
```

### Jupyter Notebooks

```python
import dpa_core
import pandas as pd

# Validate data in notebook
try:
    dpa_core.validate_py("data.csv", "schema.json", "rules.json")
    print("✅ Data validation passed")
except Exception as e:
    print(f"❌ Validation failed: {e}")
    
    # Load and analyze invalid data
    invalid_df = pd.read_csv("invalid_rows.csv")
    print(f"Found {len(invalid_df)} invalid rows")
```

## Troubleshooting

### Common Issues

1. **Schema Mismatch**
   ```bash
   # Check actual schema first
   dpa schema data.csv
   ```

2. **Rule Syntax Errors**
   ```bash
   # Validate JSON syntax
   python -m json.tool rules.json
   ```

3. **Performance Issues**
   ```bash
   # Use sampling for large files
   dpa validate large_file.csv --sample 100000
   ```

### Error Messages

- `"Column not found"`: Check column names in schema
- `"Invalid SQL expression"`: Verify SQL syntax in rules
- `"File not found"`: Check file paths and permissions

## Advanced Features

### Custom Validation Functions

```python
import dpa_core
import json

def custom_validation(file_path, custom_rules):
    """Custom validation with additional logic"""
    
    # Add custom rules
    rules = [
        {
            "name": "custom_check",
            "column": "amount",
            "rule_type": "sql",
            "expression": "amount > 1000",
            "message": "Amount exceeds threshold",
            "severity": "warning"
        }
    ]
    
    # Write rules to temporary file
    with open("temp_rules.json", "w") as f:
        json.dump(rules, f)
    
    try:
        dpa_core.validate_py(file_path, rules_file="temp_rules.json")
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False
```

### Batch Validation

```bash
#!/bin/bash
# Validate multiple files
for file in data/*.csv; do
    echo "Validating $file..."
    dpa validate "$file" --schema schema.json --rules rules.json -o "validation_results/$(basename "$file" .csv)_errors.csv"
done
```

This comprehensive validation system ensures data quality and consistency across your data processing workflows.

