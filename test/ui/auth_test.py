import allure
from page.AuthPage import AuthPage
from page.MainPage import MainPage

import pytest


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
    
