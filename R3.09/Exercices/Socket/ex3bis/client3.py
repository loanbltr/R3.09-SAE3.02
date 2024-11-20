import socket
import threading

host = "localhost"
port = 8080
name = "client3"

def rcv(client_socket):
    while True:
        try:
            messageOrigin = client_socket.recv(1024).decode()
            if not messageOrigin:
                print("Disconnected from server.")
                break
            message, quiceki = messageOrigin.split("/")
            print(f"{quiceki}: {message}")
        except ConnectionResetError:
            print("Connection with server lost.")
            break
    client_socket.close()

def send(client_socket):
    while True:
        message = str(input("Message: "))
        message += f"/{name}"
        client_socket.send(message.encode())
        if message.split("/")[0] == "bye" or message.split("/")[0] == "arret":
            client_socket.close()
            print("Socket disconnected")
            exit()

def sock_main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")

    # Start receiving and sending threads
    rcv_thread = threading.Thread(target=rcv, args=(client_socket,))
    send_thread = threading.Thread(target=send, args=(client_socket,))
    rcv_thread.start()
    send_thread.start()

if __name__ == "__main__":
    sock_main()
