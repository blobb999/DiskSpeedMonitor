Disk Speed Monitor

Disk Speed Monitor is a simple GUI application that monitors the read and write speeds of your computer's hard disk drives (HDDs) in real time. It uses the psutil library to access disk I/O statistics and the wmi library to get information about the physical drives and logical partitions on your system.

    Monitors read and write speeds for all physical disk drives on your system.
    Displays the drive letter and volume label for each drive.
    Updates the speed readings every second.

License
The Disk Speed Monitor is released under the MIT License. See LICENSE.txt for details.

Acknowledgements
The Disk Speed Monitor was created by blobb999. It uses the following open source libraries:
psutil
wmi
tkinter
ctypes