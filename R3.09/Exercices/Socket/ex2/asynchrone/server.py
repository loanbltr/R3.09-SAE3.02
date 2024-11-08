import socket
import sys
import threading

host = "localhost"
message = ""

def rcv(s, conn):
    global message
    print("debug")
    while True:
        message = conn.recv(1024).decode()
        if not message:
            print("Client disconnected")
            break
        elif message == "arret":
            print("Stopping communication")
            break
        print(f"MESSAGE DU CLIENT: {message}")
    conn.close()
    s.close()
    print("Socket closed")

def sock_main():
    global message
    server_socket = socket.socket()
    print("Socket created")
    server_socket.bind((host, 8080))
    print("Socket bind complete")
    server_socket.listen(1)
    print("Socket now listening")
    conn, address = server_socket.accept()
    print("Got connection from", address)
    rMsg = threading.Thread(target=rcv, args=[server_socket, conn])
    rMsg.start()

if __name__ == "__main__":
    sock_main()