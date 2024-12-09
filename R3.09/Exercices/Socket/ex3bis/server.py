import socket
import threading

host = "localhost"
port = 8080
clients = []
server_running = True  # Variable pour contrôler l'état du serveur


def handle_client(conn, address, server_socket):
    global server_running
    print(f"Connected to {address}")
    while server_running:
        try:
            messageOrigin = conn.recv(1024).decode()
            if not messageOrigin:
                print(f"Client {address} disconnected")
                break
            message, quiceki = messageOrigin.split("/")

            if message == "arret":
                print(f"Client {address} sent 'arret'. Stopping server.")
                server_running = False
                close_all_connections()
                server_socket.close()
                break

            print(f"{quiceki}: {message}")
            broadcast(messageOrigin, conn)
        except ConnectionResetError:
            print(f"Connection with {address} lost.")
            break
    conn.close()
    print(f"Connection with {address} closed")


def close_all_connections():
    global clients
    for client in clients:
        try:
            client.close()
        except:
            pass
    clients.clear()
    print("All connections closed")


def broadcast(message, sender_conn=None):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)


def server_send():
    global server_running
    while server_running:
        message = input("Server message: ")
        if message == "arret":
            close_all_connections()
            server_running = False  # Arrête le thread d'envoi de messages
            break
        message += "/server"
        broadcast(message)


def sock_main():
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")
    send_thread = threading.Thread(target=server_send)
    send_thread.start()

    while server_running:
        try:
            conn, address = server_socket.accept()
            clients.append(conn)
            client_thread = threading.Thread(target=handle_client, args=(conn, address, server_socket))
            client_thread.start()
            print(f"Started thread for {address}")
        except OSError:
            # Catch the exception if server_socket is closed to break the loop
            break


if __name__ == "__main__":
    sock_main()
