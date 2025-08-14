"""
Tests for the CLI functionality
"""
import pytest
import subprocess
import tempfile
import os
import shutil
from pathlib import Path


class TestCLI:
    """Test suite for CLI functionality"""
    
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
    
    def test_help_command(self):
        """Test help command"""
        result = subprocess.run(["./target/debug/dpa", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Data Processing Accelerator" in result.stdout
        assert "schema" in result.stdout
        assert "filter" in result.stdout
    
    def test_schema_command(self, sample_data_path):
        """Test schema command"""
        result = subprocess.run(["./target/debug/dpa", "schema", sample_data_path], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "user_id" in result.stdout
        assert "amount" in result.stdout
        assert "country" in result.stdout
        assert "timestamp" in result.stdout
        assert "channel" in result.stdout
    
    def test_head_command(self, sample_data_path):
        """Test head command"""
        result = subprocess.run(["./target/debug/dpa", "head", sample_data_path, "-n", "5"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "shape: (5, 5)" in result.stdout
    
    def test_profile_command(self, sample_data_path):
        """Test profile command"""
        result = subprocess.run(["./target/debug/dpa", "profile", sample_data_path], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Rows(sampled): 500" in result.stdout
        assert "user_id: Int64" in result.stdout
        assert "amount: Float64" in result.stdout
    
    def test_convert_command(self, sample_data_path, temp_dir):
        """Test convert command"""
        output_path = os.path.join(temp_dir, "output.parquet")
        result = subprocess.run(["./target/debug/dpa", "convert", sample_data_path, output_path], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_select_command(self, sample_data_path, temp_dir):
        """Test select command"""
        output_path = os.path.join(temp_dir, "selected.parquet")
        result = subprocess.run([
            "./target/debug/dpa", "select", sample_data_path, 
            "-c", "user_id,amount", "-o", output_path
        ], capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_filter_command(self, sample_data_path, temp_dir):
        """Test filter command"""
        output_path = os.path.join(temp_dir, "filtered.parquet")
        result = subprocess.run([
            "./target/debug/dpa", "filter", sample_data_path, 
            "-w", "amount > 100", "-o", output_path
        ], capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_filter_with_select(self, sample_data_path, temp_dir):
        """Test filter command with column selection"""
        output_path = os.path.join(temp_dir, "filtered_selected.parquet")
        result = subprocess.run([
            "./target/debug/dpa", "filter", sample_data_path, 
            "-w", "amount > 100", "-s", "user_id,amount", "-o", output_path
        ], capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_invalid_file(self):
        """Test error handling for invalid file"""
        result = subprocess.run(["./target/debug/dpa", "schema", "nonexistent.csv"], 
                              capture_output=True, text=True)
        assert result.returncode != 0
        assert "error" in result.stderr.lower() or "failed" in result.stderr.lower()
    
    def test_invalid_command(self):
        """Test error handling for invalid command"""
        result = subprocess.run(["./target/debug/dpa", "invalid_command"], 
                              capture_output=True, text=True)
        assert result.returncode != 0
    
    def test_missing_required_args(self):
        """Test error handling for missing required arguments"""
        result = subprocess.run(["./target/debug/dpa", "schema"], 
                              capture_output=True, text=True)
        assert result.returncode != 0


class TestPythonCLI:
    """Test suite for Python CLI functionality"""
    
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
    
    def test_help_command(self):
        """Test help command"""
        result = subprocess.run(["python3", "-m", "dpa", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Data Processing Accelerator" in result.stdout
        assert "filter" in result.stdout
        assert "select" in result.stdout
    
    def test_profile_command(self, sample_data_path):
        """Test profile command"""
        result = subprocess.run(["python3", "-m", "dpa", "profile", sample_data_path], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "rows: 500" in result.stdout
        assert "dtype:user_id" in result.stdout
    
    def test_convert_command(self, sample_data_path, temp_dir):
        """Test convert command"""
        output_path = os.path.join(temp_dir, "output.parquet")
        result = subprocess.run([
            "python3", "-m", "dpa", "convert", sample_data_path, output_path
        ], capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_select_command(self, sample_data_path, temp_dir):
        """Test select command"""
        output_path = os.path.join(temp_dir, "selected.parquet")
        result = subprocess.run([
            "python3", "-m", "dpa", "select", sample_data_path, 
            "-c", "user_id,amount", "-o", output_path
        ], capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_filter_command(self, sample_data_path, temp_dir):
        """Test filter command"""
        output_path = os.path.join(temp_dir, "filtered.parquet")
        result = subprocess.run([
            "python3", "-m", "dpa", "filter", sample_data_path, 
            "-w", "amount > 100", "-o", output_path
        ], capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
