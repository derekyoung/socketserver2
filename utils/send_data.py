#!/usr/bin/env python3
"""
Send a single line transmission to the socket server.

This script connects to the socket server and sends a single line of data.
"""

import socket
import argparse
import sys


def send_single_line(host, port, message):
    """Send a single line message to the socket server."""
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Send the single line message
        # Ensure it's a single line by removing newlines and adding one at the end
        line = message.rstrip('\n\r') + '\n'
        sock.sendall(line.encode('utf-8'))
        
        # Close connection
        sock.close()
        print(f"Sent {len(line)} bytes to {host}:{port}")
        return True
        
    except socket.error as e:
        print(f"Socket error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def main():
    """Main function to send a single line transmission."""
    parser = argparse.ArgumentParser(description='Send a single line transmission to the socket server')
    parser.add_argument('message', help='Message to send (single line)')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=15001, help='Server port (default: 15001)')
    
    args = parser.parse_args()
    
    success = send_single_line(args.host, args.port, args.message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

