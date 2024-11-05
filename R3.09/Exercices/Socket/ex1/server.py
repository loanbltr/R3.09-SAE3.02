import socket
reply = "reply from serv"
host = "localhost"
def sock_main():
    server_socket = socket.socket()
    server_socket.bind((host, 8080))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    message = conn.recv(1024).decode()
    print(message)
    conn.send(reply.encode())
    conn.close()
    server_socket.close()

if __name__ == "__main__":
    sock_main()