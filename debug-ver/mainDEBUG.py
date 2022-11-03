## This is a debug script, therefore kexec will not be run, instead we will print results to the terminal.

## Begin Prelaunch Verification
print("Loading...") # Print "Loading..." to the console.

# Importing Required Modules
import os 
from os.path import exists

# Check if user is root
#if os.geteuid() != 0: # If the user euid is not 0, then the user is not root, so exit the program.
#    print("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.")
#    exit("You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting.") # Exit the program with an error message.
## The root checker is not needed in the debug version as everything we're doing doesn't require root.

# Check if systemctl is installed
sysctlEnabled = False # Setting sysctlEnabled as a global variable as it will need to be accessed in a function later

if exists("/bin/systemctl") == True:
    # Uses the exists module to check if the systemctl executable is present.
    # It is a kinda hacky solution but I cant be arsed to figure out how to check if a program can run.                                
    print("Found Package 'systemctl' at /bin/systemctl. Continuing...") # Print to the log.
    sysctlEnabled = True # If it is then print to the log and set sysctlEnabled to True.
else:
    print("We could not find the file /bin/systemctl. However this is not required for the program to run, so we will continue anyway.") # Print to the log.


# Check if kexec is installed
if exists("/bin/kexec") == True: # Uses the exists module to check if the kexec executable is present.
    print("Found Package 'kexec' at /bin/kexec. Continuing...") # If it is then print to the log.
else:
    print("Package 'kexec' could not be found in /bin. Please install 'kexec-tools' and try again. Exiting.")
    exit("Package 'kexec' is not installed. Please install 'kexec-tools' and try again. Exiting.") # If it is not then exit the program with an error message.


# Create a function to look through users /boot directory for the kernel and initrd files.
def findKernel():
    print("Looking for kernel and initrd files in the /boot directory...") # Print to the log.
    
    # Looking for regular kernel and initramfs files
    kernelVer = os.popen("uname -r").read() # Get the kernel version
    print("Running uname -r returned: " + kernelVer) # Print the kernel version to the log
    kernelVer = kernelVer.strip() # Remove the newline character from the end of the string
    print("Removing the newline character from the kernel version.")
    kernelFile = "/boot/vmlinuz-" + kernelVer # Create the kernel file path
    print("Creating the Kernel File path: " + kernelFile) # Print the kernel file path to the log
    initrdFile = "/boot/initrd.img-" + kernelVer + ".img" # Create the initrd file path
    if exists(initrdFile) == False:
        print("Couldn't find the initrd file. Trying to find the initramfs file instead...")
        initrdFile = "/boot/initramfs-" + kernelVer + ".img" # If the initrd file doesn't exist, try the other initrd file path
    print("Creating the Initrd File path: " + initrdFile) # Print the initrd file path to the log

    
    if exists(kernelFile) == True and exists(initrdFile) == True: # If both files exist, then return the kernel and initrd file paths.
        print("Found " + kernelFile + " and " + initrdFile + ". Continuing...") # Print to the log.
        return kernelFile, initrdFile # Return the kernel and initrd file paths.
    else: # Looking for Linux Zen kernel and initrd files
        print("-----------------------------") # Print to the log.
        print("If you are seeing this message, disregard the above file paths, I'll figure out a way to disable them if they don't exist.")
        kernelFile = "/boot/vmlinuz-linux-zen" # Create the kernel file path
        print("Creating the Kernel File path: " + kernelFile) # Print the kernel file path to the log
        initrdFile = "/boot/initrd-linux-zen.img" # Create the initrd file path
        print("Creating the Initrd File path: " + initrdFile) # Print the initrd file path to the log
        if exists(initrdFile) == False:
            print("Above initrd file doesn't exist. Trying to find the initramfs file instead...")
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
print("Your kexec command is: " + kexecCMD) # Print the kexec command to the log
# User Verification
#sel = input("Are you sure you want to reboot? (y/n): ") # Ask the user if they want to reboot
#if sel == "y": # If they do, then run the kexec command
#    print("Rebooting...") # Print to the log
#    if sysctlEnabled == True: # If systemctl is installed, then use systemctl to run the kexec command
#        os.system(kexecCMD)
#        os.system("systemctl kexec") # Run the kexec command
#    else: # If systemctl is not installed, then run the kexec command directly
#        os.system(kexecCMD) # Run the kexec command
#        os.system("kexec -e") # Run the kexec command
#elif sel == "n":
#    exit("Exiting.") # If they don't, then exit the program.
#else:
#    exit("Invalid input. Exiting.")
## Debug program, we are not rebooting.l

# End Main Program

# End of File