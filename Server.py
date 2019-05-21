import threading
import socket
import json
from Database import ConnectionDatabase
import sys

from services.JsonParser import JsonParser


class Server:
    clients = {}
    room_list = {}

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("Socket failed with error:: " + err)

    def __init__(self, host, port):
        self.database = ConnectionDatabase()
        self.host = host
        self.port = port
        self.serverSocket.bind((self.host, self.port))  ## bind Takes turple as first parameter
        self.room_list = self.database.room_list()

    def listener(self):
        while True:
            self.serverSocket.listen(10)
            print("Waiting for connection...")
            client, client_address = self.serverSocket.accept()
            client.sendall(bytes('{ "type":"server-message", "message":"Welcome to secret chat 0" }', "utf-8"))
            threading.Thread(target=self.client_handler, args=(client, client_address)).start()

    def client_handler(self, client, client_address):
        size = 1024
        while True:
            data = client.recv(size).decode("utf-8")
            json_data = JsonParser.parse(data)

            should_break = False

            for json_element in json_data:
                # print(json_element)
                final_json_data = json.loads(json_element)
                result = self.event_switch(final_json_data, client, client_address)

                # print(result)
                if result is False:
                    quit_program = {
                        "type": "quit"
                    }
                    client.sendto(JsonParser.prepare(quit_program), client_address)
                    client.close()
                    should_break = True
                    break

            if should_break is True:
                break

    def event_switch(self, json_data, client, client_address):
        event = json_data["type"]
        del json_data["type"]

        json_data = list(json_data.values())
        switch = {
            "login": {
                "class": self.database,
                "method": "check_login",
                "params": json_data,
            },
            "send-message": {
                "class": self,
                "method": "send_message",
                "params": json_data + [client_address],
            },
            "create-room": {},
            "join-room": {}
        }

        current_event = switch[event]
        result = getattr(current_event["class"], current_event["method"])(*current_event["params"])

        #print(result)

        if type(result) == int:
            self.clients[result] = {
                "room_id": 1,
                "connection": client_address
            }

            room_list = self.database.room_list()
            room_list = json.dumps(room_list)

            final_room_list = {
                "type": "room-list",
                "data": room_list
            }

            client.sendto(JsonParser.prepare(final_room_list), client_address)

            server_message = {
                "type": "server-message",
                "message": "Login Success"
            }
            client.sendto(JsonParser.prepare(server_message), client_address)

            #print(self.clients)

        if result is False:
            server_message = {
                "type": "server-message",
                "message": "Wrong Username or Password"
            }
            client.sendto(JsonParser.prepare(server_message), client_address)
            return False

    def send_message(self, message, client_address):


        print(client_address)


class User:
    pass


class ChatRooms:
    pass


def main():
    ##database = ConnectionDatabase()
    ##database.check_login("admin", "admins")
    ##database.check_user(1)
    serverSocket = Server("localhost", port=8080)
    ##serverSocket.event_switch("wqdqdqwd")
    serverSocket.listener()

    ##Server("localhost", port=8080).listener()


if __name__ == '__main__':
    MainThread = threading.Thread(target=main)
    MainThread.start()
    MainThread.join()
    Server.serverSocket.close()
