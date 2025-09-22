# Socket Server

A simplified, robust TCP socket listener with post-processing support.

## Overview

This is a cleaned-up version of a socket server that was originally based on an Iridium DirectIP listener. All DirectIP/Iridium-specific code has been removed, leaving a clean, generic socket server.

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
   python3 cli.py --loglevel=info --logfile=log/socket listen \
       --host=128.171.46.213 \
       --port=15001 \
       --datadir=data \
       --post-processing=bin/postproc2 \
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
python3 cli.py listen --host=0.0.0.0 --port=15001 --datadir=./data --post-processing=./bin/postproc2
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
- `bin/postproc2` - Post-processing script (your existing script)
- `requirements.txt` - Python dependencies

## Migration Notes

This server replaces the original DirectIP-based implementation. All functionality is preserved:

- Same data directory structure
- Same post-processing script interface
- Same log file format
- Same command-line interface (with additional options)

The main difference is that the code is now clean and free of DirectIP/Iridium-specific references, making it much easier to understand and maintain.
