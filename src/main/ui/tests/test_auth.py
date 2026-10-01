from playwright.sync_api import expect
from ui.utils.constants import Urls
from ui.steps.login_steps import LoginSteps
from ui.steps.catalog_steps import CatalogSteps

def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")
    expect(page).to_have_url(Urls.CATALOG)

def test_login_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")
    expect(page).to_have_url(Urls.LOGIN)
    error_text = steps.get_error_text()
    assert "locked out" in error_text


def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    expect(catalog.catalog.product_cards.first, "Ожидаем, что в каталоге есть товары",).to_be_visible()

    catalog.logout()
    expect(page).to_have_url(Urls.LOGIN), "Ожидаем возврат на страницу логина"


def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("visual_user", "secret_sauce")
    expect(catalog.catalog.product_cards.first, "Ожидаем, что в каталоге есть товары",).to_be_visible()

    catalog.logout()
    expect(page).to_have_url(Urls.LOGIN), "Ожидаем возврат на страницу логина"