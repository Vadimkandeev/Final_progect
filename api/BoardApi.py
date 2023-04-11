import requests
from faker import Faker
import allure

fake = Faker() 

class BoardAPI:
    def __init__(self, base_url:str, token:str) -> None:
        self.base_url =  base_url
        self.token = token
                             


    # GET ALL THE BOARDS
    @allure.step("Получить все доски организации {org_id}")
    def get_all_boards_by_org_id(self, org_id: str) -> list:
        path = "{trello}organization/{id}?boards=open&board_fields=all&fields=boards".format(trello=self.base_url, id=org_id)
        cookie = {"token": self.token}
        resp = requests.get(path, cookies=cookie)      
        return resp.json().get("boards")    


    # CREATE NEW TABLE  
    @allure.step("Создать доску {name}.") 
    def create_board(self, name, default_Lists = True) -> dict:
        
        path = "{trello}boards/".format(trello=self.base_url)
        cookie = {"token": self.token}
        new_table_body = {"token": self.token,
                          "name": name,
                          "defaultLists": default_Lists}
        resp = requests.post(path, cookies=cookie, json=new_table_body) 
           
        return resp.json()
    
    # DELETE TABLE 
    @allure.step("Удалить доску {id}")
    def delete_board_by_id(self, id):
        path = "{trello}boards/{board_id}".format(trello=self.base_url, board_id = id)
        delete_table_body = {"token": self.token} 
        resp = requests.delete(path, cookies=delete_table_body , json=delete_table_body)
       
        return resp.json()


   