#!/usr/bin/env python3
"""
Send a single line transmission to the socket server.

This script connects to the socket server and sends a single line of data.
"""

import socket
import argparse
import sys
import os


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
    parser.add_argument('message', nargs='?', help='Message to send (single line) - used if -i is not provided')
    parser.add_argument('-i', '--input', help='Input file to read message from')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=15001, help='Server port (default: 15001)')
    
    args = parser.parse_args()
    
    # Determine message source
    if args.input:
        # Read from file
        if not os.path.exists(args.input):
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                message = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.message:
        # Use positional argument
        message = args.message
    else:
        print("Error: Either provide a message as argument or use -i <filename>", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    success = send_single_line(args.host, args.port, message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

