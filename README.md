# Convert a .feather pointcloud file to a .pcd file

These scripts are specificaly designed for the [Argoverse2 dataset](https://argoverse.github.io/user-guide/datasets/sensor.html).  

## featherToPcd.py

This script converts the .feather files to .pcd files without any modification.  

```bash
python3 featherToPcd.py /path/to/argoverse2/lidar/feather/files/ /output/path/
```

## splitByLaserNumber.py

This script reads the extracted .pcd files of the Argoverse2 dataset and splits them by the LiDARs.  
The `bottom_lidar` is associated to the `laser_number` of 0-31. The `top_lidar` is associated to the `lase_number` >31.  

```bash
python3 splitByLaserNumber.py /path/to/argoverse2/lidar/pcd/files/ /output/path/
```