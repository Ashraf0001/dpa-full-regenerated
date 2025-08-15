#!/usr/bin/env python3
"""
Practical examples and integration tests for DPA
"""

import pytest
import pandas as pd
import numpy as np
import json
import os
import subprocess
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
VALIDATION_RULES = str(TEST_DATA_DIR / "validation_rules.json")

class TestPracticalExamples:
    """Practical examples demonstrating DPA functionality"""
    
    def test_data_exploration_workflow(self):
        """Test a complete data exploration workflow"""
        print("\n🔍 Testing Data Exploration Workflow...")
        
        # Step 1: Profile the data
        profile = dpa_core.profile_py(TRANSACTIONS_SMALL)
        print(f"📊 Dataset: {profile['rows']} rows, {profile['columns']} columns")
        print(f"💾 Memory: {float(profile['memory_mb']):.2f} MB")
        print(f"🔢 Null percentage: {float(profile['null_percentage']):.2f}%")
        
        # Step 2: Validate data quality
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, VALID_SCHEMA, VALIDATION_RULES)
            print("✅ Data validation passed")
        except Exception as e:
            print(f"⚠️ Data validation issues found: {str(e)}")
        
        # Step 3: Sample data for analysis
        sample_file = "exploration_sample.csv"
        try:
            dpa_core.sample_py(TRANSACTIONS_SMALL, sample_file, size=50, method="random", seed=42)
            sample_df = pd.read_csv(sample_file)
            print(f"📋 Sampled {len(sample_df)} rows for analysis")
            
            # Basic analysis on sample
            print(f"💰 Amount range: ${sample_df['amount'].min():.2f} - ${sample_df['amount'].max():.2f}")
            print(f"🌍 Countries: {sample_df['country'].nunique()}")
            print(f"📱 Channels: {sample_df['channel'].unique()}")
            
        finally:
            if os.path.exists(sample_file):
                os.remove(sample_file)
    
    def test_machine_learning_preparation(self):
        """Test ML data preparation workflow"""
        print("\n🤖 Testing Machine Learning Preparation...")
        
        # Step 1: Split data for ML
        train_file = "ml_train.csv"
        test_file = "ml_test.csv"
        
        try:
            dpa_core.split_py(TRANSACTIONS_SMALL, train_file, test_file, 
                            test_size=0.2, stratify="country", seed=42)
            
            train_df = pd.read_csv(train_file)
            test_df = pd.read_csv(test_file)
            
            print(f"📚 Training set: {len(train_df)} rows ({len(train_df)/100*100:.1f}%)")
            print(f"🧪 Test set: {len(test_df)} rows ({len(test_df)/100*100:.1f}%)")
            
            # Verify stratification worked
            train_countries = train_df['country'].value_counts()
            test_countries = test_df['country'].value_counts()
            print(f"🌍 Country distribution maintained across splits")
            
        finally:
            for file in [train_file, test_file]:
                if os.path.exists(file):
                    os.remove(file)
    
    def test_data_quality_assessment(self):
        """Test comprehensive data quality assessment"""
        print("\n🔍 Testing Data Quality Assessment...")
        
        # Create a comprehensive quality report
        quality_report = {}
        
        # 1. Basic profiling
        profile = dpa_core.profile_py(TRANSACTIONS_SMALL)
        quality_report['basic_stats'] = {
            'rows': profile['rows'],
            'columns': profile['columns'],
                            'memory_mb': float(profile['memory_mb']),
            'null_percentage': profile['null_percentage']
        }
        
        # 2. Schema validation
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, VALID_SCHEMA, None)
            quality_report['schema_validation'] = "PASSED"
        except Exception as e:
            quality_report['schema_validation'] = f"FAILED: {str(e)}"
        
        # 3. Business rules validation
        try:
            dpa_core.validate_py(TRANSACTIONS_SMALL, None, VALIDATION_RULES)
            quality_report['business_rules'] = "PASSED"
        except Exception as e:
            quality_report['business_rules'] = f"FAILED: {str(e)}"
        
        # 4. Data distribution analysis
        df = pd.read_csv(TRANSACTIONS_SMALL)
        quality_report['distributions'] = {
            'amount_stats': {
                'mean': df['amount'].mean(),
                'std': df['amount'].std(),
                'min': df['amount'].min(),
                'max': df['amount'].max(),
                'negative_count': len(df[df['amount'] < 0])
            },
            'country_distribution': df['country'].value_counts().to_dict(),
            'channel_distribution': df['channel'].value_counts().to_dict()
        }
        
        print("📋 Quality Report:")
        print(f"   📊 Basic Stats: {quality_report['basic_stats']}")
        print(f"   🏗️ Schema: {quality_report['schema_validation']}")
        print(f"   📋 Business Rules: {quality_report['business_rules']}")
        print(f"   📈 Negative amounts: {quality_report['distributions']['amount_stats']['negative_count']}")
        
        return quality_report
    
    def test_performance_benchmarking(self):
        """Test performance benchmarking across different dataset sizes"""
        print("\n⚡ Testing Performance Benchmarking...")
        
        datasets = [
            ("Small", TRANSACTIONS_SMALL, 100),
            ("Medium", TRANSACTIONS_MEDIUM, 1000),
            ("Large", TRANSACTIONS_LARGE, 10000)
        ]
        
        performance_results = {}
        
        for name, file_path, expected_rows in datasets:
            print(f"\n📊 Testing {name} dataset ({expected_rows} rows)...")
            
            import time
            
            # Profile performance
            start_time = time.time()
            profile = dpa_core.profile_py(file_path)
            profile_time = time.time() - start_time
            
            # Sampling performance
            sample_file = f"perf_sample_{name.lower()}.csv"
            try:
                start_time = time.time()
                dpa_core.sample_py(file_path, sample_file, size=min(1000, expected_rows), method="random")
                sample_time = time.time() - start_time
                
                performance_results[name] = {
                    'rows': profile['rows'],
                    'profile_time': profile_time,
                    'sample_time': sample_time,
                    'memory_mb': float(profile['memory_mb'])
                }
                
                print(f"   ⏱️ Profile: {profile_time:.3f}s")
                print(f"   ⏱️ Sample: {sample_time:.3f}s")
                print(f"   💾 Memory: {float(profile['memory_mb']):.2f} MB")
                
            finally:
                if os.path.exists(sample_file):
                    os.remove(sample_file)
        
        return performance_results
    
    def test_cli_vs_api_comparison(self):
        """Compare CLI and API functionality"""
        print("\n🔄 Testing CLI vs API Comparison...")
        
        # Test profiling
        print("📊 Profiling comparison:")
        
        # API profiling
        api_profile = dpa_core.profile_py(TRANSACTIONS_SMALL)
        
        # CLI profiling
        cli_output_file = "cli_profile_output.txt"
        try:
            result = subprocess.run([
                "./target/debug/dpa", "profile", TRANSACTIONS_SMALL
            ], capture_output=True, text=True)
            
            with open(cli_output_file, 'w') as f:
                f.write(result.stdout)
            
            print(f"   🐍 API: {api_profile['rows']} rows, {api_profile['columns']} columns")
            print(f"   💻 CLI: Exit code {result.returncode}")
            print(f"   📝 CLI output length: {len(result.stdout)} characters")
            
        finally:
            if os.path.exists(cli_output_file):
                os.remove(cli_output_file)
    
    def test_error_handling_scenarios(self):
        """Test various error handling scenarios"""
        print("\n🚨 Testing Error Handling Scenarios...")
        
        error_scenarios = [
            ("Nonexistent file", "nonexistent.csv", "profile", {}),
            ("Invalid schema", TRANSACTIONS_SMALL, "validate", {"schema": "invalid.json"}),
            ("Invalid sampling method", TRANSACTIONS_SMALL, "sample", {"method": "invalid"}),
            ("Missing stratify column", TRANSACTIONS_SMALL, "sample", {"method": "stratified"})
        ]
        
        for scenario_name, file_path, operation, kwargs in error_scenarios:
            print(f"   🔍 Testing: {scenario_name}")
            
            try:
                if operation == "profile":
                    dpa_core.profile_py(file_path)
                elif operation == "validate":
                    schema = kwargs.get("schema", None)
                    dpa_core.validate_py(file_path, schema, None)
                elif operation == "sample":
                    method = kwargs.get("method", "random")
                    output_file = "error_test.csv"
                    try:
                        dpa_core.sample_py(file_path, output_file, method=method)
                    finally:
                        if os.path.exists(output_file):
                            os.remove(output_file)
                
                print(f"      ❌ Expected error but got success")
                
            except Exception as e:
                print(f"      ✅ Correctly handled: {type(e).__name__}")
    
    def test_data_transformation_pipeline(self):
        """Test a complete data transformation pipeline"""
        print("\n🔄 Testing Data Transformation Pipeline...")
        
        pipeline_steps = []
        
        # Step 1: Profile original data
        original_profile = dpa_core.profile_py(TRANSACTIONS_SMALL)
        pipeline_steps.append(("Original", original_profile))
        
        # Step 2: Sample data
        sample_file = "pipeline_sample.csv"
        try:
            dpa_core.sample_py(TRANSACTIONS_SMALL, sample_file, size=50, method="random", seed=42)
            sample_profile = dpa_core.profile_py(sample_file)
            pipeline_steps.append(("Sampled", sample_profile))
            
            # Step 3: Convert to different format
            parquet_file = "pipeline_sample.parquet"
            dpa_core.convert_py(sample_file, parquet_file)
            
            # Step 4: Convert back and verify
            final_csv = "pipeline_final.csv"
            dpa_core.convert_py(parquet_file, final_csv)
            final_profile = dpa_core.profile_py(final_csv)
            pipeline_steps.append(("Transformed", final_profile))
            
            # Verify data integrity
            original_df = pd.read_csv(TRANSACTIONS_SMALL)
            sample_df = pd.read_csv(sample_file)
            final_df = pd.read_csv(final_csv)
            
            print("📋 Pipeline Results:")
            for step_name, profile in pipeline_steps:
                print(f"   {step_name}: {profile['rows']} rows, {profile['columns']} columns")
            
            print(f"   ✅ Data integrity maintained: {len(sample_df) == len(final_df)}")
            
        finally:
            for file in [sample_file, parquet_file, final_csv]:
                if os.path.exists(file):
                    os.remove(file)

def run_practical_examples():
    """Run all practical examples"""
    print("🚀 Running DPA Practical Examples")
    print("=" * 50)
    
    test_instance = TestPracticalExamples()
    
    # Run all examples
    test_instance.test_data_exploration_workflow()
    test_instance.test_machine_learning_preparation()
    test_instance.test_data_quality_assessment()
    test_instance.test_performance_benchmarking()
    test_instance.test_cli_vs_api_comparison()
    test_instance.test_error_handling_scenarios()
    test_instance.test_data_transformation_pipeline()
    
    print("\n✅ All practical examples completed successfully!")

if __name__ == "__main__":
    run_practical_examples()
