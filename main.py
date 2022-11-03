## This program utilises the kexec program to reboot the system into a new kernel and initrd file after an install, 
## or to quickly reboot into their existing kernel and initrd file.

## Begin Prelaunch Verification
print("Loading...") # Print "Loading..." to the console.

# Importing Required Modules
import os 
from os.path import exists

# Check if user is root
if os.geteuid() != 0: # If the user euid is not 0, then the user is not root, so exit the program.
    print("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.")
    exit("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.") # Exit the program with an error message.

# Check if systemctl is installed
sysctlEnabled = False # Setting sysctlEnabled as a global variable as it will need to be accessed in a function later

if exists("/bin/systemctl") == True:
    # Uses the exists module to check if the systemctl executable is present.
    # It is a kinda hacky solution but I cant be arsed to figure out how to check if a program can run.                                
    print("Package 'systemctl' is installed. Continuing...")
    sysctlEnabled = True # If it is then print to the log and set sysctlEnabled to True.
else:
    print("Package 'systemctl is not present, we will run the kexec command directly instead.")


# Check if kexec is installed
if exists("/bin/kexec") == True: # Uses the exists module to check if the kexec executable is present.
    print("Package 'kexec' is installed. Continuing...") # If it is then print to the log.
else:
    print("Package 'kexec' is not installed. Please install 'kexec-tools' and try again. Exiting.")
    exit("Package 'kexec' is not installed. Please install 'kexec-tools' and try again. Exiting.") # If it is not then exit the program with an error message.


# Create a function to look through users /boot directory for the kernel and initrd files.
def findKernel():
    print("Looking for kernel and initrd files...")
    
    # Looking for regular kernel and initramfs files
    kernelVer = os.popen("uname -r").read() # Get the kernel version
    kernelVer = kernelVer.strip() # Remove the newline character from the end of the string
    kernelFile = "/boot/vmlinuz-" + kernelVer # Create the kernel file path
    initrdFile = "/boot/initrd.img-" + kernelVer + ".img" # Create the initrd file path
    if exists(initrdFile) == False:
        initrdFile = "/boot/initramfs-" + kernelVer + ".img" # If the initrd file doesn't exist, try the other initrd file path
    
    if exists(kernelFile) == True and exists(initrdFile) == True: # If both files exist, then return the kernel and initrd file paths.
        print("Found kernel and initrd files. Continuing...") # Print to the log.
        return kernelFile, initrdFile # Return the kernel and initrd file paths.
    else: # Looking for Linux Zen kernel and initrd files
        kernelFile = "/boot/vmlinuz-linux-zen" # Create the kernel file path
        initrdFile = "/boot/initrd-linux-zen.img" # Create the initrd file path
        if exists(initrdFile) == False:
            initrdFile = "/boot/initramfs-linux-zen.img"
        if exists(kernelFile) == True and exists(initrdFile) == True:
            print("Found kernel and initrd files. Continuing...")
            return kernelFile, initrdFile
        else:
            exit("Yeah this is a really weird bug, if you're seeing this then I've fucked something up and pushed it without testing it, or your system is dead. Please let me know ASAP.") # If it is not then exit the program with an error message.

kernelFile, initrdFile = findKernel() # Return the kernel and initrd file paths to the global scope.

## End Prelaunch Verification

# Begin Main Program

# Create kexec command
kexecCMD = "kexec -l " + kernelFile + " --initrd=" + initrdFile + " --reuse-cmdline" # Create the kexec command and store it in a variable

# User Verification
sel = input("Are you sure you want to reboot? (y/n): ") # Ask the user if they want to reboot
if sel == "y": # If they do, then run the kexec command
    print("Rebooting...") # Print to the log
    if sysctlEnabled == True: # If systemctl is installed, then use systemctl to run the kexec command
        os.system(kexecCMD)
        os.system("systemctl kexec") # Run the kexec command
    else: # If systemctl is not installed, then run the kexec command directly
        os.system(kexecCMD) # Run the kexec command
        os.system("kexec -e") # Run the kexec command
elif sel == "n":
    exit("Exiting.") # If they don't, then exit the program.
else:
    exit("Invalid input. Exiting.")

# End Main Program

# End of File