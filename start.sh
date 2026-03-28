#!/bin/bash

# HealTrack AI - Quick Start Script for macOS/Linux

echo ""
echo "================================================"
echo "  HealTrack AI - Startup Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install it with: brew install python3"
    exit 1
fi

# Check if Node.js is installed  
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Install it with: brew install node"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[1/3] Starting Backend API Server..."
echo "       Port: 5000"
cd "$SCRIPT_DIR/backend"
python3 app.py &
BACKEND_PID=$!
sleep 2

echo "[2/3] Starting Frontend Dev Server..."
echo "       Port: 5173"
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!
sleep 2

echo ""
echo "================================================"
echo "  All services started!"
echo "================================================"
echo ""
echo "  Frontend:  http://localhost:5173"
echo "  Backend:   http://localhost:5000"
echo ""
echo "  ✓ Backend running (PID: $BACKEND_PID)"
echo "  ✓ Frontend running (PID: $FRONTEND_PID)"
echo ""
echo "  Open browser to http://localhost:5173"
echo ""
echo "  To stop: Press Ctrl+C"
echo ""

# Wait for processes
wait
