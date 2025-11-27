# sick_safetyscanners2_interfaces

**パス**: `triorb_sensor/sick/sick_safetyscanners2_interfaces`  
**説明**: Interfaces for the sick_safetyscanners ros2 driver

## sick_safetyscanners2_interfaces
Interfaces for the sick_safetyscanners ros2 driver

## SICK Safetyscanner ROS2 Interfaces

This package contains the necessary interfaces used for the ROS2 driver for the SICK Safetyscanners.

It includes message and service definitions for:
* Extended Laser Scan
  * Includes detected reflectors.
* Output Paths
  * Gives the status if the currently configured output paths. 
* Raw Data
  * Gives all data currently provided by the sensor for further processing.
* Field Data
  * A service returning the protective and warning field geometries with a mapping to the respective
    output paths.

