#!/usr/bin/env python3
"""
Decode pseudobinary-c data files to CSV with automatic station name detection.

This script reads pseudobinary-c data files, extracts the station name,
and creates CSV files named after the station and current year.
"""

import argparse
from datetime import datetime
from pseudobinary_c_decoder import PseudobinaryCDecoder


def main():
    """
    Main function to decode pseudobinary-c files with automatic CSV naming.
    """
    parser = argparse.ArgumentParser(description='Decode pseudobinary-c data files to CSV')
    parser.add_argument('input', help='Input file containing pseudobinary-c data')

    args = parser.parse_args()

    # Get current year
    current_year = datetime.now().year

    # Create decoder instance
    decoder = PseudobinaryCDecoder()

    # Read file to extract station name
    data, station_name = decoder.read_file_content(args.input)
    if data is None:
        print("Error: Could not read input file")
        return

    # Generate output filename
    if station_name:
        output_file = f"{station_name}_{current_year}.csv"
        print(f"Station detected: {station_name}")
    else:
        output_file = f"decoded_data_{current_year}.csv"
        print("Warning: No station name found, using default filename")

    # Decode the pseudobinary data
    decoded_data = decoder.decode_pseudobinary_c_tx(data, current_year)
    if not decoded_data:
        print("No data decoded from pseudobinary file")
        return

    # Format the data for CSV
    formatted_data = decoder.format_data_for_csv(decoded_data)
    if not formatted_data:
        print("No formatted data to write")
        return

    # Write to CSV
    success = decoder.write_to_csv(formatted_data, output_file, append_mode=True)

    if success:
        print(f"Successfully created {output_file}")
    else:
        print("Failed to write CSV file")


if __name__ == "__main__":
    main()

