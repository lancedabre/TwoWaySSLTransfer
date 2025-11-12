import socket
import ssl
import os
import time

# --- Configuration ---
HOST = 'localhost'
PORT = 5000
CERTFILE = 'server.crt' # The server's public certificate
FILE_TO_SEND = 'send.txt'
RESULT_FILE = 'client_result.txt'
BUFFER_SIZE = 4096

def send_file(conn, filepath):
    """
    Sends a file to the server over the socket.
    Protocol: 8 bytes for file size, then the file data.
    """
    try:
        file_size = os.path.getsize(filepath)
        print(f"Sending file: {filepath} (Size: {file_size} bytes)")
        
        # 1. Send the file size
        conn.sendall(file_size.to_bytes(8, 'big'))
        
        # 2. Send the file data
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(data)
                
        print(f"Successfully sent file: {filepath}")
        
    except Exception as e:
        print(f"Error sending file: {e}")

def receive_file(conn, filepath):
    """
    Receives a file from the server over the socket.
    Protocol: 8 bytes for file size, then the file data.
    """
    try:
        # 1. Read the file size (8-byte integer)
        file_size_bytes = conn.recv(8)
        if not file_size_bytes:
            return False # Connection closed
            
        file_size = int.from_bytes(file_size_bytes, 'big')
        print(f"Receiving result file of size: {file_size} bytes")
        
        # 2. Read the file data
        with open(filepath, 'wb') as f:
            remaining = file_size
            while remaining > 0:
                chunk_size = min(BUFFER_SIZE, remaining)
                data = conn.recv(chunk_size)
                if not data:
                    break
                f.write(data)
                remaining -= len(data)
                
        print(f"Successfully received and saved result file: {filepath}")
        return True
        
    except Exception as e:
        print(f"Error receiving file: {e}")
        return False

def main():
    # 0. Check if send.txt exists. If not, create it.
    if not os.path.exists(FILE_TO_SEND):
        print(f"{FILE_TO_SEND} not found. Creating it with example content.")
        with open(FILE_TO_SEND, 'w') as f:
            f.write("usa india usa nepal india pakistan .")
        print(f"{FILE_TO_SEND} created. Please run Client again.")
        return

    # 1. Set up the SSL context
    # We trust the server's self-signed certificate (CERTFILE)
    context = ssl.create_default_context(cafile=CERTFILE)
    context.check_hostname = False # Disable hostname check for self-signed cert
    context.verify_mode = ssl.CERT_REQUIRED # Verify the cert

    try:
        # 2. Create and connect the socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 3. Wrap the socket with SSL *before* connecting
            with context.wrap_socket(sock, server_hostname=HOST) as s_conn:
                s_conn.connect((HOST, PORT))
                print(f"Connected to secure server: {HOST}:{PORT}")
                
                # --- First Transfer: Send file to Server ---
                send_file(s_conn, FILE_TO_SEND)
                
                # --- Second Transfer: Receive file from Server ---
                
                # 4. Wait for user to type 'start'
                print("\nType 'start' to receive the processed file from the server:")
                command = ""
                while command.lower() != 'start':
                    command = input("> ")
                    if command.lower() != 'start':
                        print("Invalid command. Please type 'start'.")
                
                # 5. Send the 'start' command to the server
                s_conn.sendall(b'start')
                print("Sent 'start' command. Waiting for result file...")
                
                # 6. Receive the result file
                receive_file(s_conn, RESULT_FILE)

    except ssl.SSLCertVerificationError:
        print("SSL Certificate Verification Error.")
        print("Did you create the 'server.crt' and 'server.key' files?")
    except ConnectionRefusedError:
        print("Connection refused. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Client shutting down.")

if __name__ == "__main__":
    main()