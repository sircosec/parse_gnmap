#!/usr/bin/python3

from re import compile
from sys import exit
import datetime
import argparse
from os import mkdir, path, getcwd

''' takes a .gnmap input file and extracts web-based services
 and tees them up for other tools like gobuster and nikto.
 creates a subdirectory for each protocol that it handles
 to keep from overrunning the current directory.'''

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-if", action='store', required=True, type=str, help=".gnmap input file")
parser.add_argument("--timestamp", "-ts", action='store', type=bool, help="timestamp the output files in the name", default=False)
args = parser.parse_args()

# pattern for re to extract an IP address
pattern = compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# .gnmap input file
input_file = open(args.input_file, 'r+')

# organize the input file into lines so they can be read individually
lines = input_file.readlines()
#print(lines)

# validate that the input file is a .gnmap file
if ".gnmap" not in input_file:
    print(f"\n[*] input file is {input_file.name}")
else:
    print("\n[*] input file is not a .gnmap!")
    exit()

''' identify the current working directory. if we do it this way 
then the script can be run from /usr/bin/ rather that copying
it to the local folder.'''

cwd = getcwd()

# check for the existance of the subdirectories
# create them in the local directory if they don't exist already
if path.isdir(cwd + "/http/") == False:
    mkdir(cwd + "/http/")
if path.isdir(cwd + "/ssl/") == False:
    mkdir(cwd + "/ssl/")
if path.isdir(cwd + "/smb") == False:
    mkdir(cwd + "/smb")
if path.isdir(cwd + "/ssh") == False:
    mkdir(cwd + "/ssh")
if path.isdir(cwd + "/javarmi") == False:
    mkdir(cwd + "/javarmi")
if path.isdir(cwd + "/snmp") == False:
    mkdir(cwd + "/snmp")

# run down this path if 'timestamp' is set to true
if args.timestamp == True:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"\n[*] timestamp is TRUE. files will be stamped with: {timestamp}\n")
    http_output_file = open("./http/http_file_" + timestamp + ".txt", 'w+')
    # ssl/tls/https output file with h:port only
    ssl_output_file = open("./ssl/ssl_file_" + timestamp + ".txt", 'w+')
    # ssl/tls/https output file with https:// prepended
    url_ssl_output_file = open("./ssl/url_ssl_file_" + timestamp + ".txt", 'w+')
    # http output file with http:// prepended
    url_http_output_file = open("./http/url_http_file_" + timestamp + ".txt", 'w+')
    # smb output file
    smb_output_file = open("./smb/smb_out_" + timestamp + ".txt", 'w+')
    # ssh output file
    ssh_output_file = open("./ssh/ssh_out_" + timestamp + ".txt", 'w+')
    # javarmi output file
    javarmi_output_file = open("./javarmi/javarmi_out_" + timestamp + ".txt", 'w+')
    # snmp output file
    snmp_output_file = open("./snmp/snmp_out_" + timestamp + ".txt", 'w+')

# run down this path if 'timestamp' is set to false
else:
    print("\n[*] timestamp is FALSE. files will be named plainly.\n")
    print("[*] WARNING: rerunning the script w/ the same options will overwrite the output files!\n")
    http_output_file = open("./http/http_out.txt", 'w+')
    # ssl/tls/https output file with h:port only
    ssl_output_file = open("./ssl/ssl_out.txt", 'w+')
    # ssl/tls/https output file with https:// prepended
    url_ssl_output_file = open("./ssl/url_ssl_out.txt", 'w+')
    # http output file with http:// prepended
    url_http_output_file = open("./http/url_http_out.txt", 'w+')
    # smb output file
    smb_output_file = open("./smb/smb_out.txt", 'w+')
    # ssh output file
    ssh_output_file = open("./ssh/ssh_out.txt", 'w+')
    # javarmi output file
    javarmi_output_file = open("./javarmi/javarmi_out.txt", 'w+')
    # snmp output file
    snmp_output_file = open("./snmp/snmp_out.txt", 'w+')

# list objects for sorting and collecting the different protocols
http_output_servers = []
ssl_output_servers = []
smb_output_servers = []
ssh_output_servers = []
snmp_output_servers = []
javarmi_output_servers = []

# iterate over the list object, sort out the http servers, capturing each individual port
for line in lines:
    #print(line)
    # operate on lines containing 'http'
    if '//http//' in line:
        #print(line)
        # extract the IP address at the beginning of the line for the output object
        host = pattern.search(line)
        # collect each individual port that matches http into another list
        ports_array = []
        # extract only the part of the line that has the ports in it
        port_split = line.split('Ports: ')
        # split the port objects up using the comma
        ports = port_split[1].split(',')
        # iterate over each port and extract the numerical value
        for port in ports:
            # operate only on the port objects that contain 'http'
            if '//http//' in port:
                # split the object along the forward slashes to separate
                split_port = port.split('/')
                # strip leading spaces
                ports_array.append(split_port[0].strip())
        # construct a new object using the h (ip address) and a list object containing all the ports
        new_host = [host[0], ports_array]
        # append each object to a master list
        http_output_servers.append(new_host)

