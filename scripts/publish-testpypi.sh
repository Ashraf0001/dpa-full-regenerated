#!/bin/bash

# DPA TestPyPI Publishing Script
# This script helps with local testing and publishing to TestPyPI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    if ! command_exists cargo; then
        print_error "Rust/Cargo is required but not installed"
        exit 1
    fi
    
    if ! command_exists maturin; then
        print_warning "maturin not found. Installing..."
        pip install maturin
    fi
    
    if ! command_exists twine; then
        print_warning "twine not found. Installing..."
        pip install twine
    fi
    
    print_success "Prerequisites check completed"
}

# Function to build Rust project
build_rust() {
    print_status "Building Rust project..."
    
    cargo build --release
    cargo test
    
    print_success "Rust build completed"
}

# Function to build Python packages
build_python() {
    print_status "Building Python packages..."
    
    # Build Rust wheel
    maturin build --release
    
    # Build Python CLI package
    cd python
    python -m build
    cd ..
    
    print_success "Python build completed"
}

# Function to test packages locally
test_packages() {
    print_status "Testing packages locally..."
    
    # Install the wheel
    pip install target/wheels/*.whl
    
    # Test basic functionality
    python3 -c "import dpa_core; print('✅ dpa_core imported successfully')"
    
    # Test CLI
    if command_exists dpa; then
        dpa --help
        print_success "CLI test completed"
    else
        print_warning "CLI not found in PATH"
    fi
    
    print_success "Local testing completed"
}

# Function to publish to TestPyPI
publish_to_testpypi() {
    print_status "Publishing to TestPyPI..."
    
    # Check for API token
    if [ -z "$TESTPYPI_API_TOKEN" ]; then
        print_error "TESTPYPI_API_TOKEN environment variable is required"
        print_status "Please set it with: export TESTPYPI_API_TOKEN=your_token_here"
        exit 1
    fi
    
    # Publish Rust wheel
    print_status "Publishing Rust wheel to TestPyPI..."
    twine upload --repository testpypi --verbose target/wheels/*.whl
    
    # Publish Python CLI package
    print_status "Publishing Python CLI to TestPyPI..."
    twine upload --repository testpypi --verbose python/dist/*.whl python/dist/*.tar.gz
    
    print_success "Published to TestPyPI successfully!"
}

# Function to show installation instructions
show_installation_instructions() {
    print_status "Installation instructions for TestPyPI release:"
    echo ""
    echo "📦 Install from TestPyPI:"
    echo "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dpa-cli"
    echo ""
    echo "🔗 TestPyPI Project Page:"
    echo "https://test.pypi.org/project/dpa-cli/"
    echo ""
    echo "🧪 Test the installation:"
    echo "dpa --help"
    echo "python3 -c \"import dpa_core; print('Success!')\""
}

# Function to show help
show_help() {
    echo "DPA TestPyPI Publishing Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  check       Check prerequisites"
    echo "  build       Build Rust and Python packages"
    echo "  test        Test packages locally"
    echo "  publish     Publish to TestPyPI"
    echo "  full        Run full pipeline (check + build + test + publish)"
    echo "  install     Show installation instructions"
    echo "  help        Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  TESTPYPI_API_TOKEN    Your TestPyPI API token"
    echo ""
    echo "Examples:"
    echo "  $0 check              # Check prerequisites"
    echo "  $0 build              # Build packages"
    echo "  $0 publish            # Publish to TestPyPI"
    echo "  $0 full               # Full pipeline"
}

# Main script logic
case "${1:-help}" in
    check)
        check_prerequisites
        ;;
    build)
        check_prerequisites
        build_rust
        build_python
        ;;
    test)
        test_packages
        ;;
    publish)
        publish_to_testpypi
        ;;
    full)
        check_prerequisites
        build_rust
        build_python
        test_packages
        publish_to_testpypi
        show_installation_instructions
        ;;
    install)
        show_installation_instructions
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
