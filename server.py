import socket
import ssl
import os
from collections import Counter

# --- Configuration ---
HOST = 'localhost'
PORT = 5000
CERTFILE = 'server.crt'
KEYFILE = 'server.key'
RECEIVED_FILE = 'received_from_client.txt'
RESULT_FILE = 'result_for_client.txt'
BUFFER_SIZE = 4096

def process_file(input_path, output_path):
    """
    Reads the input file, counts word frequencies, and writes to the output file.
    """
    print(f"Processing file: {input_path}")
    word_list = []
    
    try:
        # Read the received file
        with open(input_path, 'r') as f:
            content = f.read()
            words = content.split()
            
            # Stop processing at the first '.'
            for word in words:
                if word == '.':
                    break
                word_list.append(word)
                
        # Count word frequencies
        word_counts = Counter(word_list)
        
        # Write results to the output file
        with open(output_path, 'w') as f:
            for word, count in word_counts.items():
                f.write(f"{word}-{count}\n")
                
        print(f"File processed. Results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error processing file: {e}")

def receive_file(conn, filepath):
    """
    Receives a file from the client over the socket.
    Protocol: 8 bytes for file size, then the file data.
    """
    try:
        # 1. Read the file size (8-byte integer)
        file_size_bytes = conn.recv(8)
        if not file_size_bytes:
            return False # Connection closed
            
        file_size = int.from_bytes(file_size_bytes, 'big')
        print(f"Receiving file of size: {file_size} bytes")
        
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
                
        print(f"Successfully received file: {filepath}")
        return True
        
    except Exception as e:
        print(f"Error receiving file: {e}")
        return False

def send_file(conn, filepath):
    """
    Sends a file to the client over the socket.
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

def main():
    # 1. Set up the SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    
    # 2. Create and bind the server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        
        print(f"Secure server listening on {HOST}:{PORT}...")
        
        # 3. Wrap the socket with SSL
        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                try:
                    # 4. Wait for a client connection
                    conn, addr = ssock.accept()
                    with conn:
                        print(f"Client connected: {addr}")
                        
                        # --- First Transfer: Receive file from Client ---
                        if not receive_file(conn, RECEIVED_FILE):
                            print("Client disconnected before file transfer.")
                            continue
                            
                        # 5. Process the received file
                        process_file(RECEIVED_FILE, RESULT_FILE)
                        
                        # 6. Wait for the 'start' command from the client
                        command = conn.recv(1024).decode('utf-8')
                        if "start".lower() in command:
                            print("Client sent 'start' command. Sending result file...")
                            
                            # --- Second Transfer: Send file to Client ---
                            send_file(conn, RESULT_FILE)
                        else:
                            print(f"Unknown command received: {command}")
                            
                except ssl.SSLError as e:
                    print(f"SSL Error: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()