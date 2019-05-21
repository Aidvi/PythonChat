import mysql.connector


class ConnectionDatabase:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host="localhost",
                                                      database="python_chat",
                                                      user="root",
                                                      password="admin")

            self.cursor = self.connection.cursor(prepared=True)
        except mysql.connector.Error as error:
            print("Connection to Database failed: {}".format(error))

    def check_login(self, username, password):
        sql_prepare_query = """SELECT * FROM user WHERE username = %s AND password = %s"""

        client_input = (username, password)
        self.cursor.execute(sql_prepare_query, client_input)
        result = self.cursor.fetchall()

        print(password)
        print(username)

        if len(result) == 0:
            print("User not found in database")
            return False
        else:
            print(result[0][0])
            print("User found")
            return {
                "id": result[0][0],
                "username": result[0][1]
            }

    def check_user(self, user_id):
        sql_prepare_query = """SELECT * FROM user WHERE id = %s"""

        search_input = str(user_id)
        self.cursor.execute(sql_prepare_query, search_input)
        result = self.cursor.fetchall()

        if len(result) == 0:
            print("User not found in database")
            return "User not found in database"
        else:
            print(result[0][0])
            return result[0][0]

    def room_list(self):
        sql_prepare_query = """SELECT * FROM rooms"""

        self.cursor.execute(sql_prepare_query)
        result = self.cursor.fetchall()

        room_list = {}

        for row in result:
            room_list[row[0]] = row[1]

        return room_list
