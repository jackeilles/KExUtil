#KExUtil

KExUtil is made to assist people in their use of the command 'kexec'.

Currently this program is quite limited, and can only handle rebooting to the current running Kernel, however in future, I am planning to implement more features, such as a list of all the kernels that have been installed.

###How it works
This program makes use of the `kexec` command, found in `kexec-utils` to assist in helping people make use of it, it will also make use of `systemctl` to run kexec if it is installed, this way of running kexec is reccomended as it closes programs and running processes gracefully.

###Usage
##### <u>As a dependency, this program requires Python 3.7 or higher.</u>

To use KExUtil, you can clone the git repository by doing 
`git clone https://github.com/ArykDev/KExUtil`.
You can also download the `.tar.gz` file from the releases section of the repo

















This will copy the contents of the repository to the current working directory.

The program must be run with sudo privileges as `kexec` and `systemctl` both require it.

To run the program, use these commands below.
```sh
cd KExUtil
sudo python3 main.py
```

