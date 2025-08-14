#!/usr/bin/env python3
"""
Basic usage examples for the DPA library
"""

import dpa_core
import os

def main():
    """Demonstrate basic DPA functionality"""
    
    # Sample data file
    input_file = "data/transactions_small.csv"
    
    print("=== DPA Basic Usage Examples ===\n")
    
    # 1. Profile the data
    print("1. Profiling data...")
    profile = dpa_core.profile_py(input_file)
    profile_dict = dict(profile)
    
    print(f"   Rows: {profile_dict['rows']}")
    print(f"   Columns:")
    for key, value in profile_dict.items():
        if key.startswith('dtype:'):
            col_name = key.replace('dtype:', '')
            null_count = profile_dict.get(f'nulls:{col_name}', 'N/A')
            print(f"     - {col_name}: {value} (nulls: {null_count})")
    
    print()
    
    # 2. Convert CSV to Parquet
    print("2. Converting CSV to Parquet...")
    parquet_file = "examples/output.parquet"
    dpa_core.convert_py(input_file, parquet_file)
    print(f"   Created: {parquet_file}")
    print(f"   Size: {os.path.getsize(parquet_file)} bytes")
    
    print()
    
    # 3. Select specific columns
    print("3. Selecting columns...")
    selected_file = "examples/selected.parquet"
    columns = ["user_id", "amount", "country"]
    dpa_core.select_py(input_file, columns, selected_file)
    print(f"   Selected columns: {columns}")
    print(f"   Output: {selected_file}")
    
    print()
    
    # 4. Filter data
    print("4. Filtering data...")
    filtered_file = "examples/filtered.parquet"
    where_expr = "amount > 100"
    dpa_core.filter_py(input_file, where_expr, None, filtered_file)
    print(f"   Filter: {where_expr}")
    print(f"   Output: {filtered_file}")
    
    print()
    
    # 5. Filter with column selection
    print("5. Filtering with column selection...")
    result_file = "examples/result.parquet"
    select_cols = ["user_id", "amount"]
    dpa_core.filter_py(input_file, where_expr, select_cols, result_file)
    print(f"   Filter: {where_expr}")
    print(f"   Selected columns: {select_cols}")
    print(f"   Output: {result_file}")
    
    print()
    
    # 6. Show file sizes
    print("6. File sizes comparison:")
    files = [
        ("Original CSV", input_file),
        ("Converted Parquet", parquet_file),
        ("Selected columns", selected_file),
        ("Filtered data", filtered_file),
        ("Filtered + selected", result_file)
    ]
    
    for name, file_path in files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   {name}: {size:,} bytes")
    
    print("\n=== Cleanup ===")
    # Clean up example files
    for _, file_path in files[1:]:  # Skip original CSV
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"   Removed: {file_path}")

if __name__ == "__main__":
    main()
