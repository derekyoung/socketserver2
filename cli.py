#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utilities for Socket Server

This utility provides a simple command-line interface for the socket server
without requiring complex configuration files.
"""

import os
import logging
import logging.handlers

import click

from socket_server.server import runserver

@click.group()
@click.option(
        '--loglevel',
        type=click.Choice(['debug', 'info', 'warn', 'error']),
        default='info')
@click.option('--logfile', default=None)
def main(loglevel, logfile):
    """Utilities for Socket Server communication"""
    # create logger with 'SocketServer'
    logger = logging.getLogger('SocketServer')
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    if logfile is not None:
        # create file handler which logs even debug messages
        fh = logging.handlers.RotatingFileHandler(
              logfile, maxBytes=(1024**2), backupCount=10)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, loglevel.upper()))
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug('Running Socket Server command line.')


@main.command(name='listen')
@click.option('--host', type=click.STRING, required=True,
              help='Host to bind to (e.g., 127.0.0.1 or 0.0.0.0)')
@click.option('--port', type=click.INT, default=15001,
              help='Port to listen on')
@click.option('--datadir', type=click.STRING, required=True,
              help='Directory where incoming messages are saved')
@click.option('--post-processing', type=click.STRING,
              help='External script to run on received messages')
@click.option('--max-connections', type=click.INT, default=100,
              help='Maximum concurrent connections')
def listen(host, port, datadir, post_processing, max_connections):
    """Run server to listen for socket connections and process messages."""
    logger = logging.getLogger('SocketServer')
    logger.info('Starting socket server...')
    
    # Validate host
    if not host:
        logger.critical('Host is required')
        raise click.BadParameter('Host is required')
    
    # Use current directory if datadir not specified
    if not datadir:
        datadir = os.getcwd()
        logger.warning('No datadir specified, using current directory: %s' % datadir)
    
    # Create data directory if it doesn't exist
    if not os.path.exists(datadir):
        logger.info('Creating data directory: %s' % datadir)
        os.makedirs(datadir, exist_ok=True)
    
    logger.info('Server configuration:')
    logger.info('  Host: %s' % host)
    logger.info('  Port: %d' % port)
    logger.info('  Data directory: %s' % datadir)
    logger.info('  Post-processing: %s' % (post_processing or 'None'))
    logger.info('  Max connections: %d' % max_connections)
    
    try:
        runserver(host, port, datadir, post_processing, max_connections)
    except Exception as e:
        logger.error('Server failed to start: %s' % e)
        raise

if __name__ != '__main__':
    pass
else:
    main()

