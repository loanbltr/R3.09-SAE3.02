import socket
reply = "Reply from client"
host= "localhost"
name = "client1"

def rcv(address, conn):
    print(f"Connected to {address}")
    while True:
        try:
            messageOrigin = conn.recv(1024).decode()
            message = messageOrigin.split("/")[0]
            quiceki = messageOrigin.split("/")[1]
            print(f"{quiceki}: {message}")
        except ConnectionResetError:
            print(f"Connection with {address} lost.")
            break
    conn.close()

def send(conn):
    while True:
        x = str(input("Enter message to send: "))
        conn.send(x.encode())

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
        reponse = client_socket.recv(1024).decode()
        print(reponse)

if __name__ == "__main__":
    sock_main()