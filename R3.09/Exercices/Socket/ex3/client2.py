import socket
reply = "Reply from client"
host= "localhost"
name = "client2"

def sock_main():
    client_socket = socket.socket()
    print("Socket created")
    client_socket.connect((host, 8080))
    print("Socket connected")
    while True:
        message = str(input("Message: "))
        message += f"/{name}"
        client_socket.send(message.encode())
        if message.split("/")[0] == "bye" or message.split("/")[0] == "arret":
            client_socket.close()
            print("Socket disconnected")
            exit()

if __name__ == "__main__":
    sock_main()