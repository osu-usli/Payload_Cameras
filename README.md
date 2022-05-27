# Payload_Cameras
Payload camera control and vision processing scripts used in finding the direction of the rocket from the launch rail.
## Dependencies:
### Both:
  Opencv,
  numpy,
  os
### usb_pictake.py
  time,
  random,
  newvp,
  serial,
  struct
### newvp.py
  Pillow

## Description:
### usb_pictake.py
Script that runs the control of the cameras on the payload. The script utilizes Opencv video capture objects to take pictures of the surrounding area in a near 360 degree panorama.

### newvp.py
Script that scans the images taken by usb_pictake.py to find the colored tent at the launchrail. The script then scans for an amount of pixels of specific hsv ranges to determine a ratio of color seen on the tent. The four sides of the tent are uniquely colored as to make it possible to determine orientation given a fixed tent rotation.
