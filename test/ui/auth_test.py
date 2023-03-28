import allure
import pytest
from page.AuthPage import AuthPage
from page.MainPage import MainPage
from conftest import Conftest
from api.BoardApi import BoardApi
from api.Api_for_UI import Api_for_UI
from time import sleep
from faker import Faker

fake = Faker()
org_id = "62a01eec169f028abfee19bd"

conftest = Conftest

@pytest.mark.skip
def authorization_test(browser):
    email = "vadimkandeev@gmail.com"
    password = "1475Maximus2705"
    username = "Vadimkandeev"

    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)

    main_page = MainPage(browser)
    main_page.open_menu()
    info = main_page.get_account_info()
 

    current_url = main_page.get_current_url()
    with allure.step("Проверить что"+current_url+"заканчивается на vadimkandeev_1975/boards"):
        assert current_url.endswith("vadimkandeev_1975/boards")
    with allure.step("Проверить что указаны данные пользоватля"):
        with allure.step("Имя пользователя должно быть {username}"):
            assert info[0] == username
        with allure.step("Почта пользователя должна быть {email}"):    
            assert info[1] == email
    
@pytest.mark.skip
def test_create_a_board(browser):
    email = "vadimkandeev@gmail.com"
    password = "1475Maximus2705"
    
    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)  


    main_page = MainPage(browser)
    main_page.click_create_a_board("div.board-tile.mod-add")
    main_page.write_name_a_board(fake.text(10))
    main_page.click_create_a_board("[data-testid='create-board-submit-button']")
    test_delete_boards_from_ui()

    sleep(5)

    
@pytest.mark.skip
def test_delete_a_board(browser):

    email = "vadimkandeev@gmail.com"
    password = "1475Maximus2705"
    
    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, password)
     
    main_page = MainPage(browser)
    main_page.add_cookie()
    main_page.click_create_a_board("div.board-tile.mod-add")
    main_page.write_name_a_board(fake.text(10))
    main_page.click_create_a_board("[data-testid='create-board-submit-button']")

    


    