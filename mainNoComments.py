print("Loading...")

import os 
from os.path import exists

if os.geteuid() != 0:
    print("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.")
    exit("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.")


sysctlEnabled = False 

if exists("/bin/systemctl") == True:                            
    print("Package 'systemctl' is installed. Continuing...")
    sysctlEnabled = True
else:
    print("Package 'systemctl is not present, we will run the kexec command directly instead.")


if exists("/bin/kexec") == True: 
    print("Package 'kexec' is installed. Continuing...")
else:
    print("Package 'kexec' is not installed. Please install 'kexec-tools' and try again. Exiting.")
    exit("Package 'kexec' is not installed. Please install 'kexec-tools' and try again. Exiting.")


def findKernel():
    print("Looking for kernel and initrd files...")

    kernelVer = os.popen("uname -r").read()
    kernelVer = kernelVer.strip()
    kernelFile = "/boot/vmlinuz-" + kernelVer
    initrdFile = "/boot/initrd.img-" + kernelVer + ".img"

    if exists(initrdFile) == False:
        initrdFile = "/boot/initramfs-" + kernelVer + ".img"

    if exists(kernelFile) == True and exists(initrdFile) == True:
        print("Found kernel and initrd files. Continuing...")
        return kernelFile, initrdFile
    else:
        kernelFile = "/boot/vmlinuz-linux-zen"
        initrdFile = "/boot/initrd-linux-zen.img"
        if exists(initrdFile) == False:
            initrdFile = "/boot/initramfs-linux-zen.img"
        if exists(kernelFile) == True and exists(initrdFile) == True:
            print("Found kernel and initrd files. Continuing...")
            return kernelFile, initrdFile
        else:
            exit("Yeah this is a really weird bug, if you're seeing this then I've fucked something up and pushed it without testing it, or your system is dead. Please let me know ASAP.") # If it is not then exit the program with an error message.

kernelFile, initrdFile = findKernel()

kexecCMD = "kexec -l " + kernelFile + " --initrd=" + initrdFile + " --reuse-cmdline"

sel = input("Are you sure you want to reboot? (y/n): ")
if sel == "y":
    print("Rebooting...")
    if sysctlEnabled == True:
        os.system(kexecCMD)
        os.system("systemctl kexec")
    else:
        os.system(kexecCMD)
        os.system("kexec -e") 
elif sel == "n":
    exit("Exiting.")
else:
    exit("Invalid input. Exiting.")