import os
import pandas as pd
import numpy as np
import argparse

def write_pcd(filename, points, intensity, laser_number, offset_ns):
    with open(filename, 'w') as f:
        # Write PCD header
        f.write('# .PCD v0.7 - Point Cloud Data file format\n')
        f.write('VERSION 0.7\n')
        f.write('FIELDS x y z intensity laser_number offset_ns\n')
        f.write('SIZE 4 4 4 4 4 4\n')
        f.write('TYPE F F F F I I\n')
        f.write('COUNT 1 1 1 1 1 1\n')
        f.write(f'WIDTH {points.shape[0]}\n')
        f.write('HEIGHT 1\n')
        f.write('VIEWPOINT 0 0 0 1 0 0 0\n')
        f.write(f'POINTS {points.shape[0]}\n')
        f.write('DATA ascii\n')
        
        # Write data
        for i in range(points.shape[0]):
            f.write(f'{points[i, 0]} {points[i, 1]} {points[i, 2]} {intensity[i]} {laser_number[i]} {offset_ns[i]}\n')

def feather_to_pcd(feather_file, pcd_file):
    # Read the .feather file using pandas
    df = pd.read_feather(feather_file)

    # Ensure the dataframe has the expected columns for a point cloud
    required_columns = ['x', 'y', 'z', 'intensity', 'laser_number', 'offset_ns']
    if not set(required_columns).issubset(df.columns):
        raise ValueError(f"Feather file does not contain the required columns: {required_columns}")

    # Extract the points and other attributes, ensuring they are of the correct type
    points = df[['x', 'y', 'z']].to_numpy().astype(np.float32)
    intensity = df['intensity'].to_numpy().astype(np.float32)
    laser_number = df['laser_number'].to_numpy().astype(np.int32)
    offset_ns = df['offset_ns'].to_numpy().astype(np.int32)

    # Write to PCD file
    write_pcd(pcd_file, points, intensity, laser_number, offset_ns)
    print(f"Converted {feather_file} to {pcd_file}")

def convert_folder(feather_folder, pcd_folder):
    # Ensure the output directory exists
    if not os.path.exists(pcd_folder):
        os.makedirs(pcd_folder)

    # Iterate over all .feather files in the input directory
    for filename in os.listdir(feather_folder):
        if filename.endswith(".feather"):
            feather_file = os.path.join(feather_folder, filename)
            pcd_file = os.path.join(pcd_folder, filename.replace(".feather", ".pcd"))
            feather_to_pcd(feather_file, pcd_file)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert .feather files to .pcd files")
    parser.add_argument("feather_folder", type=str, help="Path to the folder containing .feather files")
    parser.add_argument("pcd_folder", type=str, help="Path to the folder where .pcd files will be saved")
    args = parser.parse_args()

    # Convert all .feather files in the specified folder
    convert_folder(args.feather_folder, args.pcd_folder)
