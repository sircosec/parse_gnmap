#!/usr/bin/python3

import datetime
import argparse
import subprocess
from os import mkdir, path, getcwd

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-if", action='store', required=False, type=str, help="url format input file")
parser.add_argument("--output_dir", "-od", action='store', required=False, type=str, help="output directory: default is ./gobuster/", default="./gobuster/")
parser.add_argument("--timestamp", "-ts", action='store', type=bool, help="timestamp the output files in the name", default=False)
args = parser.parse_args()

input_file = open(args.input_file, 'r')

if not args.output_dir:
    output_dir = args.output_dir
    print(f"[*] the gobuster output subdirectory will be {output_dir}")
    if path.isdir(output_dir) ==False:
        print(f"[*] the gobuster output subdirectory {output_dir} does not exist: creating...")
        try:
            mkdir(output_dir)
        except PermissionError as out_dir_err:
            print(f"[*] the gobuster output subdirectory {output_dir} could not be created! cannot continue.")
            print(f"[-] the error message was: {out_dir_err}")
            exit()
else:
    # check to see if the ./gobuster/ directory exists yet, and create if not
    cwd = getcwd()
    if path.isdir(cwd + "/gobuster/") == False:
        print("[*] the gobuster subdirectory does not yet exist")
        print("[*] creating it now...")
        try:
            mkdir(cwd + "/gobuster/")
        except PermissionError as out_dir_err:
            print(f"[*] the gobuster output subdirectory {output_dir} could not be created! cannot continue.")
            print(f"[-] the error message was: {out_dir_err}")
            exit()
        output_dir = str(cwd) + "/gobuster/"
    else:
        print("[*] the gobuster subdirectory already exists")
        output_dir = str(cwd) + "/gobuster/"

if args.timestamp == True:
    lines = input_file.readlines()
    # count the total number of lines for tracking
    total_count = len(lines)
    # mark the start time for tracking
    starttime = datetime.datetime.now()
    timestamp = starttime.strftime("%Y-%m-%d_%H-%M-%S")
    print(f"\n[*] timestamp is TRUE. output files will be stamped with {timestamp}.")
    # count lines
    count = 1
    for line in lines:
        print(f"[*] server: {line.strip()}")
        # count lines
        print(f"[*] # {count} of {total_count}")
        print(f"[*] starting scan against {len(lines)} targets...")
        host_name = line.split('/')[2].replace(":","_").strip()
        gobuster_output_file_name = output_dir + host_name + "_gobuster_" + timestamp + ".txt"
        print(f"[*] gobuster_output_file: {gobuster_output_file_name}")
        scan_url = line.strip()
        cmd = "/usr/bin/gobuster dir -w /usr/share/wordlists/dirb/big.txt --url " + scan_url + " -o " + gobuster_output_file_name + " -k -r -s '200,204,301,302,307,401,403'"
        print(f"[*] gobuster command: {cmd}\n")
        print("[*] scanning...")
        subprocess.call(cmd, shell=True)
        # get the size of the output file
        gobuster_output_file_name_size = path.getsize(gobuster_output_file_name)
        # print the size of the output file
        print(f"[*] {gobuster_output_file_name} \t\t\t {gobuster_output_file_name_size}\n")
        f = open(gobuster_output_file_name, 'a+')
        f.write("\nending timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        f.close()
        count = count + 1
        timediff = (datetime.datetime.now() - starttime)
        print(f"[*] time elapsed: {timediff}")

else:
    lines = input_file.readlines()
    # count the total number of lines for tracking
    total_count = len(lines)
    # mark the start time for tracking
    starttime = datetime.datetime.now()
    print(f"\n[*] timestamp is FALSE")
    print("[*] WARNING: rerunning the script w/ the same options will cause the output files will be overwritten!")
    count = 1
    for line in lines:
        total_count = len(lines)
        print(f"[*] # {count} of {total_count}")
        # count lines
        print(f"[*] starting scan against {len(lines)} targets...")
        host_name = line.split('/')[2].replace(":","_").strip()
        gobuster_output_file_name = (output_dir + host_name + "_gobuster_" + ".txt")
        print(f"gobuster_output_file: {gobuster_output_file_name}")
        scan_url = line.strip()
        cmd = "/usr/bin/gobuster dir -w /usr/share/wordlists/dirb/big.txt --url " + scan_url + " -o " + gobuster_output_file_name + " -k"
        print(f"cmd: {cmd}\n")
        print("[*] scanning...")
        subprocess.call(cmd, shell=True)
        # get the size of the output file
        gobuster_output_file_name_size = path.getsize(gobuster_output_file_name)
        # print the size of the output file
        print(f"[*] {gobuster_output_file_name} \t\t\t {gobuster_output_file_name_size}\n")
        f = open(gobuster_output_file_name, 'a+')
        f.write("\nending timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        f.close()
        count = count + 1
        timediff = (datetime.datetime.now() - starttime)
        print(f"[*] time elapsed: {timediff}")

print(f"\n[*] done!")