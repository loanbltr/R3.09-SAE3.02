import socket
import threading

host = "localhost"
port = 8080
clients = []

def rcv(address, conn, server_socket):
    global clients
    print(f"Connected to {address}")
    while True:
        try:
            messageOrigin = conn.recv(1024).decode()
            message = messageOrigin.split("/")[0]
            quiceki = messageOrigin.split("/")[1]
            if not message:
                print(f"Client {address} disconnected")
                break
            elif message == "arret":
                print("Stopping communication with all clients")
                close_all_connections(server_socket)
                break
            print(f"{quiceki}: {message}")
        except ConnectionResetError:
            print(f"Connection with {address} lost.")
            break
    conn.close()
    print(f"Connection with {address} closed")

def close_all_connections(server_socket):
    global clients
    for client in clients:
        try:
            client.close()
        except:
            pass
    clients.clear()
    print("All connections closed")
    server_socket.close()
    print("Server socket closed")

def send(conn):
    while True:
        x = str(input("Enter message to send: "))
        conn.send(x.encode())

def sock_main():
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")
    while True:
        conn, address = server_socket.accept()
        clients.append(conn)
        client_thread = threading.Thread(target=rcv, args=(address, conn, server_socket))
        send_thread = threading.Thread(target=send, args=[conn])
        client_thread.start()
        send_thread.start()
        print(f"Started thread for {address}")

if __name__ == "__main__":
    sock_main()