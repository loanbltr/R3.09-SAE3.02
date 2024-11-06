import socket
host = "localhost"

def sock_main():
    server_socket = socket.socket()
    print("Socket created")
    server_socket.bind((host, 8080))
    print("Socket bind complete")
    server_socket.listen(1)
    print("Socket now listening")
    while True:
        conn, address = server_socket.accept()
        print("Got connection from", address)
        message = conn.recv(1024).decode()
        print(f"MESSAGE DU CLIENT: {message}")
        if message == "arret":
            conn.close()
            server_socket.close()
            print("Socket closed")
            exit()

if __name__ == "__main__":
    sock_main()