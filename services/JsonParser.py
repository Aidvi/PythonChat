import json


class JsonParser:

    @staticmethod
    def parse(data):
        formatted_data = data.split("}{")

        start_string = formatted_data[0]

        start = True
        i = 0
        if len(formatted_data) > 1:
            for char in formatted_data:
                if start:
                    start = False
                    formatted_data[0] = formatted_data[0] + "}"
                elif i != len(formatted_data) - 1:
                    formatted_data[i] = "{" + char + "}"
                else:
                    formatted_data[i] = "{" + formatted_data[i]

                i = i + 1

        return formatted_data

    @staticmethod
    def prepare(data):

        return bytes(json.dumps(data), "utf-8")

