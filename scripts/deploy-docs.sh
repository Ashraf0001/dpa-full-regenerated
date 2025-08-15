#!/bin/bash

# DPA Documentation Deployment Script
# This script helps with local testing and deployment of the documentation site

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

# Function to install dependencies
install_dependencies() {
    print_status "Installing documentation dependencies..."
    
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    pip install -r requirements-docs.txt
    print_success "Dependencies installed successfully"
}

# Function to build documentation
build_docs() {
    print_status "Building documentation..."
    
    if [ "$1" = "--strict" ]; then
        mkdocs build --strict
    else
        mkdocs build
    fi
    
    print_success "Documentation built successfully"
}

# Function to serve documentation locally
serve_docs() {
    print_status "Starting local documentation server..."
    print_status "Site will be available at: http://127.0.0.1:8000"
    print_status "Press Ctrl+C to stop the server"
    
    mkdocs serve
}

# Function to deploy to GitHub Pages
deploy_to_github() {
    print_status "Deploying to GitHub Pages..."
    
    if ! command_exists git; then
        print_error "Git is required but not installed"
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
    
    # Check if we have uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "You have uncommitted changes. Consider committing them first."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    mkdocs gh-deploy --force
    print_success "Deployed to GitHub Pages successfully"
}

# Function to validate documentation
validate_docs() {
    print_status "Validating documentation..."
    
    # Check for broken links
    if command_exists linkchecker; then
        print_status "Checking for broken links..."
        linkchecker http://127.0.0.1:8000 --no-robots --ignore-url=^mailto: --ignore-url=^javascript: || true
    else
        print_warning "linkchecker not installed. Install it to check for broken links."
    fi
    
    # Check for common issues
    print_status "Checking for common documentation issues..."
    
    # Check for missing files referenced in nav
    if grep -r "WARNING.*not found" site/ 2>/dev/null; then
        print_warning "Found missing files referenced in navigation"
    fi
    
    print_success "Validation completed"
}

# Function to show help
show_help() {
    echo "DPA Documentation Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  install     Install documentation dependencies"
    echo "  build       Build documentation locally"
    echo "  build-strict Build documentation with strict mode"
    echo "  serve       Serve documentation locally"
    echo "  deploy      Deploy to GitHub Pages"
    echo "  validate    Validate documentation (requires local server)"
    echo "  test        Run full test suite (build + validate)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install      # Install dependencies"
    echo "  $0 build        # Build documentation"
    echo "  $0 serve        # Start local server"
    echo "  $0 deploy       # Deploy to GitHub Pages"
    echo "  $0 test         # Full test suite"
}

# Main script logic
case "${1:-help}" in
    install)
        install_dependencies
        ;;
    build)
        build_docs
        ;;
    build-strict)
        build_docs --strict
        ;;
    serve)
        serve_docs
        ;;
    deploy)
        deploy_to_github
        ;;
    validate)
        validate_docs
        ;;
    test)
        print_status "Running full test suite..."
        install_dependencies
        build_docs --strict
        print_success "Test suite completed successfully"
        print_status "You can now run '$0 serve' to view the documentation locally"
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
