from time import sleep
from page.AuthPage import AuthPage
from page.MainPage import MainPage


def authorization_test(browser):
    email = "vadimkandeev@gmail.com"
    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as(email, "1475Maximus2705")

    main_page = MainPage(browser)
    main_page.open_menu()
    info = main_page.get_account_info()

    assert main_page.get_current_url().endswith("vadimkandeev_1975/boards")
    assert info[0] == "Vadimkandeev"
    assert info[1] == email
    
