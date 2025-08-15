# TestPyPI Publishing Guide

This guide explains how to set up and use the TestPyPI publishing pipeline for the Data Processing Accelerator (DPA) project.

## 🎯 **Why TestPyPI?**

TestPyPI is perfect for:
- **Testing package distribution** before PyPI
- **Validating installation process**
- **Testing CI/CD pipelines**
- **Getting feedback from users**
- **Safe experimentation**

## 🚀 **Quick Start**

### **1. Automatic Publishing (Recommended)**

The GitHub Actions workflow automatically publishes to TestPyPI when you push to the `feature-testing` branch:

```bash
# Push to trigger automatic publishing
git push origin feature-testing
```

### **2. Manual Publishing**

Use the local script for manual publishing:

```bash
# Run full pipeline
./scripts/publish-testpypi.sh full

# Or step by step
./scripts/publish-testpypi.sh check
./scripts/publish-testpypi.sh build
./scripts/publish-testpypi.sh test
./scripts/publish-testpypi.sh publish
```

## 🔧 **Setup Requirements**

### **1. TestPyPI Account**

1. **Create TestPyPI Account:**
   - Visit: https://test.pypi.org/account/register/
   - Create an account with your email

2. **Generate API Token:**
   - Go to: https://test.pypi.org/manage/account/token/
   - Create a new token with "Entire account" scope
   - Copy the token (starts with `pypi-`)

### **2. GitHub Secrets**

Add the TestPyPI token to your GitHub repository secrets:

1. **Go to Repository Settings:**
   ```
   https://github.com/Ashraf0001/data-processing-accelerator-dpa/settings/secrets/actions
   ```

2. **Add New Secret:**
   - **Name:** `TESTPYPI_API_TOKEN`
   - **Value:** Your TestPyPI API token

### **3. Local Environment**

For local publishing, set the environment variable:

```bash
export TESTPYPI_API_TOKEN=pypi-your-token-here
```

## 📦 **What Gets Published**

The pipeline publishes two packages:

### **1. Rust Wheel (`dpa`)**
- **Source:** Rust code with PyO3 bindings
- **Package:** `dpa` (core library)
- **Usage:** `import dpa_core`

### **2. Python CLI (`dpa-cli`)**
- **Source:** Python CLI wrapper
- **Package:** `dpa-cli` (command-line tool)
- **Usage:** `dpa --help`

## 🧪 **Testing the Published Packages**

### **Install from TestPyPI**

```bash
# Install the CLI package
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dpa-cli

# Test the installation
dpa --help
python3 -c "import dpa_core; print('Success!')"
```

### **Test Different Features**

```bash
# Test data profiling
dpa profile data/transactions_small.csv

# Test data validation
dpa validate data/transactions_small.csv

# Test data sampling
dpa sample data/transactions_small.csv -n 100
```

## 🔄 **Workflow Process**

### **Automatic Pipeline (GitHub Actions)**

1. **Trigger:** Push to `feature-testing` branch
2. **Test:** Run full test suite (Rust + Python)
3. **Build:** Create Rust wheel and Python package
4. **Publish:** Upload to TestPyPI
5. **Release:** Create GitHub release
6. **Notify:** Send completion notification

### **Manual Pipeline (Local Script)**

1. **Check:** Verify prerequisites
2. **Build:** Compile Rust and Python packages
3. **Test:** Local functionality testing
4. **Publish:** Upload to TestPyPI
5. **Instructions:** Show installation guide

## 📋 **Version Management**

### **Updating Versions**

Before publishing, update versions in:

1. **`Cargo.toml`:**
   ```toml
   [package]
   version = "0.2.2"
   ```

2. **`python/pyproject.toml`:**
   ```toml
   [project]
   version = "0.2.2"
   ```

### **Version Strategy**

- **TestPyPI:** Use `feature-testing` branch with incremental versions
- **PyPI:** Use `main` branch for stable releases
- **Format:** Semantic versioning (e.g., `0.2.2`)

## 🎯 **Best Practices**

### **Before Publishing**

1. **✅ Run Tests:**
   ```bash
   cargo test
   pytest tests/
   ```

2. **✅ Check Build:**
   ```bash
   cargo build --release
   maturin build --release
   ```

3. **✅ Test Locally:**
   ```bash
   pip install target/wheels/*.whl
   python3 -c "import dpa_core"
   ```

### **After Publishing**

1. **✅ Verify Installation:**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dpa-cli
   ```

2. **✅ Test Functionality:**
   ```bash
   dpa --help
   dpa profile data/transactions_small.csv
   ```

3. **✅ Check TestPyPI Page:**
   - Visit: https://test.pypi.org/project/dpa-cli/

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Authentication Error:**
   ```
   Error: Invalid credentials
   ```
   **Solution:** Check your `TESTPYPI_API_TOKEN`

2. **Package Already Exists:**
   ```
   Error: File already exists
   ```
   **Solution:** Increment version number

3. **Build Failures:**
   ```
   Error: Build failed
   ```
   **Solution:** Check Rust/Python dependencies

### **Debug Commands**

```bash
# Check TestPyPI token
echo $TESTPYPI_API_TOKEN

# Test twine configuration
twine check target/wheels/*.whl

# Verify package structure
tar -tzf python/dist/*.tar.gz
```

## 📊 **Monitoring**

### **TestPyPI Dashboard**

- **Project Page:** https://test.pypi.org/project/dpa-cli/
- **Account:** https://test.pypi.org/manage/account/
- **API Tokens:** https://test.pypi.org/manage/account/token/

### **GitHub Actions**

- **Workflow Runs:** https://github.com/Ashraf0001/data-processing-accelerator-dpa/actions
- **Releases:** https://github.com/Ashraf0001/data-processing-accelerator-dpa/releases

## 🔗 **Useful Links**

- **TestPyPI:** https://test.pypi.org/
- **PyPI:** https://pypi.org/
- **Twine Documentation:** https://twine.readthedocs.io/
- **Maturin Documentation:** https://www.maturin.rs/

## 📝 **Next Steps**

After successful TestPyPI testing:

1. **Merge to Main:** When ready for production
2. **PyPI Publishing:** Set up production PyPI pipeline
3. **Documentation:** Update installation guides
4. **Announcement:** Share with community

---

**Happy Testing! 🚀**
# TestPyPI Ready
# TestPyPI Pipeline Test - Fri Aug 15 15:53:23 CEST 2025
# Trigger TestPyPI workflow - Fri Aug 15 16:52:16 CEST 2025
