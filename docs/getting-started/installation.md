# Installation Guide

This guide covers all installation methods for Data Processing Accelerator (DPA).

## System Requirements

### Minimum Requirements

- **Operating System**: Linux, macOS, or Windows
- **Rust**: 1.70 or later
- **Python**: 3.8 or later
- **Memory**: 4GB RAM (8GB recommended for large datasets)
- **Storage**: 2GB free space

### Recommended Requirements

- **CPU**: Multi-core processor (4+ cores)
- **Memory**: 16GB RAM or more
- **Storage**: SSD with 10GB+ free space
- **Network**: Internet connection for package downloads

## Installation Methods

### Method 1: From Source (Recommended)

#### Step 1: Install Prerequisites

**Install Rust:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
rustup default stable
```

**Install Python:**
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# On macOS with Homebrew
brew install python3

# On Windows
# Download from https://python.org
```

#### Step 2: Clone and Build

```bash
# Clone the repository
git clone https://github.com/Ashraf0001/data-processing-accelerator-dpa
cd data-processing-accelerator-dpa

# Build the Rust binary
cargo build --release

# Install Python dependencies
pip install maturin

# Build and install Python bindings
maturin develop

# Install Python CLI
cd python
pip install .
```

#### Step 3: Verify Installation

```bash
# Test CLI
./target/release/dpa --help

# Test Python API
python -c "import dpa_core; print('DPA installed successfully!')"
```

### Method 2: Using pip (Python Only)

```bash
# Install from PyPI (when available)
pip install dpa

# Or install from GitHub
pip install git+https://github.com/Ashraf0001/data-processing-accelerator-dpa.git
```

### Method 3: Using Cargo (Rust Only)

```bash
# Install from crates.io (when available)
cargo install dpa

# Or install from GitHub
cargo install --git https://github.com/Ashraf0001/data-processing-accelerator-dpa.git
```

## Platform-Specific Instructions

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt update
sudo apt install build-essential pkg-config libssl-dev

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install Python
sudo apt install python3 python3-pip python3-venv

# Follow the source installation steps above
```

### macOS

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install rust python3

# Follow the source installation steps above
```

### Windows

1. **Install Rust:**
   - Download rustup-init.exe from https://rustup.rs
   - Run the installer and follow the prompts

2. **Install Python:**
   - Download from https://python.org
   - Ensure "Add Python to PATH" is checked

3. **Install Visual Studio Build Tools:**
   - Download from Microsoft Visual Studio
   - Install C++ build tools

4. **Follow the source installation steps above**

## Virtual Environment Setup

```bash
# Create virtual environment
python3 -m venv dpa-env

# Activate virtual environment
# On Linux/macOS:
source dpa-env/bin/activate

# On Windows:
dpa-env\Scripts\activate

# Install DPA in virtual environment
pip install maturin
maturin develop
```

## Configuration

### Environment Variables

```bash
# Set DPA configuration
export DPA_CONFIG_PATH=/path/to/config
export DPA_LOG_LEVEL=info
export DPA_CACHE_DIR=/path/to/cache
```

### Configuration File

Create `~/.dpa/config.toml`:

```toml
[general]
log_level = "info"
cache_dir = "~/.dpa/cache"
max_memory = "8GB"

[profiling]
sample_size = 10000
detailed_stats = true

[validation]
strict_mode = false
max_errors = 1000
```

## Troubleshooting

### Common Issues

**1. Rust Build Errors**
```bash
# Update Rust
rustup update

# Clean and rebuild
cargo clean
cargo build --release
```

**2. Python Import Errors**
```bash
# Reinstall Python bindings
maturin develop --force-reinstall

# Check Python version
python --version
```

**3. Memory Issues**
```bash
# Increase system memory or reduce dataset size
export DPA_MAX_MEMORY=4GB
```

**4. Permission Errors**
```bash
# Fix permissions
chmod +x target/release/dpa
```

### Getting Help

- 📖 **Documentation**: Check this documentation
- 🐛 **GitHub Issues**: Report bugs on GitHub
- 💬 **Discussions**: Join community discussions
- 📧 **Email**: Contact support team

## Next Steps

After installation:

1. 🚀 Try the [Quick Start Guide](quick-start.md)
2. 📖 Read the [User Guide](../user-guide/)
3. 🎯 Explore [Examples](../examples/)
4. 🔧 Learn about [Configuration](configuration.md)

---

**Installation complete! Ready to accelerate your data processing.** ⚡
