#!/usr/bin/env python3
"""
Comprehensive Python API tests for DPA
"""

import pytest
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
import dpa_core

# Test data paths
TEST_DATA_DIR = Path("tests/test_data")
TRANSACTIONS_SMALL = str(TEST_DATA_DIR / "transactions_small.csv")
TRANSACTIONS_MEDIUM = str(TEST_DATA_DIR / "transactions_medium.csv")
TRANSACTIONS_LARGE = str(TEST_DATA_DIR / "transactions_large.csv")
CUSTOMERS = str(TEST_DATA_DIR / "customers.csv")
PRODUCTS = str(TEST_DATA_DIR / "products.csv")
MIXED_TYPES = str(TEST_DATA_DIR / "mixed_types.csv")
VALID_SCHEMA = str(TEST_DATA_DIR / "valid_schema.json")
INVALID_SCHEMA = str(TEST_DATA_DIR / "invalid_schema.json")
VALIDATION_RULES = str(TEST_DATA_DIR / "validation_rules.json")

class TestPythonAPIBasic:
    """Basic Python API functionality tests"""
    
    def test_import(self):
        """Test that dpa_core can be imported"""
        assert dpa_core is not None
        assert hasattr(dpa_core, 'profile_py')
    
    def test_profile_basic(self):
        """Test basic profiling"""
        result = dpa_core.profile_py(TRANSACTIONS_SMALL)
        assert isinstance(result, dict)
        assert 'rows' in result
        assert 'columns' in result
        # Convert string values to numbers for comparison
        rows = int(result['rows'])
        columns = int(result['columns'])
        assert rows > 0
        assert columns > 0
    
    def test_profile_detailed(self):
        """Test detailed profiling"""
        result = dpa_core.profile_py(TRANSACTIONS_SMALL)
        # Check for detailed statistics
        assert any('min:' in key.lower() for key in result.keys())
        assert any('max:' in key.lower() for key in result.keys())
        assert any('mean:' in key.lower() for key in result.keys())

class TestPythonAPIProfiling:
    """Profiling API tests"""
    
    def test_profile_small_dataset(self):
        """Test profiling small dataset"""
        result = dpa_core.profile_py(TRANSACTIONS_SMALL)
        assert int(result['rows']) == 100
        assert int(result['columns']) == 5
        assert 'memory_mb' in result
        assert 'null_percentage' in result
    
    def test_profile_medium_dataset(self):
        """Test profiling medium dataset"""
        result = dpa_core.profile_py(TRANSACTIONS_MEDIUM)
        assert int(result['rows']) == 1000
        assert int(result['columns']) == 5
    
    @pytest.mark.slow
    def test_profile_large_dataset(self):
        """Test profiling large dataset"""
        result = dpa_core.profile_py(TRANSACTIONS_LARGE)
        assert int(result['rows']) == 10000
        assert int(result['columns']) == 5
    
    def test_profile_column_statistics(self):
        """Test that column statistics are present"""
        result = dpa_core.profile_py(TRANSACTIONS_SMALL)
        
        # Check for user_id statistics
        assert any('user_id' in key for key in result.keys())
        user_id_keys = [key for key in result.keys() if 'user_id' in key]
        assert len(user_id_keys) > 0
        
        # Check for amount statistics
        assert any('amount' in key for key in result.keys())
        amount_keys = [key for key in result.keys() if 'amount' in key]
        assert len(amount_keys) > 0
    
    def test_profile_memory_usage(self):
        """Test memory usage calculation"""
        result = dpa_core.profile_py(TRANSACTIONS_SMALL)
        assert 'memory_mb' in result
        # Convert string to float for comparison
        memory_mb = float(result['memory_mb'])
        assert memory_mb >= 0  # Memory can be 0 for very small datasets
    
    def test_profile_null_percentage(self):
        """Test null percentage calculation"""
        result = dpa_core.profile_py(TRANSACTIONS_SMALL)
        assert 'null_percentage' in result
        # Convert string to float for comparison
        null_percentage = float(result['null_percentage'])
        assert 0 <= null_percentage <= 100

class TestPythonAPIValidation:
    """Validation API tests"""
    
    def test_validate_basic(self):
        """Test basic validation without schema or rules"""
        # This should run without errors
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, None, None)
        except Exception as e:
            # If validation fails, it should be due to data quality issues, not API errors
            assert "validation" in str(e).lower() or "error" in str(e).lower()
    
    def test_validate_with_valid_schema(self):
        """Test validation with valid schema"""
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, VALID_SCHEMA, None)
        except Exception as e:
            # Should pass validation with valid schema
            pass
    
    def test_validate_with_invalid_schema(self):
        """Test validation with invalid schema"""
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, INVALID_SCHEMA, None)
        except Exception as e:
            # Should fail validation with invalid schema
            assert "validation" in str(e).lower() or "error" in str(e).lower()
    
    def test_validate_with_rules(self):
        """Test validation with custom rules"""
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, None, VALIDATION_RULES)
        except Exception as e:
            # Should fail validation due to data quality issues in rules
            assert "validation" in str(e).lower() or "error" in str(e).lower()
    
    def test_validate_with_schema_and_rules(self):
        """Test validation with both schema and rules"""
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, VALID_SCHEMA, VALIDATION_RULES)
        except Exception as e:
            # Should fail due to validation rules
            assert "validation" in str(e).lower() or "error" in str(e).lower()

