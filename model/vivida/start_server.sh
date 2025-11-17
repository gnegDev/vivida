#!/bin/bash
# GBM Treatment Optimization API v3.0 - Linux/Mac Startup Script

echo "================================================================================"
echo "GBM TREATMENT OPTIMIZATION API v3.0"
echo "================================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Starting API server..."
echo ""
echo "Server will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================================================================"
echo ""

python3 app.py
