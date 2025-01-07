#!/bin/bash

# Create/Refresh virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create report directory
mkdir -p test-reports

# Run tests with xmlrunner (for XML output - MOST IMPORTANT CHANGE)
python -m xmlrunner discover -s . -p "test_*.py" -t . -o test-reports

# Run tests with pytest (for HTML output - optional)
if command -v pytest &> /dev/null; then
    pytest --html=test-reports/report.html
fi

open test-reports/report.html

deactivate