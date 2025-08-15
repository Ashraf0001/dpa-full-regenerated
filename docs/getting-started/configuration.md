# Configuration Guide

Learn how to configure DPA for optimal performance and customization.

## Configuration Overview

DPA can be configured through multiple methods:

- **Environment Variables**: Quick settings for current session
- **Configuration Files**: Persistent settings across sessions
- **Command-line Options**: Override settings for specific commands
- **Python API Parameters**: Programmatic configuration

## Environment Variables

### Core Configuration

```bash
# Set configuration file path
export DPA_CONFIG_PATH=/path/to/config.toml

# Set log level (debug, info, warn, error)
export DPA_LOG_LEVEL=info

# Set cache directory
export DPA_CACHE_DIR=~/.dpa/cache

# Set maximum memory usage
export DPA_MAX_MEMORY=8GB

# Set number of threads for parallel processing
export DPA_NUM_THREADS=4
```

### Performance Settings

```bash
# Enable/disable parallel processing
export DPA_PARALLEL=true

# Set chunk size for large file processing
export DPA_CHUNK_SIZE=10000

# Set buffer size for I/O operations
export DPA_BUFFER_SIZE=8192

# Enable/disable memory mapping
export DPA_USE_MMAP=true
```

### File Format Settings

```bash
# Default CSV delimiter
export DPA_CSV_DELIMITER=,

# Default CSV quote character
export DPA_CSV_QUOTE="

# Parquet compression level
export DPA_PARQUET_COMPRESSION=snappy

# JSON pretty print
export DPA_JSON_PRETTY=true
```

## Configuration Files

### Main Configuration File

Create `~/.dpa/config.toml`:

```toml
[general]
# General settings
log_level = "info"
cache_dir = "~/.dpa/cache"
max_memory = "8GB"
num_threads = 4
parallel = true

[profiling]
# Profiling settings
sample_size = 10000
detailed_stats = true
include_memory_usage = true
include_null_percentage = true
include_unique_counts = true
include_value_distributions = true

[validation]
# Validation settings
strict_mode = false
max_errors = 1000
continue_on_error = true
output_invalid_rows = false

[sampling]
# Sampling settings
default_method = "random"
default_size = 1000
stratified_min_group_size = 10
random_seed = null

[file_formats]
# File format settings
csv_delimiter = ","
csv_quote = "\""
csv_escape = "\\"
parquet_compression = "snappy"
json_pretty = true

[performance]
# Performance settings
chunk_size = 10000
buffer_size = 8192
use_mmap = true
lazy_evaluation = true

[output]
# Output settings
default_format = "csv"
include_header = true
float_precision = 6
date_format = "%Y-%m-%d"
datetime_format = "%Y-%m-%d %H:%M:%S"
```

### Project-Specific Configuration

Create `dpa.toml` in your project directory:

```toml
[project]
name = "my-data-project"
version = "1.0.0"

[data_sources]
raw_data = "data/raw/"
processed_data = "data/processed/"
output_data = "data/output/"

[profiling]
# Override global settings for this project
sample_size = 50000
detailed_stats = false

[validation]
# Project-specific validation rules
schema_file = "schemas/data_schema.json"
rules_file = "rules/validation_rules.json"

[sampling]
# Project-specific sampling settings
stratify_columns = ["category", "region"]
test_size = 0.2
```

## Command-Line Configuration

### Global Options

```bash
# Set configuration file
./target/release/dpa --config /path/to/config.toml profile data.csv

# Override log level
./target/release/dpa --log-level debug profile data.csv

# Set output format
./target/release/dpa --output-format parquet profile data.csv

# Set number of threads
./target/release/dpa --threads 8 profile data.csv
```

### Command-Specific Options

```bash
# Profiling with custom settings
./target/release/dpa profile data.csv \
  --sample-size 50000 \
  --detailed \
  --include-memory

# Validation with custom settings
./target/release/dpa validate data.csv \
  --schema schema.json \
  --rules rules.json \
  --max-errors 100 \
  --output-invalid

# Sampling with custom settings
./target/release/dpa sample data.csv output.csv \
  --method stratified \
  --size 1000 \
  --stratify category \
  --seed 42
```

## Python API Configuration

### Global Configuration

