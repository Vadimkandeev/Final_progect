from api.BoardApi import BoardApi
from faker import Faker
fake = Faker() 
org_id = "62a01eec169f028abfee19bd"
token = "62a01eb2f072a11c2e65969c/ATTS2gQtUeAdkLAMAoxtiaMh7Lk9hwnziuABBiVn9MpBMnHufo0MwiF3TW4BAfcq0KbF815A9D09"
base_url = "https://trello.com/1/"
api = BoardApi(base_url, token)


def test_create_board(api_client: BoardApi, delete_board:dict):
    board_list_before = api_client.get_all_boards_by_org_id(org_id)

    resp = api_client.create_board(fake.company())
    delete_board["board_id"] = resp.get("id")
    
    board_list_after = api_client.get_all_boards_by_org_id(org_id)
    assert len(board_list_after) - len(board_list_before) == 1
    #api.delete_board_by_id("board_id")



def test_delete_board(api_client: BoardApi, dummy_board_id: str):

    board_list_before = api_client.get_all_boards_by_org_id(org_id)
    api_client.delete_board_by_id(dummy_board_id)
    board_list_after = api_client.get_all_boards_by_org_id(org_id)

    assert len(board_list_before) - len(board_list_after) == 1


   
    
