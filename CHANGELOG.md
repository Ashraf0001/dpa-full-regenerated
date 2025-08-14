# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release with Rust backend and Python bindings
- CLI interface for data processing operations
- Python API for programmatic data processing
- Support for CSV, Parquet, and JSON file formats
- Data filtering with SQL-like expressions
- Column selection functionality
- Data profiling and statistics
- Format conversion between supported formats
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions

### Changed
- Updated to Polars v0.43 for improved performance
- Updated to PyO3 v0.22 for better Python integration
- Optimized memory usage with lazy evaluation

### Fixed
- Fixed Polars API compatibility issues
- Fixed PyO3 module binding issues
- Fixed parquet writer API compatibility
- Fixed join type compatibility issues

## [0.2.1] - 2024-08-14

### Added
- Initial beta release
- Core data processing functionality
- Rust CLI and Python API
- Basic file format support (CSV, Parquet)
- SQL-like filtering expressions
- Column selection and data profiling

### Technical Details
- Built with Rust 1.70+ and Python 3.8+
- Uses Polars for high-performance data processing
- PyO3 bindings for Python integration
- Cross-platform wheel distribution
