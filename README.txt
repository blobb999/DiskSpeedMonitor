Disk Speed Monitor

Disk Speed Monitor is a simple GUI application that monitors the read and write speeds of your computer's hard disk drives (HDDs) in real time. It uses the psutil library to access disk I/O statistics and the wmi library to get information about the physical drives and logical partitions on your system.

    Monitors read and write speeds for all physical disk drives on your system.
    Displays the drive letter and volume label for each drive.
    Updates the speed readings every second.

License
The Disk Speed Monitor is released under the MIT License.

Acknowledgements
The Disk Speed Monitor was created by blobb999. It uses the following open source libraries:
psutil
wmi
tkinter
ctypes

Known Issue:
psutils cant determ drive letters and volume labels of encrypted and mounted drives. Finding a workarround is in progress...
1. pyveracrypt discontinued.
2. no volume label with cmd "wmic logicaldisk get deviceid, volumename, description"
3. no volume label with module subprocess
4. no volume label with cmd "vol x:"