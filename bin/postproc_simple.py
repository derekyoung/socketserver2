#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple post-processing script for socket server messages.
Reads incoming data, processes it, and moves to archive directory.
"""

import os
import sys
import shutil
import logging
from datetime import datetime, timezone

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def decode_message(data):
    """
    Decode the incoming message data.
    
    Args:
        data (bytes): Raw message data
        
    Returns:
        dict: Decoded message information
    """
    # TODO: Implement decoding logic here
    # For now, return basic information
    decoded = {
        'raw_data': data,
        'size': len(data),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'message_type': 'unknown',
        'station_id': 'unknown',
        'decoded_content': None
    }
    
    # Basic parsing - extract first few bytes as message type
    if len(data) > 0:
        decoded['message_type'] = chr(data[0]) if data[0] < 128 else 'binary'
    
    # Try to extract station ID if data contains spaces (like in the example)
    try:
        parts = data.split(b' ')
        if len(parts) > 1:
            decoded['station_id'] = parts[1].decode('utf-8', errors='ignore')
    except:
        pass
    
    logger.info(f"Decoded message: type={decoded['message_type']}, "
                f"station={decoded['station_id']}, size={decoded['size']} bytes")
    
    return decoded

def process_message(filepath):
    """
    Process an incoming message file.
    
    Args:
        filepath (str): Path to the message file
    """
    try:
        # Read the message data
        with open(filepath, 'rb') as f:
            data = f.read()
        
        if not data:
            logger.warning(f"Empty message file: {filepath}")
            # Move empty files to a separate directory
            data_dir = os.path.dirname(os.path.dirname(filepath))  # Go up from inbox to data
            empty_dir = os.path.join(data_dir, 'empty')
            os.makedirs(empty_dir, exist_ok=True)
            shutil.move(filepath, empty_dir)
            return
        
        # Decode the message
        decoded = decode_message(data)
        
        # Create archive directory structure
        filename = os.path.basename(filepath)
        timestamp = datetime.now(timezone.utc)
        day_dir = timestamp.strftime('%Y%m%d')
        
        # Create archive directory - use absolute path to avoid relative path issues
        data_dir = os.path.dirname(os.path.dirname(filepath))  # Go up from inbox to data
        archive_dir = os.path.join(data_dir, 'archive', day_dir)
        os.makedirs(archive_dir, exist_ok=True)
        
        # Create processed filename with additional info
        base_name = os.path.splitext(filename)[0]
        processed_name = f"{base_name}_{decoded['message_type']}_{decoded['station_id']}.raw"
        
        # Move to archive
        archive_path = os.path.join(archive_dir, processed_name)
        shutil.move(filepath, archive_path)
        
        logger.info(f"Processed and archived: {filename} -> {archive_path}")
        
        # TODO: Add additional processing here (database storage, notifications, etc.)
        
    except Exception as e:
        logger.error(f"Error processing {filepath}: {e}")
        # Move failed files to error directory
        try:
            data_dir = os.path.dirname(os.path.dirname(filepath))  # Go up from inbox to data
            error_dir = os.path.join(data_dir, 'error')
            os.makedirs(error_dir, exist_ok=True)
            shutil.move(filepath, error_dir)
        except:
            pass
        raise

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        logger.error("Usage: postproc_simple.py <message_file>")
        sys.exit(1)
    
    message_file = sys.argv[1]
    
    if not os.path.exists(message_file):
        logger.error(f"Message file not found: {message_file}")
        sys.exit(1)
    
    logger.info(f"Processing message: {message_file}")
    process_message(message_file)
    logger.info("Processing completed successfully")

if __name__ == '__main__':
    main()
