import requests
from faker import Faker


fake = Faker() 

class BoardApi:
    def __init__(self, base_url:str, token:str) -> None:
        self.base_url =  base_url #"https://trello.com/1/"   /1/cards
        self.token = token # "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxtiaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09"


    # GET ALL THE BOARDS
    def get_all_boards_by_org_id(self, org_id: str) -> list:
        path = "{trello}organization/{id}?boards=open&board_fields=all&fields=boards".format(trello=self.base_url, id=org_id)
        cookie = {"token": self.token}
        resp = requests.get(path, cookies=cookie)      
        return resp.json().get("boards")    


    # CREATE NEW TABLE   
    def create_board(self, name, default_Lists = True) -> dict:
        
        path = "{trello}boards/".format(trello=self.base_url)
        cookie = {"token": self.token}
        new_table_body = {"token": self.token,
                          "name": name,
                          "defaultLists": default_Lists}
        resp = requests.post(path, cookies=cookie, json=new_table_body) 
           
        return resp.json()
    
    # DELETE TABLE 
    def delete_board_by_id(self, id):
        path = "{trello}boards/{board_id}".format(trello=self.base_url, board_id = id)
        delete_table_body = {"token": self.token} 
        resp = requests.delete(path, cookies=delete_table_body , json=delete_table_body)
       
        return resp.json()


    # ADD NEW CARD FROM A BOARD
    def add_card(self, id_list, name_card):
        create_list_body = {
           "token": self.token,
           "idList": id_list,
           "name": name_card
           }
        cookie = {"token": self.token}
        path = "{trello}cards".format(trello=self.base_url)  
        resp = requests.post(path, cookies=cookie , json = create_list_body)

        return resp.json()
    

    def get_list(self, id_table): #{{BaseUrl}}1/boards/{{speed}}/lists/
        cookie = {"token": self.token}
        path = "{trello}boards/{table_id}/lists/".format(trello=self.base_url, table_id = id_table)
        resp = requests.get(path, cookies=cookie).json()
        return resp

    
    def get_card(self, id_card):
        cookie = {"token": self.token}
        path = "{trello}cards/{card_id}".format(trello=self.base_url, card_id = id_card)
        resp = requests.get(path, cookies=cookie).json()
        return resp
  
    def rename_card(self, id_card):
        cookie = {"token": self.token}
        body = {"name": fake.text(20)}  
        path = "{trello}cards/{card_id}?token={token}".format(trello=self.base_url, card_id = id_card, token=self.token)
        resp = requests.put(path, cookies=cookie, json=body).json()
        return resp
    

    def delete_a_card(self, id_card):
        cookie = {"token": self.token}
        
        path = "{trello}cards/{card_id}".format(trello=self.base_url, card_id = id_card)
        resp = requests.delete(path, cookies=cookie, json=cookie).json()
        return resp
    
    def get_all_cards_on_list(self, id_list):
        cookie = {"token": self.token}
        path = "{trello}lists/{list_id}/cards".format(trello=self.base_url, list_id = id_list)
        resp = requests.get(path, cookies=cookie).json()
        return resp
    
    def relocate_a_card(self, id_card, id_board, id_new_list):
        cookie = {"token": self.token}
        path = "{trello}cards/{card_id}?token={token}&idBoard={board_id}&idLIst={list_id}".\
            format(trello=self.base_url, card_id=id_card, board_id=id_board, list_id = id_new_list, token = self.token)
        resp = requests.get(path, cookies=cookie).json()
        return resp