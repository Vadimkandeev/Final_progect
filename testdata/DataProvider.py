import json

my_file = open('test_data.json')
global_data = json.load(my_file)

class DataProvider:
    def __init__(self) -> None:
        self.data = global_data

    def get(self, prop: str) -> str:
        return self.data.get(prop)

    def getint(self, prop: str) -> int:
        val = self.data.get(prop)
        return int(val)

    def get_token(self) -> str:
        return self.data.get("token")
