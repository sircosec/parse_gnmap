#!/usr/bin/python3
#jconsole_parse.py
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-if", action='store', required=True, type=str, help="input file format: 'host:port' one per line.")
args = parser.parse_args()

input_file = open(args.input_file, 'r+')

lines = input_file.readlines()

print("\n[*] simple looping script for running jconsole against a whole lot of servers")
print("\n[*] if authentication fails, you have to manually close the jconsole windows!")

for line in lines:
	cmd = f"jconsole {line.strip()}"
	print(f"[*] current host: {line.strip()}")
	subprocess.call(cmd, shell=True)

print("\n[*] done!")