# iterate over the http server objects, format the output strings with h:port
for http_server_object in http_output_servers:
    # for each port, create a new object containing the h (ip address) and port separated by a colon
    for port in http_server_object[1]:
        # construct a string containing the IP address colon (:) port
        server_string = http_server_object[0] + ":" + port
        #print(f"server_string: {server_string}")
        # write out the new string into the output file
        http_output_file.write(server_string + '\n')
        # write out the same string prepended with 'http://'
        url_http_output_file.write("http://" + server_string + '\n')

# run it back, doing the same thing for 'ssl' servers
for line in lines:
    # operate on lines containing 'ssl'
    if '//ssl' in line:
        # extract the IP address at the beginning of the line
        host = pattern.search(line)
        ports_array = []
        port_split = line.split('Ports: ')
        ports = port_split[1].split(',')
        for port in ports:
            if '//ssl' in port:
                split_port = port.split('/')
                ports_array.append(split_port[0].strip())
        new_host = [host[0], ports_array]
        ssl_output_servers.append(new_host)

# for each ssl port, create a new object containing the h (ip address) and port separated by a colon
for ssl_output_server in ssl_output_servers:
    for port in ssl_output_server[1]:
        '''there's a quirky name conflict with the nmap output where 3389/rdp shows up as ssl (because it 
        rides ssl) this 'if' statement keeps 3389/rdp results from being written into the regular ssl file 
        which is intended for web servers. thanks microsoft.'''
        if port == "3389":
            pass
        else:
            server_string = ssl_output_server[0] + ":" + port
            ssl_output_file.write(server_string + '\n')
            url_ssl_output_file.write("https://" + server_string + '\n')

# this time sort out the java-rmi servers
for line in lines:
    # operate on lines containing 'http'
    if '//java-rmi//' in line:
        # extract the IP address at the beginning of the line for the output object
        host = pattern.search(line)
        # collect each individual port that matches http into another list
        ports_array = []
        # extract only the part of the line that has the ports in it
        port_split = line.split('Ports: ')
        # split the port objects up using the comma
        ports = port_split[1].split(',')
        # iterate over each port and extract the numerical value
        for port in ports:
            # operate only on the port objects that contain 'http'
            if '//java-rmi//' in port:
                # split the object along the forward slashes to separate
                split_port = port.split('/')
                # strip leading spaces
                ports_array.append(split_port[0].strip())
        # construct a new object using the h (ip address) and a list object containing all the ports
        new_host = [host[0], ports_array]
        # append each object to a master list
        javarmi_output_servers.append(new_host)

# for each java-rmi port, create a new object containing the h (ip address) and port separated by a colon for jconsole
for javarmi_server_object in javarmi_output_servers:
    # for each port, create a new object containing the h (ip address) and port separated by a colon
    for port in http_server_object[1]:
        # construct a string containing the IP address colon (:) port
        server_string = javarmi_server_object[0] + ":" + port
        # write out the new string into the output file
        javarmi_output_file.write(server_string + '\n')
        # write out the same string prepended with 'http://'
        javarmi_output_file.write(server_string + '\n')

# while we're at it, sort out smb, ssh, and snmp provided they are running on standard ports
for line in lines:
    if '/microsoft-ds?/' in line:
        host = pattern.search(line)
        smb_output_file.write(host[0] + '\n')
    if '//ssh//' in line:
        #print(line)
        host = pattern.search(line)
        ssh_output_file.write(host[0] + '\n')
    if '//snmp?/' in line:
        host = pattern.search(line)
        snmp_output_file.write(host[0] + '\n')

# clean up the output files
input_file.close()
ssl_output_file.close()
http_output_file.close()
url_ssl_output_file.close()
url_http_output_file.close()
javarmi_output_file.close()
smb_output_file.close()
ssh_output_file.close()
snmp_output_file.close()

# gather the sizes of the output files
http_output_file_size = path.getsize(http_output_file.name)
ssl_output_file_size = path.getsize(ssl_output_file.name)
url_http_output_file_size = path.getsize(url_http_output_file.name)
url_ssl_output_file_size = path.getsize(url_ssl_output_file.name)
javarmi_output_file_size = path.getsize(javarmi_output_file.name)
smb_output_file_size = path.getsize(smb_output_file.name)

ssh_output_file_size = path.getsize(ssh_output_file.name)
snmp_output_file_size = path.getsize(snmp_output_file.name)

print(f"{http_output_file.name} \t\t\t {http_output_file_size}")
print(f"{ssl_output_file.name} \t\t\t\t {ssl_output_file_size}")
print(f"{url_http_output_file.name} \t\t\t {url_http_output_file_size}")
print(f"{url_ssl_output_file.name} \t\t\t {url_ssl_output_file_size}")
print(f"{javarmi_output_file.name} \t\t\t {javarmi_output_file_size}")
print(f"{smb_output_file.name} \t\t\t\t {smb_output_file_size}")
print(f"{ssh_output_file.name} \t\t\t\t {ssh_output_file_size}")
print(f"{snmp_output_file.name} \t\t\t {snmp_output_file_size}")

# list out the output files with bytecount to see what popped

print("\n[*] done!")