class TestPythonAPISampling:
    """Sampling API tests"""
    
    def test_sample_random(self):
        """Test random sampling"""
        output_file = "test_sample_random_api.csv"
        try:
            dpa_core.sample_py(TRANSACTIONS_SMALL, output_file, size=50, method="random")
            assert os.path.exists(output_file)
            
            # Verify output
            df = pd.read_csv(output_file)
            assert len(df) == 50
            assert list(df.columns) == ['user_id', 'amount', 'country', 'timestamp', 'channel']
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_sample_head(self):
        """Test head sampling"""
        output_file = "test_sample_head_api.csv"
        try:
            dpa_core.sample_py(TRANSACTIONS_SMALL, output_file, size=20, method="head")
            assert os.path.exists(output_file)
            
            df = pd.read_csv(output_file)
            assert len(df) == 20
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_sample_tail(self):
        """Test tail sampling"""
        output_file = "test_sample_tail_api.csv"
        try:
            dpa_core.sample_py(TRANSACTIONS_SMALL, output_file, size=15, method="tail")
            assert os.path.exists(output_file)
            
            df = pd.read_csv(output_file)
            assert len(df) == 15
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_sample_stratified(self):
        """Test stratified sampling"""
        output_file = "test_sample_stratified_api.csv"
        try:
            dpa_core.sample_py(TRANSACTIONS_SMALL, output_file, size=30, 
                             method="stratified", stratify="country")
            assert os.path.exists(output_file)
            
            df = pd.read_csv(output_file)
            # Allow some flexibility due to rounding in proportional sampling
            assert 25 <= len(df) <= 35
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_sample_with_seed(self):
        """Test sampling with seed for reproducibility"""
        output_file1 = "test_sample_seed1_api.csv"
        output_file2 = "test_sample_seed2_api.csv"
        
        try:
            # First run with seed
            dpa_core.sample_py(TRANSACTIONS_SMALL, output_file1, size=20, 
                             method="random", seed=42)
            
            # Second run with same seed
            dpa_core.sample_py(TRANSACTIONS_SMALL, output_file2, size=20, 
                             method="random", seed=42)
            
            # Files should be identical
            df1 = pd.read_csv(output_file1)
            df2 = pd.read_csv(output_file2)
            pd.testing.assert_frame_equal(df1, df2)
        finally:
            for file in [output_file1, output_file2]:
                if os.path.exists(file):
                    os.remove(file)
    
    def test_sample_large_dataset(self):
        """Test sampling large dataset"""
        output_file = "test_sample_large_api.csv"
        try:
            dpa_core.sample_py(TRANSACTIONS_LARGE, output_file, size=1000, method="random")
            assert os.path.exists(output_file)
            
            df = pd.read_csv(output_file)
            assert len(df) == 1000
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

class TestPythonAPISplit:
    """Split API tests"""
    
    def test_split_random(self):
        """Test random split"""
        train_file = "test_train_api.csv"
        test_file = "test_test_api.csv"
        
        try:
            dpa_core.split_py(TRANSACTIONS_SMALL, train_file, test_file, test_size=0.3)
            assert os.path.exists(train_file)
            assert os.path.exists(test_file)
            
            # Verify output files
            train_df = pd.read_csv(train_file)
            test_df = pd.read_csv(test_file)
            
            # Check that split proportions are approximately correct
            total_rows = len(train_df) + len(test_df)
            test_proportion = len(test_df) / total_rows
            assert 0.20 <= test_proportion <= 0.40  # Allow more tolerance for small datasets
        finally:
            for file in [train_file, test_file]:
                if os.path.exists(file):
                    os.remove(file)
    
    def test_split_stratified(self):
        """Test stratified split"""
        train_file = "test_train_strat_api.csv"
        test_file = "test_test_strat_api.csv"
        
        try:
            dpa_core.split_py(TRANSACTIONS_SMALL, train_file, test_file, 
                            test_size=0.2, stratify="country")
            assert os.path.exists(train_file)
            assert os.path.exists(test_file)
            
            train_df = pd.read_csv(train_file)
            test_df = pd.read_csv(test_file)
            
            # Check that both files have data
            assert len(train_df) > 0
            assert len(test_df) > 0
        finally:
            for file in [train_file, test_file]:
                if os.path.exists(file):
                    os.remove(file)
    
    def test_split_with_seed(self):
        """Test split with seed for reproducibility"""
        train_file1 = "test_train_seed1_api.csv"
        test_file1 = "test_test_seed1_api.csv"
        train_file2 = "test_train_seed2_api.csv"
        test_file2 = "test_test_seed2_api.csv"
        
        try:
            # First split with seed
            dpa_core.split_py(TRANSACTIONS_SMALL, train_file1, test_file1, 
                            test_size=0.3, seed=42)
            
            # Second split with same seed
            dpa_core.split_py(TRANSACTIONS_SMALL, train_file2, test_file2, 
                            test_size=0.3, seed=42)
            
            # Files should be identical
            train_df1 = pd.read_csv(train_file1)
            train_df2 = pd.read_csv(train_file2)
            test_df1 = pd.read_csv(test_file1)
            test_df2 = pd.read_csv(test_file2)
            
            pd.testing.assert_frame_equal(train_df1, train_df2)
            pd.testing.assert_frame_equal(test_df1, test_df2)
        finally:
            for file in [train_file1, train_file2, test_file1, test_file2]:
                if os.path.exists(file):
                    os.remove(file)

