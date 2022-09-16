#!/usr/bin/python3

import datetime
import argparse
import subprocess
from os import path, getcwd, mkdir

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-if", action='store', required=True, type=str, help="input file format: 'host:port' one per line")
parser.add_argument("--output_dir", "-od", action='store', required=False, type=str, help="output directory: default is ./gobuster/", default="./gobuster/")
parser.add_argument("--timestamp", "-ts", action='store', type=bool, help="timestamp the output files in the name", default=False)
args = parser.parse_args()

input_file = open(args.input_file, 'r')

if args.output_dir:
    output_dir = args.output_dir
    print(f"[*] the sslscan output subdirectory will be {output_dir}")
else:
    # check to see if the ./sslscan/ directory exists yet, and create if not
    cwd = getcwd()
    if path.isdir(cwd + "/sslscan/") == False:
        print("[*] the sslscan subdirectory does not yet exist")
        print("[*] creating it now...")
        mkdir(cwd + "/sslscan/")
        output_dir = str(cwd) + "/sslscan/"
    else:
        print("[*] the sslscan subdirectory already exists")
        output_dir = str(cwd) + "/sslscan/"

if args.timestamp == True:
    # read the input file into 'lines'
    lines = input_file.readlines()
    # count the total number of lines for tracking
    total_count = len(lines)
    # capture the current date and time string for use in the output file name
    starttime = datetime.datetime.now()
    timestamp = starttime.strftime("%Y-%m-%d_%H-%M-%S")
    print(f"\n[*] timestamp is TRUE") 
    print(f"[*] files will be stamped with {timestamp}")
    # count lines
    count = 1
    # read the input file into 'lines'
    for line in lines:
        print(f"[*] server: {line.strip()}")
        print(f"[*] # {count} of {total_count}")
        # split the host:port string for output file naming uniqueness
        line_split = line.split(":")
        # split the host:port string, concatenate the protocol, host, port, and timestamp into the file name for uniqueness
        sslscan_output_file_name = (output_dir + line_split[0].strip() + "_" + line_split[1].strip() + "_sslscan_" + timestamp + ".txt").strip()
        # call sslscan and write the results to the output file
        cmd = '/usr/bin/sslscan ' + str(line.strip()) + ' > ' + sslscan_output_file_name
        print(f"[*] sslscan cmd: {cmd}\n")
        print("[*] scanning...")
        subprocess.call(cmd, shell=True)
        # get the size of the output file
        sslscan_output_file_name_size = path.getsize(sslscan_output_file_name)
        # print the size of the output file
        print(f"[*] output file: {sslscan_output_file_name} \t\t\t file size: {sslscan_output_file_name_size}\n")
        f = open(sslscan_output_file_name, 'a+')
        f.write("\nending timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        f.close()
        # increment the count
        count = count + 1
        timediff = (datetime.datetime.now() - starttime)
        print(f"[*] time elapsed: {timediff}")

else:
    # read the input file into 'lines'
    lines = input_file.readlines()
    print("\n[*] timestamp is FALSE")
    print(f"[*] files will be named plainly")
    print("[*] WARNING: rerunning the script w/ the same options will overwrite the output files!")
    
    # read the input file into 'lines'
    for line in lines:
        print(f"[*] server: {line}")
        # split the host:port string, concatenate the protocol, host, and port into the file name
        sslscan_output_file_name = (output_dir + line_split[0].strip() + "_" + line_split[1].strip() + "_sslscan_" + ".txt").strip()
        # call sslscan and write the results to the output file
        cmd = '/usr/bin/sslscan ' + str(line.strip()) + ' > ' + sslscan_output_file_name
        print(f"[*] sslscan cmd: {cmd}\n")
        print("[*] scanning...")
        subprocess.call(cmd, shell=True)
        # get the size of the output file
        sslscan_output_file_name_size = path.getsize(sslscan_output_file_name)
        # print the size of the output file
        print(f"[*] output file: {sslscan_output_file_name} \t\t\t file size: {sslscan_output_file_name_size}\n")
        f = open(sslscan_output_file_name, 'a+')
        f.write("\nending timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        f.close()
        # increment the count
        count = count + 1
        timediff = (datetime.datetime.now() - starttime)
        print(f"[*] time elapsed: {timediff}")

input_file.close()
print("[*] done!")