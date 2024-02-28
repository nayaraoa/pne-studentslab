import socket

def main():
    HOST = '127.0.0.1'
    PORT = 8081

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))

    server_socket.listen(1)

    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            client_conn, client_addr = server_socket.accept()
            print(f"Connection established with {client_addr}")

            data = client_conn.recv(1024).decode('utf-8')
            print(f"Received data from client: {data}")

            client_conn.sendall(data.encode('utf-8'))

            client_conn.close()
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    main()