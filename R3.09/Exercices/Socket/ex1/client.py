import socket
reply = "Reply from client"
host= "localhost"
message = "Hello from Client"

def sock_main():
    client_socket = socket.socket()
    client_socket.connect((host, 8080))
    client_socket.send(message.encode())
    data = client_socket.recv(1024).decode()
    print(data)
    client_socket.close()

if __name__ == "__main__":
    sock_main()