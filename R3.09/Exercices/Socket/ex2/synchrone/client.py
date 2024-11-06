import socket
reply = "Reply from client"
host= "localhost"

def sock_main():
    client_socket = socket.socket()
    client_socket.connect((host, 8080))
    client_socket.send(message.encode())
    if message == "bye" or "arret":
        client_socket.close()

if __name__ == "__main__":
    message = str(input("Message: "))
    sock_main()