#!/bin/bash

# Build and Publish Script for DPA
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 DPA Build and Publish Script${NC}"

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo -e "${RED}Error: Cargo.toml not found. Please run this script from the project root.${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command_exists maturin; then
    echo -e "${RED}Error: maturin not found. Please install it with: pip install maturin${NC}"
    exit 1
fi

if ! command_exists cargo; then
    echo -e "${RED}Error: cargo not found. Please install Rust.${NC}"
    exit 1
fi

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
cargo clean
rm -rf target/wheels/
rm -rf dist/
rm -rf build/

    # Build Rust binary (debug mode for tests)
    echo -e "${YELLOW}Building Rust binary...${NC}"
    cargo build --bin dpa
    
    # Run tests
    echo -e "${YELLOW}Running tests...${NC}"
    cargo test
    python3 -m pytest tests/ -v
    
    # Build wheels
    echo -e "${YELLOW}Building Python wheels...${NC}"
    maturin build --release --out target/wheels

# List built wheels
echo -e "${GREEN}✅ Built wheels:${NC}"
ls -la target/wheels/

echo -e "${GREEN}🎉 Build completed successfully!${NC}"
echo -e "${YELLOW}To publish to TestPyPI:${NC}"
echo "  python3 -m twine upload --repository testpypi target/wheels/*"
echo -e "${YELLOW}To publish to PyPI:${NC}"
echo "  python3 -m twine upload target/wheels/*"
echo -e "${YELLOW}To install from TestPyPI:${NC}"
echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dpa-cli"
echo -e "${YELLOW}To install with uv from TestPyPI:${NC}"
echo "  uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dpa-cli"
