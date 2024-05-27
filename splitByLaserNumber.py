import os
import numpy as np
import open3d as o3d
import argparse

def read_custom_fields(pcd_file):
    # Read the PCD file to extract custom fields
    with open(pcd_file, 'r') as f:
        lines = f.readlines()
        fields = None
        for line in lines:
            if line.startswith('FIELDS'):
                fields = line.strip().split()[1:]
                break

    if not fields:
        raise ValueError(f"No custom fields found in {pcd_file}")

    field_indices = {field: index for index, field in enumerate(fields)}

    # Read data section and extract custom fields
    data_start = lines.index('DATA ascii\n') + 1
    data_lines = [line.split() for line in lines[data_start:]]
    data_array = np.array(data_lines).astype(np.float32)

    custom_fields = {}
    for field, index in field_indices.items():
        custom_fields[field] = data_array[:, index]

    return custom_fields

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

def split_point_cloud_by_laser_number(pcd_file, output_folder):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(pcd_file)

    # Read custom fields
    custom_fields = read_custom_fields(pcd_file)

    # Extract custom fields
    intensity = custom_fields['intensity']
    laser_number = custom_fields['laser_number'].astype(np.int32)
    offset_ns = custom_fields['offset_ns'].astype(np.int32)

    # Split points by laser_number
    mask_bottom = laser_number <= 31
    mask_top = laser_number > 31

    points_bottom = np.asarray(pcd.points)[mask_bottom]
    points_top = np.asarray(pcd.points)[mask_top]

    # Save the new point clouds
    base_filename = os.path.basename(pcd_file).replace('.pcd', '')
    output_bottom_file = os.path.join(output_folder, f"{base_filename}_bottom.pcd")
    output_top_file = os.path.join(output_folder, f"{base_filename}_top.pcd")

    write_pcd(output_bottom_file, points_bottom, intensity[mask_bottom], laser_number[mask_bottom], offset_ns[mask_bottom])
    write_pcd(output_top_file, points_top, intensity[mask_top], laser_number[mask_top], offset_ns[mask_top])
    
    print(f"Saved {output_bottom_file} and {output_top_file}")

def split_pcds_in_folder(input_folder, output_folder):
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all .pcd files in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith(".pcd") and not filename.endswith("_bottom.pcd") and not filename.endswith("_top.pcd"):
            pcd_file = os.path.join(input_folder, filename)
            split_point_cloud_by_laser_number(pcd_file, output_folder)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Split PCD files by laser_number field")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing .pcd files")
    parser.add_argument("output_folder", type=str, help="Path to the folder where split .pcd files will be saved")
    args = parser.parse_args()

    # Split all .pcd files in the specified folder
    split_pcds_in_folder(args.input_folder, args.output_folder)
