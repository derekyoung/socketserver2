#!/usr/bin/env python3
import socket
import time

def send_multiline_message(host, port, message):
    """Send a multi-line message to the socket server."""
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Send the multi-line message
        sock.sendall(message.encode('utf-8'))
        
        # Close connection
        sock.close()
        print(f"Sent {len(message)} bytes to {host}:{port}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example multi-line message
    multiline_message = """This is line 1
This is line 2
This is line 3
And this is the final line"""
    
    # Send to your server
    send_multiline_message('127.0.0.1', 15001, multiline_message)
