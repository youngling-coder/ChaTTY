import socket
import json
import threading
from styles import ColorStyle

style = ColorStyle()


class Server:
    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 9909
        self.users = {}

    def listen(self, conn):
        while True:

            try:
                # Receive & decode data
                data = conn.recv(4096).decode("utf-8")

                if data:
                    msg = json.loads(data)

                    match msg["type"]:
                        case "meet":
                            id_ = msg["from"]
                            if not id_ in self.users:
                                print(style.success(f"New user added: @[{id_}]"))
                            self.users[id_] = conn

                        case "plain":
                            to_id = msg["to"]

                            if to_id in self.users.keys():
                                msg = json.dumps(msg)
                                self.users[to_id].send(msg.encode("utf-8"))

                            else:
                                response = {
                                    "type": "server",
                                    "text": "There's no user with such uID. Message not delivered!"
                                }

                                response = json.dumps(response)

                                conn.send(response.encode("utf-8"))
            except Exception as e:
                print(style.error(f"An error occured:\n{e}"))
                conn.close()
                print(style.warning(f"Connection closed due to occured error!\n"))
                break

    def bind(self):

        # Launch server socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

            # Bind server to address
            try:
                server.bind((self.HOST, self.PORT))
                print(style.success(f"Server bound: {(self.HOST, self.PORT)}\n"))
            except Exception as e:
                print(style.error(f"Failed to bind: {(self.HOST, self.PORT)}:\n{e}\n"))

            server.listen()

            print(style.bright("Listening to incoming connections...\n"))
            while True:
                # Accept incoming connection
                conn, addr = server.accept()

                print(style.bright(f"New incoming connection from: {addr}"))

                listenThread = threading.Thread(target=self.listen, args=(conn,))
                listenThread.start()

server = Server()

server.bind()
