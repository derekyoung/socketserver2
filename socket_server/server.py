# -*- coding: utf-8 -*-

"""
TCP Socket server to receive socket messages.
A simplified, generic socket listener with post-processing support.
"""

from datetime import datetime
import socket
import os.path
import logging
import subprocess
import threading
import signal
import sys
try:
    import socketserver
except:
    import SocketServer as socketserver

module_logger = logging.getLogger('SocketServer')

def save_raw_msg(outputdir, client_address, data, timestamp):
    """Save incoming message to file with timestamp and client address."""
    inbox_dir = os.path.join(outputdir, 'inbox')
    if not os.path.isdir(inbox_dir):
        os.makedirs(inbox_dir, exist_ok=True)
    
    filename = os.path.join(
        inbox_dir, 
        "%s_%s.raw" % (
            timestamp.strftime('%Y%m%d%H%M%S%f'), 
            client_address[0].replace('.', '_')
        )
    )
    
    module_logger.debug('Saving message: %s' % filename)
    with open(filename, 'wb') as f:
        f.write(data)
    module_logger.debug("Saved: %s" % filename)
    return filename


class SocketHandler(socketserver.BaseRequestHandler):
    """A request handler for each socket connection.
    
    Handles individual client connections, receives data, saves it to file,
    and optionally runs post-processing scripts.
    """
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('SocketServer.Handler')
        self.logger.debug('Initializing SocketHandler')
        socketserver.BaseRequestHandler.__init__(
                self, request, client_address, server)

    def handle(self):
        """Handle incoming socket connection and process message."""
        try:
            # Set connection timeout
            self.request.settimeout(30)
            
            self.logger.info('Connection from %s' % self.client_address[0])
            timestamp = datetime.utcnow()
            
            # Receive data from client
            data = self.request.recv(2048)
            if not data:
                self.logger.warning('Empty message from %s' % self.client_address[0])
                return
                
            self.logger.info('Received %d bytes from %s' % (len(data), self.client_address[0]))
            
            # Save message to file
            filename = save_raw_msg(
                self.server.datadir, self.client_address, data, timestamp)
            
            # Run post-processing if configured
            if self.server.postProcessing is not None:
                self.logger.debug('Running post-processing: %s' % self.server.postProcessing)
                try:
                    result = subprocess.run(
                        [self.server.postProcessing, filename],
                        timeout=60,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    self.logger.debug('Post-processing successful: %s' % result.stdout)
                except subprocess.TimeoutExpired:
                    self.logger.error('Post-processing timeout for %s' % filename)
                except subprocess.CalledProcessError as e:
                    self.logger.error('Post-processing failed: %s' % e.stderr)
                except Exception as e:
                    self.logger.error('Post-processing error: %s' % e)
                    
        except socket.timeout:
            self.logger.warning('Connection timeout from %s' % self.client_address[0])
        except Exception as e:
            self.logger.error('Error handling connection from %s: %s' % (self.client_address[0], e))
        finally:
            self.logger.debug('Connection from %s closed' % self.client_address[0])


class SocketServer(socketserver.TCPServer):
    """A TCP server for receiving socket messages with post-processing support."""
    
    def __init__(self, server_address, datadir, postProcessing=None, max_connections=100):
        self.logger = logging.getLogger('SocketServer')
        self.logger.debug('Initializing SocketServer')
        
        # Validate and set data directory
        if not os.path.exists(datadir):
            self.logger.critical('Data directory does not exist: %s' % datadir)
            raise ValueError('Data directory does not exist: %s' % datadir)
        self.datadir = datadir
        self.logger.info('Data directory: %s' % datadir)
        
        # Validate post-processing script if provided
        if postProcessing is not None and not os.path.exists(postProcessing):
            self.logger.error('Post-processing script not found: %s' % postProcessing)
            raise ValueError('Post-processing script not found: %s' % postProcessing)
        self.postProcessing = postProcessing
        
        # Set connection limits
        self.max_connections = max_connections
        self.active_connections = 0
        
        # Initialize the TCP server
        socketserver.TCPServer.__init__(
            self, server_address, RequestHandlerClass=SocketHandler)
        
        # Allow address reuse for quick restarts
        self.allow_reuse_address = True

    def verify_request(self, request, client_address):
        """Verify incoming connection request."""
        self.logger.debug('Connection request from %s' % client_address[0])
        
        # Check connection limit
        if self.active_connections >= self.max_connections:
            self.logger.warning('Max connections reached, rejecting %s' % client_address[0])
            return False
            
        self.active_connections += 1
        return True
    
    def finish_request(self, request, client_address):
        """Called when a request has been processed."""
        self.active_connections -= 1
        super().finish_request(request, client_address)


class ThreadedSocketServer(socketserver.ThreadingMixIn, SocketServer):
    """Threaded version of SocketServer for handling multiple concurrent connections."""
    pass


def runserver(host, port, datadir, postProcessing=None, max_connections=100):
    """Run a socket server to listen for messages.

    Args:
        host (str): Host to bind to (e.g., '127.0.0.1' or '0.0.0.0')
        port (int): Port to listen on (e.g., 15001)
        datadir (str): Directory to save received messages
        postProcessing (str): Optional script to run on each received message
        max_connections (int): Maximum concurrent connections (default: 100)
    """
    module_logger.info('Starting socket server...')
    
    try:
        server = ThreadedSocketServer(
            (host, port), 
            datadir, 
            postProcessing, 
            max_connections
        )
        module_logger.info('Server listening on %s:%s' % (host, port))
        module_logger.info('Data directory: %s' % datadir)
        if postProcessing:
            module_logger.info('Post-processing: %s' % postProcessing)
        module_logger.info('Max connections: %d' % max_connections)
        module_logger.info('Press Ctrl-C to stop the server')
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        module_logger.info('Server shutdown requested by user')
    except Exception as e:
        module_logger.error('Server error: %s' % e)
        raise
    finally:
        module_logger.info('Server stopped')


def main():
    """Main entry point for running the server directly."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Socket Server')
    parser.add_argument('--host', required=True, help='Host to bind to')
    parser.add_argument('--port', type=int, required=True, help='Port to listen on')
    parser.add_argument('--datadir', required=True, help='Data directory')
    parser.add_argument('--post-processing', help='Post-processing script')
    parser.add_argument('--max-connections', type=int, default=100, 
                       help='Maximum concurrent connections')
    
    args = parser.parse_args()
    
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    runserver(
        args.host, 
        args.port, 
        args.datadir, 
        args.post_processing,
        args.max_connections
    )


if __name__ == '__main__':
    main()