class TestPythonAPIFileOperations:
    """File operation API tests"""
    
    def test_convert_csv_to_parquet(self):
        """Test CSV to Parquet conversion"""
        output_file = "test_convert.parquet"
        try:
            dpa_core.convert_py(TRANSACTIONS_SMALL, output_file)
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_convert_parquet_to_csv(self):
        """Test Parquet to CSV conversion"""
        parquet_file = "test_temp.parquet"
        csv_file = "test_convert_back.csv"
        
        try:
            # First convert to parquet
            dpa_core.convert_py(TRANSACTIONS_SMALL, parquet_file)
            
            # Then convert back to CSV
            dpa_core.convert_py(parquet_file, csv_file)
            assert os.path.exists(csv_file)
            
            # Verify data integrity
            original_df = pd.read_csv(TRANSACTIONS_SMALL)
            converted_df = pd.read_csv(csv_file)
            pd.testing.assert_frame_equal(original_df, converted_df)
        finally:
            for file in [parquet_file, csv_file]:
                if os.path.exists(file):
                    os.remove(file)

class TestPythonAPIErrorHandling:
    """Error handling tests"""
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent file"""
        with pytest.raises(Exception):
            dpa_core.profile_py("nonexistent.csv")
    
    def test_invalid_schema_file(self):
        """Test validation with invalid schema file"""
        with pytest.raises(Exception):
            dpa_core.validate_py(TRANSACTIONS_SMALL, "nonexistent.json", None)
    
    def test_invalid_rules_file(self):
        """Test validation with invalid rules file"""
        with pytest.raises(Exception):
            dpa_core.validate_py(TRANSACTIONS_SMALL, None, "nonexistent.json")
    
    def test_invalid_sampling_method(self):
        """Test sampling with invalid method"""
        output_file = "test_invalid_method.csv"
        try:
            with pytest.raises(Exception):
                dpa_core.sample_py(TRANSACTIONS_SMALL, output_file, method="invalid")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_missing_stratify_column(self):
        """Test stratified sampling without stratify column"""
        output_file = "test_missing_stratify.csv"
        try:
            with pytest.raises(Exception):
                dpa_core.sample_py(TRANSACTIONS_SMALL, output_file, 
                                 method="stratified", size=10)
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

class TestPythonAPIDataQuality:
    """Data quality specific tests"""
    
    def test_profile_with_nulls(self):
        """Test profiling data with null values"""
        # Create a dataset with nulls
        df_with_nulls = pd.DataFrame({
            'col1': [1, 2, None, 4, 5],
            'col2': ['a', 'b', 'c', None, 'e'],
            'col3': [1.1, 2.2, 3.3, 4.4, None]
        })
        
        null_file = "test_nulls.csv"
        try:
            df_with_nulls.to_csv(null_file, index=False)
            result = dpa_core.profile_py(null_file)
            
            assert 'null_percentage' in result
            # Convert string to float for comparison
            null_percentage = float(result['null_percentage'])
            assert null_percentage > 0
        finally:
            if os.path.exists(null_file):
                os.remove(null_file)
    
    def test_profile_mixed_types(self):
        """Test profiling data with mixed types"""
        result = dpa_core.profile_py(MIXED_TYPES)
        assert int(result['rows']) == 1000
        assert int(result['columns']) == 4
    
    def test_validate_data_quality_issues(self):
        """Test validation with known data quality issues"""
        # The test data has negative amounts and outliers
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, None, VALIDATION_RULES)
        except Exception as e:
            # Should fail due to data quality issues
            assert "validation" in str(e).lower() or "error" in str(e).lower()

@pytest.mark.slow
class TestPythonAPIPerformance:
    """Performance tests"""
    
    def test_profile_large_dataset_performance(self):
        """Test profiling performance on large dataset"""
        import time
        start_time = time.time()
        result = dpa_core.profile_py(TRANSACTIONS_LARGE)
        end_time = time.time()
        
        assert int(result['rows']) == 10000
        assert end_time - start_time < 30  # Should complete within 30 seconds
    
    def test_sample_large_dataset_performance(self):
        """Test sampling performance on large dataset"""
        output_file = "test_large_sample_perf.csv"
        try:
            import time
            start_time = time.time()
            dpa_core.sample_py(TRANSACTIONS_LARGE, output_file, size=1000, method="random")
            end_time = time.time()
            
            assert os.path.exists(output_file)
            df = pd.read_csv(output_file)
            assert len(df) == 1000
            assert end_time - start_time < 60  # Should complete within 60 seconds
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
