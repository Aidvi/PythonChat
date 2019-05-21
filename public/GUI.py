import threading
import socket
import json
from tkinter import *
import sys

from services.JsonParser import JsonParser


class ClientWrapper:
    room_list = {}

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("Socket failed with error:: " + err)

    def __init__(self, root):
        self.root = root
        self.server_address = ("localhost", 8080)
        self.client_socket.connect(self.server_address)
        threading.Thread(target=self.socket_data).start()

        root.title("Secret Chat")
        root.geometry("600x600")
        LoginFrame(root)
        # ChatFrame(root)

    def socket_data(self):
        size = 1024
        while True:
            data = self.client_socket.recv(size).decode("utf-8")
            json_data = JsonParser.parse(data)

            for json_element in json_data:
                final_json_data = json.loads(json_element)

                result = self.client_event_handler(final_json_data)

                if result is False:
                    self.client_socket.close()
                    print("Exit test")
                    self.root.destroy()
                    sys.exit()

    def client_event_handler(self, json_data):
        event = json_data["type"]
        del json_data["type"]

        switch = {
            "quit": {
                "class": self,
                "method": "close_connection",
                "params": json_data.values()
            },
            "server-message": {
                "class": self,
                "method": "server_message",
                "params": json_data.values()
            },
            "room-list": {
                "class": self,
                "method": "room_list",
                "params": json_data.values()
            },
            "set-id": {
                "class": self,
                "method": "set_id",
                "params": json_data.values()
            }
        }

        current_event = switch[event]
        result = getattr(current_event["class"], current_event["method"])(*current_event["params"])

        return result

    def server_message(self, message):
        # TODO Implement Server message display in GUI view (Tkinter)
        print(message)

    def send_message(self, message):
        message = {
            "type": "send-message",
            "message": message
        }
        self.client_socket.send(JsonParser.prepare(message))

    def room_list(self, data):

        room_list = json.loads(data)

        final_room_list = {}

        for k, v in room_list.items():
            try:
                final_room_list[int(k)] = v
            except (ValueError, TypeError):
                pass

        #print(final_room_list)
        self.room_list = final_room_list

    def close_connection(self):
        print("Connection closed by server")
        return False

    def frame_switch(self, frame_name):
        if frame_name == "chat":
            pass

class LoginFrame(ClientWrapper):
    def __init__(self, root):
        self.login_frame = Frame(root)
        self.login_frame.pack(side="top", fill="both", expand=True)  ## MAN SKAL ÅBENBART PACK, LORTE TKINTER
        self.login_frame.configure(background="black")

        ## Label Username
        Label(self.login_frame, text="Username:", bg="black", fg="white").grid(row=1, column=0, sticky=W)

        ## Username
        self.username = Entry(self.login_frame, width=20, bg="white")
        self.username.grid(row=2, column=0, sticky=W)

        ## Label Password
        Label(self.login_frame, text="Password:", bg="black", fg="white").grid(row=3, column=0, sticky=W)

        ## Password
        self.password = Entry(self.login_frame, width=20, bg="white")
        self.password.grid(row=4, column=0, sticky=W)

        ## Button
        Button(self.login_frame, text="Login", width=6, command=self.login).grid(row=5, column=0, sticky=W)

    def login(self):
        username_text = self.username.get()
        password_text = self.password.get()
        json_credentials = '{ "type":"login", "username":"%s", "password":"%s" }' % (username_text, password_text)
        self.client_socket.send(bytes(json_credentials, "utf-8"))

        self.send_message("TEST SEND MESSAGE FROM CLIENT")

        self.username.delete(0, END)
        self.password.delete(0, END)


class ChatFrame(ClientWrapper):
    def __init__(self, root):
        self.chat_frame = Frame(root)
        self.message_box = Scrollbar(self.chat_frame, wrap=Tk.WORD, width=50, height=25)
        list = Listbox(self.chat_frame, bg="black", height=60, width=100, yscrollcommand=self.message_box)

        self.message_box.pack()
        list.pack()
        self.chat_frame.pack(side="left", fill="both", expand=True)


def main():
    root = Tk()
    ClientWrapper(root)
    root.mainloop()


if __name__ == '__main__':
    main()
