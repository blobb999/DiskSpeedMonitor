import tkinter as tk
import psutil
import time
import threading
import wmi
import ctypes

class DiskSpeedMonitor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Disk Speed Monitor")
        self.geometry("400x200")

        self.partition_info = self.get_partition_info()
        self.create_labels()
        self.update_speeds()

    def get_volume_label(self, drive_letter):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        buf = ctypes.create_unicode_buffer(1024)
        n = kernel32.GetVolumeInformationW(drive_letter + "\\", buf, 1024, None, None, None, None, 0)

        if n == 0:
            return ""

        return buf.value

    def get_partition_info(self):
        partition_info = {}
        c = wmi.WMI()
        for disk in c.Win32_DiskDrive():
            for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    partition_letter = logical_disk.DeviceID
                    volume_label = self.get_volume_label(partition_letter)
                    partition_info[disk.Index] = f"{partition_letter} ({volume_label})"
        return partition_info

    def create_labels(self):
        self.labels = {}
        for disk_index in self.partition_info.keys():
            disk_name = f"PhysicalDrive{disk_index}"
            label = tk.Label(self, text=f"{self.partition_info[disk_index]}: Read 0 MB/s, Write 0 MB/s")
            label.pack()
            self.labels[disk_name] = label

    def update_speeds(self):
        def get_disk_io_counters():
            disk_io_counters = psutil.disk_io_counters(perdisk=True)
            return {k: (v.read_bytes, v.write_bytes) for k, v in disk_io_counters.items()}

        def monitor_disk_speed(interval=1):
            prev_disk_io_counters = get_disk_io_counters()

            def update_labels():
                current_disk_io_counters = get_disk_io_counters()
                for disk_name, (read_bytes, write_bytes) in current_disk_io_counters.items():
                    if disk_name in prev_disk_io_counters:
                        prev_read_bytes, prev_write_bytes = prev_disk_io_counters[disk_name]
                        read_speed = (read_bytes - prev_read_bytes) / (1024 * 1024) / interval
                        write_speed = (write_bytes - prev_write_bytes) / (1024 * 1024) / interval
                        disk_index = int(disk_name.split("PhysicalDrive")[1])
                        mount_point = self.partition_info.get(disk_index, "N/A")
                        if disk_name not in self.labels:
                            label = tk.Label(self, text=f"{mount_point}: Read 0 MB/s, Write 0 MB/s")
                            label.pack()
                            self.labels[disk_name] = label
                        self.labels[disk_name].config(text=f"{mount_point}: Read {read_speed:.2f} MB/s, Write {write_speed:.2f} MB/s")
                prev_disk_io_counters.update(current_disk_io_counters)
                self.after(int(interval * 1000), update_labels)

            update_labels()

        t = threading.Thread(target=monitor_disk_speed)
        t.daemon = True
        t.start()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    app = DiskSpeedMonitor()
    app.mainloop()

       
