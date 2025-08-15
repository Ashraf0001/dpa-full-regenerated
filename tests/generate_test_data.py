#!/usr/bin/env python3
"""
Generate synthetic test data for DPA testing
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

def generate_transactions_data(n_rows=10000):
    """Generate realistic transaction data with various data quality issues"""
    np.random.seed(42)
    
    # Generate user IDs
    user_ids = np.random.randint(1, 10001, n_rows)
    
    # Generate amounts with some outliers and negative values
    amounts = np.random.exponential(50, n_rows)
    # Add some outliers
    outlier_indices = np.random.choice(n_rows, size=int(n_rows * 0.05), replace=False)
    amounts[outlier_indices] = np.random.uniform(1000, 10000, len(outlier_indices))
    # Add some negative values (data quality issue)
    negative_indices = np.random.choice(n_rows, size=int(n_rows * 0.02), replace=False)
    amounts[negative_indices] = -np.random.uniform(10, 100, len(negative_indices))
    
    # Generate countries with some missing values
    countries = np.random.choice(['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP'], n_rows)
    missing_country_indices = np.random.choice(n_rows, size=int(n_rows * 0.03), replace=False)
    countries[missing_country_indices] = None
    
    # Generate timestamps
    start_date = datetime(2024, 1, 1)
    timestamps = [start_date + timedelta(seconds=np.random.randint(0, 365*24*3600)) for _ in range(n_rows)]
    
    # Generate channels
    channels = np.random.choice(['web', 'mobile', 'pos'], n_rows)
    
    # Create DataFrame
    df = pd.DataFrame({
        'user_id': user_ids,
        'amount': amounts,
        'country': countries,
        'timestamp': timestamps,
        'channel': channels
    })
    
    return df

def generate_customers_data(n_rows=5000):
    """Generate customer data for joins"""
    np.random.seed(42)
    
    customer_ids = np.arange(1, n_rows + 1)
    names = [f"Customer_{i}" for i in customer_ids]
    emails = [f"customer_{i}@example.com" for i in customer_ids]
    ages = np.random.normal(35, 15, n_rows).astype(int)
    ages = np.clip(ages, 18, 80)
    
    # Add some invalid ages
    invalid_age_indices = np.random.choice(n_rows, size=int(n_rows * 0.01), replace=False)
    ages[invalid_age_indices] = np.random.choice([-5, 0, 150, 200], len(invalid_age_indices))
    
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'name': names,
        'email': emails,
        'age': ages
    })
    
    return df

def generate_products_data(n_rows=1000):
    """Generate product data"""
    np.random.seed(42)
    
    product_ids = np.arange(1, n_rows + 1)
    names = [f"Product_{i}" for i in product_ids]
    categories = np.random.choice(['Electronics', 'Clothing', 'Books', 'Food', 'Sports'], n_rows)
    prices = np.random.uniform(10, 500, n_rows)
    
    df = pd.DataFrame({
        'product_id': product_ids,
        'name': names,
        'category': categories,
        'price': prices
    })
    
    return df

def generate_mixed_data_types(n_rows=1000):
    """Generate data with mixed types in string columns"""
    np.random.seed(42)
    
    # String column with mixed types
    mixed_col = []
    for i in range(n_rows):
        if i % 3 == 0:
            mixed_col.append(str(np.random.randint(1, 100)))  # Numbers as strings
        elif i % 3 == 1:
            mixed_col.append(f"2024-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}")  # Dates as strings
        else:
            mixed_col.append(f"text_{i}")  # Regular text
    
    df = pd.DataFrame({
        'id': range(n_rows),
        'mixed_column': mixed_col,
        'numeric_col': np.random.normal(0, 1, n_rows),
        'categorical_col': np.random.choice(['A', 'B', 'C', 'D'], n_rows)
    })
    
    return df

def create_test_files():
    """Create all test files"""
    # Create test data directory
    os.makedirs('tests/test_data', exist_ok=True)
    
    # Generate and save data
    print("Generating test data...")
    
    # Transactions data
    transactions_df = generate_transactions_data(10000)
    transactions_df.to_csv('tests/test_data/transactions_large.csv', index=False)
    transactions_df.head(1000).to_csv('tests/test_data/transactions_medium.csv', index=False)
    transactions_df.head(100).to_csv('tests/test_data/transactions_small.csv', index=False)
    
    # Customers data
    customers_df = generate_customers_data(5000)
    customers_df.to_csv('tests/test_data/customers.csv', index=False)
    
    # Products data
    products_df = generate_products_data(1000)
    products_df.to_csv('tests/test_data/products.csv', index=False)
    
    # Mixed data types
    mixed_df = generate_mixed_data_types(1000)
    mixed_df.to_csv('tests/test_data/mixed_types.csv', index=False)
    
    # Create schema files
    print("Creating schema files...")
    
    # Valid schema
    valid_schema = {
        "user_id": "Int64",
        "amount": "Float64",
        "country": "String",
        "timestamp": "Int64",
        "channel": "String"
    }
    
    with open('tests/test_data/valid_schema.json', 'w') as f:
        json.dump(valid_schema, f, indent=2)
    
    # Invalid schema (mismatched types)
    invalid_schema = {
        "user_id": "String",  # Should be Int64
        "amount": "String",   # Should be Float64
        "country": "Int64",   # Should be String
        "timestamp": "String", # Should be Int64
        "channel": "Float64"  # Should be String
    }
    
    with open('tests/test_data/invalid_schema.json', 'w') as f:
        json.dump(invalid_schema, f, indent=2)
    
    # Validation rules
    print("Creating validation rules...")
    
    validation_rules = [
        {
            "name": "positive_amounts",
            "column": "amount",
            "rule_type": "range",
            "expression": "0,1000",
            "message": "Amount should be between 0 and 1000",
            "severity": "error"
        },
        {
            "name": "valid_countries",
            "column": "country",
            "rule_type": "sql",
            "expression": "country IN ('US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP')",
            "message": "Country should be one of the valid countries",
            "severity": "warning"
        },
        {
            "name": "user_id_range",
            "column": "user_id",
            "rule_type": "range",
            "expression": "1,10000",
            "message": "User ID should be between 1 and 10000",
            "severity": "error"
        }
    ]
    
    with open('tests/test_data/validation_rules.json', 'w') as f:
        json.dump(validation_rules, f, indent=2)
    
    # Create summary
    print("\nTest data summary:")
    print(f"✅ transactions_large.csv: {len(transactions_df)} rows")
    print(f"✅ transactions_medium.csv: {len(transactions_df.head(1000))} rows")
    print(f"✅ transactions_small.csv: {len(transactions_df.head(100))} rows")
    print(f"✅ customers.csv: {len(customers_df)} rows")
    print(f"✅ products.csv: {len(products_df)} rows")
    print(f"✅ mixed_types.csv: {len(mixed_df)} rows")
    print(f"✅ valid_schema.json: Schema for transactions data")
    print(f"✅ invalid_schema.json: Schema with type mismatches")
    print(f"✅ validation_rules.json: Custom validation rules")
    
    # Data quality summary
    print("\nData quality issues included:")
    print(f"🔍 {len(transactions_df[transactions_df['amount'] < 0])} negative amounts")
    print(f"🔍 {len(transactions_df[transactions_df['amount'] > 1000])} outlier amounts (>1000)")
    print(f"🔍 {transactions_df['country'].isna().sum()} missing countries")
    print(f"🔍 {len(customers_df[customers_df['age'] < 0])} invalid ages")
    print(f"🔍 Mixed data types in mixed_types.csv")

if __name__ == "__main__":
    create_test_files()

