# What does it do and why
This program initializes the MegaSync Desktop app and let's it run for a given number of minutes.


I created it as a way of managing my (free) account's storage space better. Fewer versions of the same file make it easier to revert back changes when I need to.
# How to use
Run the main.py file. An additonal file (cache) will be generated by the program.


The program may ask you to specify the Mega .exe path if it cannot find it in its default location. This should only happen once.


The program can take three optional arguments, described below.

The first one is a positional optional argument that specifies the number of minutes the program will run. Adjust it depending on the average time it takes for the app to back up all your files. The default value of minutes is 5 if you don't specify otherwise.

The other arguments' order does not matter:
• You can use '-v' if you want the console to print out information about the execution of the script.
• You can use '-a' if you want the program to prompt you to input the arguments when it runs. You may find this useful if you don't want to run the script everyday or if you'd like to adjust the time manually each time the program runs depending on your changes.

For the second argument you can type 
# How should you use it
I use (and would recommend using) Windows Task Scheduler to run it periodically and automatically.

# System
Tested on Windows 11. Should also work on Windows 10. Not sure about older versions of Windows. Will most likely not work on other OS.