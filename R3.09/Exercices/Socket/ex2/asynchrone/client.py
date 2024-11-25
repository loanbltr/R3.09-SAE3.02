import socket
reply = "Reply from client"
host= "localhost"

def sock_main():
    client_socket = socket.socket()
    print("Socket created")
    client_socket.connect((host, 4200))
    print("Socket connected")
    while True:
        message = str(input("Message: "))
        client_socket.send(message.encode())
        if message == "bye" or message == "arret":
            client_socket.close()
            print("Socket disconnected")
            exit()

if __name__ == "__main__":
    sock_main()