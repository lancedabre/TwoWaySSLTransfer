A simple, secure, and cross-platform Python application for two-way file transfer and processing using sockets and SSL/TLS.

This project demonstrates a client-server architecture where:

A Client sends a text file (send.txt) to a server.

The Server receives the file, counts the frequency of each word, and saves the results.

The Client can then request the processed file, which the server sends back.

All communication is encrypted.

How It Works (Protocol Flow)

Client                             Server
  |                                  |
  |--- SSL/TLS Handshake ----------> |
  |                                  |
  |--- Send File Size (8 bytes) ---> |
  |--- Send File Data (send.txt) --> |
  |                                  |
  |                                  | <--- Receive & Process File
  |                                  | <--- Save result_for_client.txt
  |                                  |
  |--- Send 'start' command -----> |
  |                                  |
  | <--- Send File Size (8 bytes) --- |
  | <--- Send File Data (result) ---- |
  |                                  |
  |--- Receive & Save result_file.txt |



Features

Secure: All data is encrypted using SSL/TLS, preventing eavesdropping.

Two-Way Transfer: Demonstrates both client-to-server and server-to-client file transfers.

Simple Protocol: Uses a simple [8-byte file size] + [file data] protocol for transfers.

Cross-Platform: Built to run on different operating systems (tested with a macOS client and a Windows server).

Requirements

Python 3.x (Uses standard libraries socket, ssl, os, collections).

openssl (for generating the security certificates).

Setup & Installation

Clone the repository:

git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
cd YourRepoName



Generate Security Certificates:
You must generate a private key and a public certificate for the server. Run this command in your project directory:

openssl req -x509 -newkey rsa:2048 -nodes -keyout server.key -out server.crt -days 365



This will create two files: server.key (your private key) and server.crt (your public certificate).

Prepare the Client File:
The file send.txt is included. You can edit it, but make sure it ends with a space and a period (.) for the word counter to work correctly.

How to Run

You can run this in two modes: on a single machine (localhost) or over a network.

1. Localhost Test (On one machine)

This is the best way to first check that the scripts are working.

Edit client.py:

Change the HOST variable to 'localhost':

HOST = 'localhost'



Start the Server:

Open a terminal and run:

python3 server.py



You should see: Secure server listening on 0.0.0.0:5000...

Run the Client:

Open a second terminal and run:

python3 client.py



It should connect and then ask you to type 'start'.

Type start and press Enter.

Check the Result:

A new file, client_result.txt, will be created in your folder with the word counts.

2. Network Test (On two machines, e.g., macOS Client / Windows Server)

This is the real-world test. It requires network configuration.

On the Server (Windows)

Find your IP Address:

Connect to your network (e.g., your mobile hotspot).

Open Command Prompt (cmd) and type ipconfig.

Find your IPv4 Address (e.g., 172.20.10.9). This is your Server IP.

Edit server.py:

Make sure the HOST variable is set to '0.0.0.0'. This tells it to listen on all available IPs.

HOST = '0.0.0.0'



Configure your Windows Firewall (CRITICAL):
The Windows Firewall will block connections by default, especially on "Public" networks (which a hotspot is). You must create two Inbound rules.

Open "Windows Defender Firewall with Advanced Security" (wf.msc).

Go to "Inbound Rules" -> "New Rule...".

Rule 1: Allow the Python App (Port 5000)

Rule Type: Port

Protocol: TCP

Specific local ports: 5000

Action: Allow the connection

Profile: Check all three boxes: Domain, Private, and Public.

Name: Python App Port 5000

Rule 2: Allow ping (for Testing)

This lets you run the ping test to see if your computers can find each other at all.

Rule Type: Custom

Protocol: Change from "Any" to ICMPv4.

Customize: Select "Specific ICMP types" -> "Echo Request".

Action: Allow the connection

Profile: Check all three boxes: Domain, Private, and Public.

Name: Allow All Ping (ICMPv4-In)

On the Client (macOS)

Copy the Certificate:

Copy the server.crt file from the server machine to your client's project folder. The client needs this to verify the server's identity.

Edit client.py:

Change the HOST variable to match your Server IP.

HOST = '172.20.10.9' # <-- Use your server's actual IP here



Run the Test

Server (Windows): Run python3 server.py.

Client (macOS): Open a terminal. First, test connectivity:

ping 172.20.10.9  # <-- Use your server's IP



If you get Reply from..., your firewall rules are working!

Client (macOS): Now run the app:

python3 client.py



It should connect. Type start to complete the transfer.

License

This project is licensed under the MIT License. See the LICENSE file for details.
