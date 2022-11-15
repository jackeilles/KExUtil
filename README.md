<h1>KExUtil</h1>

KExUtil is made to assist people in their use of the command 'kexec'.

Currently this program is quite limited, and can only handle rebooting to the current running Kernel, however in future, I am planning to implement more features, such as a list of all the kernels that have been installed.

<h3>How it works</h3>
This program makes use of the `kexec` command, found in `kexec-utils` to assist in helping people make use of it, it will also make use of `systemctl` to run kexec if it is installed, this way of running kexec is reccomended as it closes programs and running processes gracefully.

<h3>Usage</h3>
<b><u>As a dependency, this program requires Python 3.7 or higher.</u></b>

To use KExUtil, you can clone the git repo by doing 
`git clone https://github.com/ArykDev/KExUtil`.
You can also download the `.tar.gz` file from the releases section of the repo.

This will copy the contents of the repository to the current working directory.

The program must be run with sudo privileges as `kexec` and `systemctl` both require it.

To run the program, use these commands below.

```sh
cd KExUtil
sudo python3 main.py
```

<h3>Versions</h3>
You may have noticed that there are 3 versions of the program.

The version held in the folder named 'debug-ver' is a version made for debugging the program, it has higher verbosity and does not actually execute the commands, and instead prints them to the terminal.

The mainNoComments.py version is going to be used for creating an executable version, not entirely sure why I've added this but oh well.

The main version is main.py, the mainNoComments is the exact same as the main file, if edits are going to be made, please also edit the mainNoComments file accordingly.
