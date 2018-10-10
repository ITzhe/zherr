import os

disk_dic = {}      #save disk's size

disk = os.popen("/usr/bin/inxi -D|grep '/dev/sd' |awk '{print $2}'").read().split()


def disk_info():
    disk_size = "inxi -D|grep %s |awk '{print $(NF-2)}'"
    disk_type = "inxi -D|grep %s |awk '{print $7}'"

    for i in disk:
	d_size = os.popen(disk_size % (i)).read().strip() + " GB"
	d_type = os.popen(disk_type % (i)).read().strip()
        disk_dic[i] = (d_size,d_type)
    return disk_dic
