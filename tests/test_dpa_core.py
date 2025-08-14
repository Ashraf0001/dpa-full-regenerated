"""
Tests for the dpa_core module (Rust bindings)
"""
import pytest
import tempfile
import os
import shutil
from pathlib import Path

import dpa_core


class TestDPACore:
    """Test suite for dpa_core module"""
    
    @pytest.fixture
    def sample_data_path(self):
        """Fixture providing path to sample data"""
        return "data/transactions_small.csv"
    
    @pytest.fixture
    def temp_dir(self):
        """Fixture providing temporary directory for test outputs"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_profile_py(self, sample_data_path):
        """Test profile_py function"""
        result = dpa_core.profile_py(sample_data_path)
        
        # Check that result is a dictionary-like object
        assert hasattr(result, 'items')
        
        # Convert to dict for easier testing
        profile_dict = dict(result)
        
        # Check expected keys exist
        expected_keys = ['rows', 'dtype:user_id', 'dtype:amount', 'dtype:country', 
                        'dtype:timestamp', 'dtype:channel']
        for key in expected_keys:
            assert key in profile_dict, f"Missing key: {key}"
        
        # Check specific values
        assert profile_dict['rows'] == '500'
        assert profile_dict['dtype:user_id'] == 'Int64'
        assert profile_dict['dtype:amount'] == 'Float64'
        assert profile_dict['dtype:country'] == 'String'
        assert profile_dict['dtype:timestamp'] == 'Int64'
        assert profile_dict['dtype:channel'] == 'String'
        
        # Check null counts
        null_keys = ['nulls:user_id', 'nulls:amount', 'nulls:country', 
                    'nulls:timestamp', 'nulls:channel']
        for key in null_keys:
            assert key in profile_dict
            assert profile_dict[key] == '0'
    
    def test_convert_py(self, sample_data_path, temp_dir):
        """Test convert_py function"""
        output_path = os.path.join(temp_dir, "output.parquet")
        
        result = dpa_core.convert_py(sample_data_path, output_path)
        
        # Check return value
        assert result == output_path
        
        # Check file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_select_py(self, sample_data_path, temp_dir):
        """Test select_py function"""
        output_path = os.path.join(temp_dir, "selected.parquet")
        columns = ["user_id", "amount"]
        
        result = dpa_core.select_py(sample_data_path, columns, output_path)
        
        # Check return value
        assert result == output_path
        
        # Check file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_select_py_default_output(self, sample_data_path):
        """Test select_py function with default output"""
        columns = ["user_id", "amount"]
        
        result = dpa_core.select_py(sample_data_path, columns)
        
        # Check return value is default output path
        assert result == "dpa_out.parquet"
        
        # Check file was created
        assert os.path.exists("dpa_out.parquet")
        assert os.path.getsize("dpa_out.parquet") > 0
        
        # Clean up
        os.remove("dpa_out.parquet")
    
    def test_filter_py(self, sample_data_path, temp_dir):
        """Test filter_py function"""
        output_path = os.path.join(temp_dir, "filtered.parquet")
        where_expr = "amount > 100"
        
        result = dpa_core.filter_py(sample_data_path, where_expr, None, output_path)
        
        # Check return value
        assert result == output_path
        
        # Check file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_filter_py_with_select(self, sample_data_path, temp_dir):
        """Test filter_py function with column selection"""
        output_path = os.path.join(temp_dir, "filtered_selected.parquet")
        where_expr = "amount > 100"
        select_columns = ["user_id", "amount"]
        
        result = dpa_core.filter_py(sample_data_path, where_expr, select_columns, output_path)
        
        # Check return value
        assert result == output_path
        
        # Check file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_filter_py_default_output(self, sample_data_path):
        """Test filter_py function with default output"""
        where_expr = "amount > 100"
        
        result = dpa_core.filter_py(sample_data_path, where_expr)
        
        # Check return value is default output path
        assert result == "dpa_out.parquet"
        
        # Check file was created
        assert os.path.exists("dpa_out.parquet")
        assert os.path.getsize("dpa_out.parquet") > 0
        
        # Clean up
        os.remove("dpa_out.parquet")
    
    def test_invalid_file_path(self):
        """Test error handling for invalid file path"""
        with pytest.raises(Exception):
            dpa_core.profile_py("nonexistent_file.csv")
    
    def test_invalid_sql_expression(self, sample_data_path):
        """Test error handling for invalid SQL expression"""
        with pytest.raises(Exception):
            dpa_core.filter_py(sample_data_path, "invalid sql expression")
    
    def test_invalid_column_names(self, sample_data_path):
        """Test error handling for invalid column names"""
        with pytest.raises(Exception):
            dpa_core.select_py(sample_data_path, ["nonexistent_column"])
    
    def test_empty_columns_list(self, sample_data_path):
        """Test handling of empty columns list (creates empty DataFrame)"""
        result = dpa_core.select_py(sample_data_path, [])
        
        # Check return value is default output path
        assert result == "dpa_out.parquet"
        
        # Check file was created (even if empty)
        assert os.path.exists("dpa_out.parquet")
        
        # Clean up
        os.remove("dpa_out.parquet")
    
    def test_module_attributes(self):
        """Test that all expected functions are available"""
        expected_functions = ['filter_py', 'select_py', 'convert_py', 'profile_py']
        
        for func_name in expected_functions:
            assert hasattr(dpa_core, func_name), f"Missing function: {func_name}"
            assert callable(getattr(dpa_core, func_name)), f"Not callable: {func_name}"
