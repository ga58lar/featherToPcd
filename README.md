# Convert a .feather pointcloud file to a .pcd file

These scripts are specificaly designed for the [Argoverse2 dataset](https://argoverse.github.io/user-guide/datasets/sensor.html).  

<img src="doc/lidarSplitExample.png" width="800px">  

white ... top  
orange ... bottom  

## Download

To clone this repository use:  
`git clone --recursive https://github.com/ga58lar/featherToPcd.git`

## Usage

### featherToPcd.py

This script converts the .feather files to .pcd files without any modification.  

```bash
python3 featherToPcd.py /path/to/argoverse2/lidar/feather/files/ /output/path/
```

### splitByLaserNumber.py

This script reads the extracted .pcd files of the Argoverse2 dataset and splits them by the LiDARs.  
The `bottom_lidar` is associated to the `laser_number` of 0-31. The `top_lidar` is associated to the `lase_number` >31.  

```bash
python3 splitByLaserNumber.py /path/to/argoverse2/lidar/pcd/files/ /output/path/
```

### printFeather.py

Print the content of a .feather file using the av2-api.  

```bash
python3 printFeather.py /path/to/feather/file
```