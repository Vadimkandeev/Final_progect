import requests
from faker import Faker



class Api_for_UI:
    def __init__(self, base_url:str, token:str) -> None:
        self.base_url =  base_url #"https://trello.com/1/"   /1/cards
        self.token = token # "62a01eb2f072a11c2e65969c/ATTScKZElxpOwaMptEcGVOzPa0nF8ZPh8aYXUP9CupnYn5iwrSvL60fqTSJD0yuEbTxYBEA745B5"


 # DELETE TABLE 
    def delete_board_by_id(self, id):
        path = "{trello}boards/{board_id}".format(trello=self.base_url, board_id = id)
        delete_table_body = {"token": self.token} 
        resp = requests.delete(path, cookies=delete_table_body , json=delete_table_body)
       
        return resp.json()

 # GET ALL THE BOARDS
    def get_all_boards_by_org_id(self, org_id: str) -> list:
        path = "{trello}organization/{id}?boards=open&board_fields=all&fields=boards".format(trello=self.base_url, id=org_id)
        cookie = {"token": self.token}
        resp = requests.get(path, cookies=cookie)      
        return resp.json().get("boards")    