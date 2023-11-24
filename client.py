import socket
from threading import Thread
from random import randint
import json
from queue import Queue
from styles import ColorStyle


# Create a thread-safe queue
msg_queue = Queue()
style = ColorStyle()



# Custom stylized input
def sinput(prompt, empty=False):
    data = input(style.success(prompt))

    while not empty and not data:
        print(style.error("Enter a value to continue!"))
        data = input(style.success(prompt))

    return data


class Client:
    def __init__(self) -> None:
        self.__HOST = "localhost"
        self.__PORT = 9909
        self.__ID = None

    def msg_send(self, socket_: socket.socket, msg=None):
        while not msg_queue.empty():
            qmsg = msg_queue.get()

            match qmsg["type"]:
                case "plain":
                    msg_block = style.user(f"@[{qmsg['from']}]: ")
                    msg_block += qmsg["text"]
                    print(msg_block)
                case "server":
                    msg_block = style.warning(qmsg["text"])
                    print(msg_block)

        if not msg:
            msg = sinput("Enter message: ", True)

            if msg:
                to = sinput("Enter receiver: ")

                msg = {
                    "type": "plain",
                    "from": self.__ID,
                    "to": to,
                    "text": msg
                }
        if msg:
            type_ = msg["type"]
            msg = json.dumps(msg)
            socket_.send(msg.encode("utf-8"))

            if type_ == "plain":
                print(style.success("Message sent!\n"))

    def msg_recv(self, socket_: socket.socket):
        while True:
            data = socket_.recv(4096)

            if data:
                msg = data.decode("utf-8")
                msg = json.loads(msg)
                msg_queue.put(msg)


    def update(self):
        with open("config.json", "w") as fuser:
            user = {
                "id": self.__ID
            }

            json.dump(user, fuser)

    def start(self):
        with open("config.json") as json_user:
            user = json.load(json_user)

            self.__ID = user["id"]

        self.connect()

def connect(self):
    """
    If you're working on localhost you can comment if condition below to achieve different IDs while launching several client instances
    """
    if not self.__ID:
        print(style.bright("Seems you're new here! Creating your personal uID...\n"))
        self.__ID = self.generateID()
        self.update()
        print(style.success(f"Congratulations! Your new uID is: {self.__ID}\n"))

    greet_text = f"""Welcome to ChaTTY!
    Your uID: {self.__ID}
    """
    print(style.bright(greet_text))
    print(style.success("Connection establishment..."))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((self.__HOST, self.__PORT))
            print(style.bright("Connection established!\n"))

            msg = {
                "type": "meet",
                "from": self.__ID,
                "to": "server"
            }
            self.msg_send(socket_=client, msg=msg)

            recv_trd = Thread(target=self.msg_recv, args=(client,))
            recv_trd.daemon = True
            recv_trd.start()

            while True:
                self.msg_send(client)

        except ConnectionRefusedError:
            print(style.error("Connection refused. Make sure the server is running and reachable."))
        except Exception as e:
            print(style.error(f"Error while connecting to the server:\n{e}"))


    def generateID(self):
        id_ = str(randint(0, 999_999_999_999))

        if len(id_) < 12:
            id_ = "0" * (12 - len(id_)) + id_

        return id_

cli = Client()
cli.start()
