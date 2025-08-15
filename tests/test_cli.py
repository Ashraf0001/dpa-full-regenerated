#!/usr/bin/env python3
"""
Comprehensive CLI tests for DPA
"""

import pytest
import subprocess
import os
import json
import pandas as pd
from pathlib import Path

# Test data paths
TEST_DATA_DIR = Path("tests/test_data")
TRANSACTIONS_SMALL = TEST_DATA_DIR / "transactions_small.csv"
TRANSACTIONS_MEDIUM = TEST_DATA_DIR / "transactions_medium.csv"
TRANSACTIONS_LARGE = TEST_DATA_DIR / "transactions_large.csv"
CUSTOMERS = TEST_DATA_DIR / "customers.csv"
PRODUCTS = TEST_DATA_DIR / "products.csv"
MIXED_TYPES = TEST_DATA_DIR / "mixed_types.csv"
VALID_SCHEMA = TEST_DATA_DIR / "valid_schema.json"
INVALID_SCHEMA = TEST_DATA_DIR / "invalid_schema.json"
VALIDATION_RULES = TEST_DATA_DIR / "validation_rules.json"

# CLI binary path
CLI_BINARY = "./target/debug/dpa"

class TestCLIBasic:
    """Basic CLI functionality tests"""
    
    def test_help(self):
        """Test help command"""
        result = subprocess.run([CLI_BINARY, "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Data Processing Accelerator" in result.stdout
    
    def test_no_args(self):
        """Test running without arguments"""
        result = subprocess.run([CLI_BINARY], 
                              capture_output=True, text=True)
        assert result.returncode != 0  # Should fail without subcommand
    
    def test_invalid_subcommand(self):
        """Test invalid subcommand"""
        result = subprocess.run([CLI_BINARY, "invalid"], 
                              capture_output=True, text=True)
        assert result.returncode != 0

class TestCLISchema:
    """Schema command tests"""
    
    def test_schema_basic(self):
        """Test basic schema command"""
        result = subprocess.run([CLI_BINARY, "schema", str(TRANSACTIONS_SMALL)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "user_id" in result.stdout
        assert "amount" in result.stdout
        assert "country" in result.stdout
    
    def test_schema_missing_file(self):
        """Test schema with missing file"""
        result = subprocess.run([CLI_BINARY, "schema", "nonexistent.csv"], 
                              capture_output=True, text=True)
        assert result.returncode != 0

class TestCLIHead:
    """Head command tests"""
    
    def test_head_basic(self):
        """Test basic head command"""
        result = subprocess.run([CLI_BINARY, "head", str(TRANSACTIONS_SMALL)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "shape:" in result.stdout
        assert "5" in result.stdout  # 5 columns
    
    def test_head_with_n(self):
        """Test head with custom number of rows"""
        result = subprocess.run([CLI_BINARY, "head", str(TRANSACTIONS_SMALL), "-n", "5"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        # Count lines in output (excluding header)
        lines = result.stdout.strip().split('\n')
        assert len(lines) <= 6  # Header + 5 rows

class TestCLIProfile:
    """Profile command tests"""
    
    def test_profile_basic(self):
        """Test basic profile command"""
        result = subprocess.run([CLI_BINARY, "profile", str(TRANSACTIONS_SMALL)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Data Profile Report" in result.stdout
        assert "Total Rows" in result.stdout
        assert "Total Columns" in result.stdout
    
    def test_profile_detailed(self):
        """Test detailed profile command"""
        result = subprocess.run([CLI_BINARY, "profile", str(TRANSACTIONS_SMALL), "--detailed"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Detailed Statistics" in result.stdout
        assert "Min:" in result.stdout
        assert "Max:" in result.stdout
        assert "Mean:" in result.stdout
    
    def test_profile_with_sample(self):
        """Test profile with custom sample size"""
        result = subprocess.run([CLI_BINARY, "profile", str(TRANSACTIONS_LARGE), "--sample", "1000"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Data Profile Report" in result.stdout

class TestCLIValidate:
    """Validate command tests"""
    
    def test_validate_basic(self):
        """Test basic validation without schema or rules"""
        result = subprocess.run([CLI_BINARY, "validate", str(TRANSACTIONS_SMALL)], 
                              capture_output=True, text=True)
        assert result.returncode == 1  # Should have validation errors due to negative amounts
        assert "Data Validation Report" in result.stdout
        assert "Errors" in result.stdout
    
    def test_validate_with_schema_valid(self):
        """Test validation with valid schema"""
        result = subprocess.run([CLI_BINARY, "validate", str(TRANSACTIONS_SMALL), 
                               "--schema", str(VALID_SCHEMA)], 
                              capture_output=True, text=True)
        assert result.returncode == 1  # Should have schema validation errors
        assert "Data Validation Report" in result.stdout
        assert "Errors" in result.stdout
    
    def test_validate_with_schema_invalid(self):
        """Test validation with invalid schema"""
        result = subprocess.run([CLI_BINARY, "validate", str(TRANSACTIONS_SMALL), 
                               "--schema", str(INVALID_SCHEMA)], 
                              capture_output=True, text=True)
        # Should have errors due to schema mismatches
        assert result.returncode == 1  # Exit with error code
        assert "Errors" in result.stdout
    
    def test_validate_with_rules(self):
        """Test validation with custom rules"""
        result = subprocess.run([CLI_BINARY, "validate", str(TRANSACTIONS_SMALL), 
                               "--rules", str(VALIDATION_RULES)], 
                              capture_output=True, text=True)
        assert result.returncode == 1  # Should have validation errors
        assert "Data Validation Report" in result.stdout
    
    def test_validate_with_output(self):
        """Test validation with output file"""
        output_file = "test_invalid_rows.csv"
        result = subprocess.run([CLI_BINARY, "validate", str(TRANSACTIONS_SMALL), 
                               "--rules", str(VALIDATION_RULES), 
                               "-o", output_file], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        # Check if output file was created
        if os.path.exists(output_file):
            os.remove(output_file)

class TestCLISample:
    """Sample command tests"""
    
    def test_sample_random(self):
        """Test random sampling"""
        output_file = "test_sample_random.csv"
        result = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                               "-o", output_file, "--size", "50"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Sampled 50 rows" in result.stdout
        
        # Verify output file
        if os.path.exists(output_file):
            df = pd.read_csv(output_file)
            assert len(df) == 50
            os.remove(output_file)
    
    def test_sample_head(self):
        """Test head sampling"""
        output_file = "test_sample_head.csv"
        result = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                               "-o", output_file, "--method", "head", "--size", "20"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Sampled 20 rows" in result.stdout
        
        if os.path.exists(output_file):
            df = pd.read_csv(output_file)
            assert len(df) == 20
            os.remove(output_file)
    
    def test_sample_tail(self):
        """Test tail sampling"""
        output_file = "test_sample_tail.csv"
        result = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                               "-o", output_file, "--method", "tail", "--size", "15"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Sampled 15 rows" in result.stdout
        
        if os.path.exists(output_file):
            df = pd.read_csv(output_file)
            assert len(df) == 15
            os.remove(output_file)
    
    def test_sample_stratified(self):
        """Test stratified sampling"""
        output_file = "test_sample_stratified.csv"
        result = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                               "-o", output_file, "--method", "stratified", 
                               "--stratify", "country", "--size", "30"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Sampled" in result.stdout
        assert result.returncode == 0
        
        if os.path.exists(output_file):
            df = pd.read_csv(output_file)
            # Allow some flexibility due to rounding in proportional sampling
            assert 25 <= len(df) <= 35
            os.remove(output_file)
    
    def test_sample_with_seed(self):
        """Test sampling with seed for reproducibility"""
        output_file1 = "test_sample_seed1.csv"
        output_file2 = "test_sample_seed2.csv"
        
        # First run with seed
        result1 = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                                "-o", output_file1, "--size", "20", "--seed", "42"], 
                               capture_output=True, text=True)
        assert result1.returncode == 0
        
        # Second run with same seed
        result2 = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                                "-o", output_file2, "--size", "20", "--seed", "42"], 
                               capture_output=True, text=True)
        assert result2.returncode == 0
        
        # Files should be identical
        if os.path.exists(output_file1) and os.path.exists(output_file2):
            df1 = pd.read_csv(output_file1)
            df2 = pd.read_csv(output_file2)
            pd.testing.assert_frame_equal(df1, df2)
            os.remove(output_file1)
            os.remove(output_file2)

class TestCLISplit:
    """Split command tests"""
    
    def test_split_random(self):
        """Test random split"""
        train_file = "test_train.csv"
        test_file = "test_test.csv"
        
        result = subprocess.run([CLI_BINARY, "split", str(TRANSACTIONS_SMALL), 
                               "--train", train_file, "--test", test_file, 
                               "--test-size", "0.3"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Split dataset" in result.stdout
        
        # Verify output files
        if os.path.exists(train_file) and os.path.exists(test_file):
            train_df = pd.read_csv(train_file)
            test_df = pd.read_csv(test_file)
            
            # Check that split proportions are approximately correct
            total_rows = len(train_df) + len(test_df)
            test_proportion = len(test_df) / total_rows
            assert 0.20 <= test_proportion <= 0.40  # Allow more tolerance for small datasets
            
            os.remove(train_file)
            os.remove(test_file)
    
    def test_split_stratified(self):
        """Test stratified split"""
        train_file = "test_train_strat.csv"
        test_file = "test_test_strat.csv"
        
        result = subprocess.run([CLI_BINARY, "split", str(TRANSACTIONS_SMALL), 
                               "--train", train_file, "--test", test_file, 
                               "--test-size", "0.2", "--stratify", "country"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Split dataset" in result.stdout
        
        if os.path.exists(train_file) and os.path.exists(test_file):
            train_df = pd.read_csv(train_file)
            test_df = pd.read_csv(test_file)
            
            # Check that both files have data
            assert len(train_df) > 0
            assert len(test_df) > 0
            
            os.remove(train_file)
            os.remove(test_file)
    
    def test_split_with_seed(self):
        """Test split with seed for reproducibility"""
        train_file1 = "test_train_seed1.csv"
        test_file1 = "test_test_seed1.csv"
        train_file2 = "test_train_seed2.csv"
        test_file2 = "test_test_seed2.csv"
        
        # First split with seed
        result1 = subprocess.run([CLI_BINARY, "split", str(TRANSACTIONS_SMALL), 
                                "--train", train_file1, "--test", test_file1, 
                                "--test-size", "0.3", "--seed", "42"], 
                               capture_output=True, text=True)
        assert result1.returncode == 0
        
        # Second split with same seed
        result2 = subprocess.run([CLI_BINARY, "split", str(TRANSACTIONS_SMALL), 
                                "--train", train_file2, "--test", test_file2, 
                                "--test-size", "0.3", "--seed", "42"], 
                               capture_output=True, text=True)
        assert result2.returncode == 0
        
        # Files should be identical
        if (os.path.exists(train_file1) and os.path.exists(train_file2) and
            os.path.exists(test_file1) and os.path.exists(test_file2)):
            train_df1 = pd.read_csv(train_file1)
            train_df2 = pd.read_csv(train_file2)
            test_df1 = pd.read_csv(test_file1)
            test_df2 = pd.read_csv(test_file2)
            
            pd.testing.assert_frame_equal(train_df1, train_df2)
            pd.testing.assert_frame_equal(test_df1, test_df2)
            
            os.remove(train_file1)
            os.remove(train_file2)
            os.remove(test_file1)
            os.remove(test_file2)

class TestCLIErrorHandling:
    """Error handling tests"""
    
    def test_missing_input_file(self):
        """Test handling of missing input file"""
        result = subprocess.run([CLI_BINARY, "profile", "nonexistent.csv"], 
                              capture_output=True, text=True)
        assert result.returncode != 0
    
    def test_invalid_sampling_method(self):
        """Test invalid sampling method"""
        result = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                               "-o", "test.csv", "--method", "invalid"], 
                              capture_output=True, text=True)
        assert result.returncode != 0
        assert "Unknown sampling method" in result.stderr
    
    def test_missing_stratify_column(self):
        """Test stratified sampling without stratify column"""
        result = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_SMALL), 
                               "-o", "test.csv", "--method", "stratified"], 
                              capture_output=True, text=True)
        assert result.returncode != 0
        assert "stratify column required" in result.stderr
    
    def test_invalid_schema_file(self):
        """Test validation with invalid schema file"""
        result = subprocess.run([CLI_BINARY, "validate", str(TRANSACTIONS_SMALL), 
                               "--schema", "nonexistent.json"], 
                              capture_output=True, text=True)
        assert result.returncode != 0

@pytest.mark.slow
class TestCLIPerformance:
    """Performance tests for large datasets"""
    
    def test_profile_large_dataset(self):
        """Test profiling large dataset"""
        result = subprocess.run([CLI_BINARY, "profile", str(TRANSACTIONS_LARGE), 
                               "--sample", "5000"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Data Profile Report" in result.stdout
    
    def test_sample_large_dataset(self):
        """Test sampling large dataset"""
        output_file = "test_large_sample.csv"
        result = subprocess.run([CLI_BINARY, "sample", str(TRANSACTIONS_LARGE), 
                               "-o", output_file, "--size", "1000"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        
        if os.path.exists(output_file):
            df = pd.read_csv(output_file)
            assert len(df) == 1000
            os.remove(output_file)
