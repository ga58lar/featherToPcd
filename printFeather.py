import argparse
import av2.utils.io as io_utils

def print_file(file_path):
    print(io_utils.read_feather(file_path))

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Print content of .feather file")
    parser.add_argument("feather_file", type=str, help="Path to the .feather file")
    args = parser.parse_args()

    # Convert all .feather files in the specified folder
    print_file(args.feather_file)