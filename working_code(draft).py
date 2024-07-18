import time

import pytest
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


timeout = 0.5


@pytest.fixture
def credentials() -> dict:
    creds = {"email": "tester@tester.ru", "pwd": "3cfsr5y^"}
    return creds


class LoginForm:
    def __init__(self):
        self.driver = WebDriver()
        self._elements = Elements(self.driver)

    def next_field(self):
        self._elements.email_input.send_keys(Keys.TAB)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.driver.get("https://webapp.dev.l3m.space/copilot/#/auth")
        time.sleep(5)

    def close(self):
        self.driver.close()

    def fill_email(self, email):
        self._elements.email_area.click()
        self._elements.email_input.send_keys(email)
        self._elements.email_input.send_keys(Keys.TAB)
        time.sleep(timeout)

    def fill_password(self, pwd):
        self._elements.pwd_input.send_keys(pwd)
        time.sleep(timeout)

    def submit(self):
        self._elements.submit_btn.click()
        time.sleep(5)

    def open_dialog(self):
        self._elements.dialog_icon.click()
        time.sleep(timeout)

    def proceed_through_wizard(self):
        try:
            wizard = self._elements.next_wizard_btn
            for _ in range(4):
                wizard.click()
                time.sleep(timeout)
        except Exception:
            pass

    def ask_question(self):
        self._elements.dialog_input.send_keys(
            "какой штраф будет за выброшенный окурок в водоохранной зоне?"
        )
        self._elements.send_btn.click()

    def get_response(self) -> str:
        self.wait_till_response_loaded()
        response = self._elements.response[0].text + " " \
            + self._elements.response_link.text + " " \
            + self._elements.response[1].text
        return response

    def wait_till_response_loaded(self):
        start = time.monotonic()
        while time.monotonic() - start < 30:
            try:
                assert not self._elements.is_loading
            except:
                continue


class Elements:
    def __init__(self, driver):
        self.driver = driver

    @property
    def email_area(self) -> WebElement:
        element = self.driver.find_element(By.CSS_SELECTOR, '[aria-label*=E-mail]')
        return element

    @property
    def email_input(self) -> WebElement:
        element = self.driver.find_element(By.CSS_SELECTOR, '[id=email]')
        return element

    @property
    def pwd_input(self) -> WebElement:
        element = self.driver.find_element(By.CSS_SELECTOR, '[id=current-password]')
        return element

    @property
    def submit_btn(self) -> WebElement:
        element = self.driver.find_elements(
            By.CSS_SELECTOR, '[role=button]'
        )
        return element[0]

    @property
    def dialog_icon(self) -> WebElement:
        element = self.driver.find_element(By.XPATH, '//*[contains(text(), "Диалог")]')
        return element

    @property
    def next_wizard_btn(self) -> WebElement:
        element = self.driver.find_element(
            By.XPATH, '//*[contains(text(), "Начать") or contains(text(), '
                      '"Далее") or contains(text(), "Начать работу") ]',
        )
        return element

    @property
    def dialog_input(self) -> WebElement:
        element = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="/Диалог"]')
        return element

    @property
    def send_btn(self) -> WebElement:
        elements = self.driver.find_elements(
            By.XPATH, '//*[@aria-label="/Диалог"]//..//following-sibling::*')
        return elements[1]

    @property
    def response(self) -> list[WebElement]:
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'span')
        return elements

    @property
    def response_link(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "a")

    @property
    def is_loading(self) -> bool:
        elements = self.driver.find_elements(By.XPATH, '//*[contains(text(), "%")]')
        return len(elements) == 3


def login():
    with LoginForm() as login:
        login.fill_email("tester@tester.ru")
        login.fill_password("3cfsr5y^")
        login.submit()
        login.proceed_through_wizard()
        login.open_dialog()
        login.ask_question()
        response = login.get_response()
    assert len(response) > 0
    print("Ответ:\n", response)


login()

