#!/usr/bin/env python3
"""
Simple HTTP server for the Computing Evolution Dashboard

This script serves the dashboard locally for development and testing.

Usage:
    python serve.py [port]

Default port: 8000
"""

import http.server
import socketserver
import sys
import os
from pathlib import Path

# Default port
PORT = 8000

# Parse command line arguments
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port number: {sys.argv[1]}")
        print("Usage: python serve.py [port]")
        sys.exit(1)

# Change to dashboard directory
dashboard_dir = Path(__file__).parent
os.chdir(dashboard_dir)

# Create custom handler to set CORS headers
class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow data loading
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

# Start server
Handler = CORSRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 70)
        print("Computing Evolution Dashboard - Development Server")
        print("=" * 70)
        print(f"\nServer running at: http://localhost:{PORT}")
        print(f"Dashboard URL: http://localhost:{PORT}/index.html")
        print(f"\nServing from: {dashboard_dir}")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 70)
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\nServer stopped.")
    sys.exit(0)
except OSError as e:
    if e.errno == 48 or e.errno == 98:  # Address already in use
        print(f"\nError: Port {PORT} is already in use.")
        print(f"Try a different port: python serve.py {PORT + 1}")
    else:
        print(f"\nError starting server: {e}")
    sys.exit(1)
