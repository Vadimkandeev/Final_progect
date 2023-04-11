import allure
from api.BoardAPI import BoardAPI
from api.CardAPI import CardAPI

@allure.epic("Автоматизация тестов для проверки работы с досками и карточками в сервисе Trello")
@allure.suite("API-тесты")
class TrelloTestAPI:
    @allure.story("Доски")
    @allure.title("Создание доски")
    @allure.description("Проверка создания новой доски по id организации")
    @allure.severity("Critical")
    @allure.id("API-1")   
    def test_create_board(self, api_client: BoardAPI, delete_board: dict, test_data: dict):
        org_id = test_data.get("org_id")
        board_name = test_data.get("board_name")

        board_list_before = api_client.get_all_boards_by_org_id(org_id)

        resp = api_client.create_board(board_name)

        delete_board["board_id"] = resp.get("id")

        board_list_after = api_client.get_all_boards_by_org_id(org_id)

        with allure.step("Проверить, что количество досок стало больше на 1"):
            assert len(board_list_after) - len(board_list_before) == 1


    @allure.story("Доски")
    @allure.title("Удаление доски")
    @allure.description("Проверка удаления существующей доски по id")
    @allure.severity("Critical")
    @allure.id("API-2")  
    def test_delete_board(self, api_client: BoardAPI, dummy_board_id: str, test_data: dict):
        org_id = test_data.get("org_id")
        
        board_list_before = api_client.get_all_boards_by_org_id(org_id)

        api_client.delete_board_by_id(dummy_board_id)

        board_list_after = api_client.get_all_boards_by_org_id(org_id)

        with allure.step("Проверить, что количество досок стало меньше на 1"):
            assert len(board_list_before) - len(board_list_after) == 1


    @allure.story("Карточки")
    @allure.title("Создание карточки")
    @allure.description("Проверка создания новой карточки по id колонки")
    @allure.severity("Critical")
    @allure.id("API-3") 
    def test_create_card(self, api_card_client: CardAPI, lists_on_board: dict, test_data: dict):
        card_name = test_data.get("card_name")

        cards_on_list_before = api_card_client.get_cards_by_list_id(lists_on_board["list_one_id"])

        created_card = api_card_client.create_card(lists_on_board["list_one_id"], card_name)

        new_card_info = api_card_client.get_card_info(created_card["id"])

        cards_on_list_after = api_card_client.get_cards_by_list_id(lists_on_board["list_one_id"])

        with allure.step("Проверить, что карточка создалась:"):
            with allure.step("количество карточек стало больше на 1"):
                assert len(cards_on_list_after) - len(cards_on_list_before) == 1
            with allure.step("название новой карточки совпадает с заданным названием"):
                assert new_card_info["name"] == card_name
            with allure.step("карточка находится в той колонке, в которую её добавляли"):
                assert lists_on_board["list_one_id"] == new_card_info["idList"]


    @allure.story("Карточки")
    @allure.title("Редактирование карточки")
    @allure.description("Проверка редактирования карточки")
    @allure.severity("Critical")
    @allure.id("API-4") 
    def test_update_card(self, api_card_client: CardAPI, dummy_card_id: str, test_data: dict):
        new_name = test_data.get("new_data")["card_new_name"]
        new_description = test_data.get("new_data")["card_new_description"]        

        api_card_client.get_card_info(dummy_card_id)

        api_card_client.update_card(dummy_card_id, new_name, new_description)

        updated_card_info = api_card_client.get_card_info(dummy_card_id)

        with allure.step("Проверить, что данные карточки изменились:"):
            with allure.step("новое название соответствует заданному"):
                assert updated_card_info["name"] == new_name
            with allure.step("новое описание соответствует заданному"):
                assert updated_card_info["desc"] == new_description

    @allure.story("Карточки")
    @allure.title("Перемещение карточки")
    @allure.description("Проверка перемещения карточки из одной колонки в другую")
    @allure.severity("Critical")
    @allure.id("API-5")
    def test_move_card(self, api_card_client: CardAPI, dummy_card_id: str, get_lists_on_board_by_dummy_card_id: dict):
        api_card_client.get_card_info(dummy_card_id)

        future_list_id = get_lists_on_board_by_dummy_card_id['list_two_id']

        api_card_client.move_one_card(dummy_card_id, future_list_id)

        moved_card_info = api_card_client.get_card_info(dummy_card_id)

        with allure.step("Проверить, что карточка переместилась в другую колонку"):
            assert moved_card_info["idList"] == future_list_id

    @allure.story("Карточки")
    @allure.title("Удаление карточки")
    @allure.description("Проверка удаления существующей карточки по id")
    @allure.severity("Critical")
    @allure.id("API-6")
    def test_delete_card(self, api_card_client: CardAPI, dummy_card_id: str, get_lists_on_board_by_dummy_card_id: dict):
        lists_on_board = get_lists_on_board_by_dummy_card_id["list_one_id"]

        cards_before = api_card_client.get_cards_by_list_id(lists_on_board)

        api_card_client.delete_card(dummy_card_id)

        cards_after = api_card_client.get_cards_by_list_id(lists_on_board)

        with allure.step("Проверить, что карточек в колонке стало меньше на 1"):
            assert len(cards_before) - len(cards_after) == 1