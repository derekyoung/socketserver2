# Socket Server

A simplified, robust TCP socket listener with post-processing support.

## Overview

This is a clean, generic socket server.

## Features

- **TCP Socket Server**: Listens for incoming socket connections
- **Post-Processing Support**: Runs external scripts on received messages
- **Robust Logging**: Rotating file logs with configurable levels
- **Connection Management**: Handles multiple concurrent connections with limits
- **Error Handling**: Comprehensive error handling and recovery
- **Threading**: Threaded server for handling multiple connections

## Quick Start

1. **Start the server**:
   ```bash
   ./bin/start_server
   ```

2. **Or use the CLI directly**:
   ```bash
   python cli.py --loglevel=info --logfile=log/socket listen \
       --host=0.0.0.0 \
       --port=15001 \
       --datadir=data \
       --post-processing=bin/postproc_simple.py \
       --max-connections=100
   ```

## Configuration

The server uses command-line arguments for configuration:

- `--host`: Host to bind to (required)
- `--port`: Port to listen on (default: 15001)
- `--datadir`: Directory to save received messages (required)
- `--post-processing`: External script to run on each message (optional)
- `--max-connections`: Maximum concurrent connections (default: 100)
- `--loglevel`: Log level (debug, info, warn, error)
- `--logfile`: Log file path (optional)

## Directory Structure

```
data/
├── inbox/      # Newly received messages
└── archive/    # Successfully processed messages (created by post-processing)
```

## Post-Processing

The server can run external scripts on each received message. The script receives the filename of the saved message as its first argument.

Example post-processing script usage:
```bash
python cli.py listen --host=0.0.0.0 --port=15001 --datadir=./data --post-processing=./bin/postproc
```

## Dependencies

- Python 3.6+
- Click (for CLI)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Files

- `socket_server/server.py` - Main server implementation
- `cli.py` - Command-line interface
- `bin/start_server` - Startup script
- `bin/postproc` - Post-processing script (your existing script)
- `requirements.txt` - Python dependencies