```python
import dpa_core
import os

# Set environment variables
os.environ['DPA_LOG_LEVEL'] = 'debug'
os.environ['DPA_MAX_MEMORY'] = '4GB'

# Configure through Python
dpa_core.set_config({
    'log_level': 'info',
    'max_memory': '4GB',
    'num_threads': 4
})
```

### Function-Specific Configuration

```python
import dpa_core

# Profile with custom settings
stats = dpa_core.profile_py(
    "data.csv",
    sample_size=50000,
    detailed=True,
    include_memory=True
)

# Sample with custom settings
dpa_core.sample_py(
    "data.csv",
    "output.csv",
    size=1000,
    method="stratified",
    stratify="category",
    seed=42
)

# Validate with custom settings
dpa_core.validate_py(
    "data.csv",
    schema="schema.json",
    rules="rules.json"
)
```

## Advanced Configuration

### Memory Management

```toml
[memory]
# Memory management settings
max_memory = "8GB"
memory_fraction = 0.8
spill_to_disk = true
spill_directory = "/tmp/dpa_spill"
cleanup_on_exit = true
```

### Caching Configuration

```toml
[cache]
# Caching settings
enabled = true
cache_dir = "~/.dpa/cache"
max_cache_size = "2GB"
cache_ttl = 3600  # seconds
cleanup_interval = 86400  # seconds
```

### Logging Configuration

```toml
[logging]
# Logging settings
level = "info"
format = "{time} {level} {message}"
file = "~/.dpa/logs/dpa.log"
max_file_size = "10MB"
max_files = 5
```

### Performance Tuning

```toml
[performance]
# Performance tuning
chunk_size = 10000
buffer_size = 8192
use_mmap = true
lazy_evaluation = true
parallel_threshold = 10000
rayon_threads = 4
```

## Configuration Precedence

DPA follows this precedence order (highest to lowest):

1. **Command-line options** (highest priority)
2. **Function parameters** (Python API)
3. **Project configuration** (`dpa.toml`)
4. **User configuration** (`~/.dpa/config.toml`)
5. **Environment variables**
6. **Default values** (lowest priority)

## Configuration Validation

### Validate Configuration File

```bash
# Validate configuration syntax
./target/release/dpa config validate config.toml

# Check configuration
./target/release/dpa config check
```

### Python Configuration Validation

```python
import dpa_core

# Validate configuration
config = {
    'log_level': 'info',
    'max_memory': '8GB',
    'num_threads': 4
}

try:
    dpa_core.validate_config(config)
    print("✅ Configuration is valid")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

## Best Practices

### 1. Use Project-Specific Configurations

```bash
# Create project configuration
cat > dpa.toml << EOF
[project]
name = "my-project"

[profiling]
sample_size = 50000

[validation]
schema_file = "schemas/data_schema.json"
EOF
```

### 2. Environment-Specific Settings

```bash
# Development environment
export DPA_LOG_LEVEL=debug
export DPA_MAX_MEMORY=4GB

# Production environment
export DPA_LOG_LEVEL=warn
export DPA_MAX_MEMORY=16GB
```

### 3. Monitor Performance

```bash
# Enable performance monitoring
export DPA_PROFILE_PERFORMANCE=true
export DPA_PERFORMANCE_LOG=performance.log
```

### 4. Secure Configuration

```bash
# Use secure file permissions
chmod 600 ~/.dpa/config.toml

# Don't commit sensitive configuration
echo "~/.dpa/config.toml" >> .gitignore
```

## Troubleshooting

### Common Configuration Issues

**1. Configuration File Not Found**
```bash
# Check configuration path
echo $DPA_CONFIG_PATH
ls -la ~/.dpa/config.toml
```

**2. Invalid Configuration Syntax**
```bash
# Validate TOML syntax
./target/release/dpa config validate config.toml
```

**3. Memory Issues**
```bash
# Reduce memory usage
export DPA_MAX_MEMORY=4GB
export DPA_CHUNK_SIZE=5000
```

**4. Performance Issues**
```bash
# Optimize performance
export DPA_NUM_THREADS=8
export DPA_PARALLEL=true
export DPA_USE_MMAP=true
```

## Next Steps

- 🔧 **Customize Settings**: Adjust configuration for your needs
- 📊 **Monitor Performance**: Use performance settings to optimize
- 🛡️ **Security**: Implement secure configuration practices
- 📚 **Examples**: See configuration examples in the [Examples](../examples/) section

---

**Configuration complete! Your DPA setup is optimized and ready.** ⚙️
