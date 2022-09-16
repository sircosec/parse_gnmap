#!/usr/bin/python3

import datetime
import argparse
import subprocess
from os import path, getcwd, mkdir
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-if", action='store', required=True, type=str, help="input file")
parser.add_argument("--output_dir", "-od", action='store', required=False, type=str, help="default output directory: default is ./nikto/", default="./nikto/")
parser.add_argument("--timestamp", "-ts", action='store', type=bool, help="timestamp the output files in the name", default=False)
args = parser.parse_args()

# the input file in url format
input_file = open(args.input_file, 'r')

if not args.output_dir:
    output_dir = args.output_dir
    print(f"[*] the nikto output subdirectory will be {output_dir}")
    if path.isdir(output_dir) ==False:
        print(f"[*] the nikto output subdirectory {output_dir} does not exist: creating...")
        try:
            mkdir(output_dir)
        except PermissionError as out_dir_err:
            print(f"[*] the nikto output subdirectory {output_dir} could not be created! cannot continue.")
            print(f"[-] the error message was: {out_dir_err}")
            exit()
else:
    # check to see if the ./nikto/ directory exists yet, and create if not
    cwd = getcwd()
    if path.isdir(cwd + "/nikto/") == False:
        print("[*] the nikto subdirectory does not yet exist")
        print("[*] creating it now...")
        try:
            mkdir(cwd + "/nikto/")
        except PermissionError as out_dir_err:
            print(f"[*] the nikto output subdirectory {output_dir} could not be created! cannot continue.")
            print(f"[-] the error message was: {out_dir_err}")
            exit()
        output_dir = str(cwd) + "/nikto/"
    else:
        print("[*] the nikto subdirectory already exists")
        output_dir = str(cwd) + "/nikto/"

# run down this path if the timestamp is set to True
if args.timestamp == True:
    # read the input file into 'lines'
    lines = input_file.readlines()
    # count the total number of lines for tracking
    total_count = len(lines)
    print(f"[*] starting scan against {total_count} targets...")
    # capture the current date and time string for use in the output file name
    starttime = datetime.datetime.now()
    timestamp = starttime.strftime("%Y-%m-%d_%H-%M-%S")
    print(f"\n[*] timestamp is TRUE")
    print(f"[*] files will be stamped with {timestamp}")
    # count lines
    count = 1
    # iterate over each line object, feed it to nikto, and capture the output file
    for line in lines:
        # print the count to measure progress
        print(f"[*] # {count} of {total_count}")
        # print the current target
        print(f"[*] url: {line}")
    	# create the nikto output file, ensuring uniqueness (incorporate ip address, port and http|https) including timestamp
        line_split = line.split("://")
        port_split = line_split[1].split(":")
        nikto_output_file_name = "./nikto/" + line_split[0] + "_" + port_split[0] + "_" + port_split[1].strip() + "_" + timestamp + ".txt"
        # run nikto against each line
        cmd = '/usr/bin/nikto -C all -ask auto -host ' + str(line.strip()) + ' -output ' + nikto_output_file_name
        print(f"[*] nikto command: {cmd}\n")
        print("[*] scanning...")
        subprocess.call(cmd, shell=True)
        # get the size of the output file
        nikto_output_file_name_size = path.getsize(nikto_output_file_name)
        # print the size of the output file
        print(f"[*] output file: {nikto_output_file_name} \t\t\t file size: {nikto_output_file_name_size}\n")
        f = open(nikto_output_file_name, 'a+')
        f.write("\nending timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        f.close()
        # increment the count
        count = count + 1
        timediff = (datetime.datetime.now() - starttime)
        print(f"[*] time elapsed: {timediff}")

# run down this path if the timestamp is set to False
else:
	# read the input file into 'lines'
    lines = input_file.readlines()
    # count lines
    print(f"[*] starting scan against {len(lines)} targets...")
    print("\n[*] timestamp is FALSE")
    print(f"[*] files will be named plainly.")
    print("[*] WARNING: rerunning the script w/ the same options will overwrite the output files!")
    # count lines
    count = 1
    # iterate over each line object, feed it to nikto, and capture the output file
    for line in lines:
        # print the count to measure progress
        print(f"[*] # {count} of {total_count}")
        print(f"[*] host:port {line}")
        # create the nikto output file, ensuring uniqueness (incorporate ip address, port and http|https) omitting timestamp
        line_split = line.split("://")
        port_split = line_split[1].split(":")
        nikto_output_file_name = "./nikto/" + line_split[0] + "_" + port_split[0] + "_" + port_split[1] + ".txt"
        cmd = '/usr/bin/nikto -C ALL -ask auto -host ' + str(line.strip()) + ' -output ' + str(nikto_output_file)
        print(f"[*] nikto command: {cmd}\n")
        print("[*] scanning...")
        subprocess.call(cmd, shell=True)
        # get the size of the output file
        nikto_output_file_name_size = path.getsize(nikto_output_file_name)
        # print the size of the output file
        print(f"[*] output file: {nikto_output_file_name} \t\t\t file size: {nikto_output_file_name_size}\n")
        f = open(nikto_output_file_name, 'a+')
        f.write("\nending timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        f.close()
        # increment the count
        count = count + 1
        timediff = (datetime.datetime.now() - starttime)
        print(f"[*] time elapsed: {timediff}")

input_file.close()
print("[*] done!")