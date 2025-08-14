#!/bin/bash

# Publish to TestPyPI Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Publishing to TestPyPI${NC}"

# Check if wheels exist
if [ ! -d "target/wheels" ] || [ -z "$(ls -A target/wheels 2>/dev/null)" ]; then
    echo -e "${RED}Error: No wheels found in target/wheels/${NC}"
    echo -e "${YELLOW}Please run ./scripts/build_and_publish.sh first${NC}"
    exit 1
fi

echo -e "${YELLOW}Found wheels:${NC}"
ls -la target/wheels/

echo -e "${YELLOW}Publishing to TestPyPI...${NC}"
echo -e "${YELLOW}You will be prompted for your TestPyPI credentials.${NC}"
echo -e "${YELLOW}If you don't have a TestPyPI account, create one at: https://test.pypi.org/account/register/${NC}"
echo ""

# Upload to TestPyPI
python3 -m twine upload --repository testpypi target/wheels/*

echo -e "${GREEN}✅ Successfully published to TestPyPI!${NC}"
echo ""
echo -e "${YELLOW}To install from TestPyPI:${NC}"
echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dpa-cli"
echo ""
echo -e "${YELLOW}To install with uv from TestPyPI:${NC}"
echo "  uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dpa-cli"
echo ""
echo -e "${YELLOW}TestPyPI URL: https://test.pypi.org/project/dpa-cli/${NC}"
