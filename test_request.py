import pytest

from pages import LoginForm, DialogForm


@pytest.fixture
def credentials() -> dict:
    creds = {"email": "tester@tester.ru", "pwd": "3cfsr5y^"}
    return creds


@pytest.fixture
def login_form() -> LoginForm:
    login = LoginForm()
    return login


@pytest.fixture
def dialog_form() -> DialogForm:
    dialog = DialogForm()
    return dialog


def test_login(credentials, login_form, dialog_form):
    with login_form:
        login_form.fill_email(credentials["email"])
        login_form.next_field()
        login_form.fill_password(credentials["pwd"])

    dialog_form.proceed_through_wizard()
    dialog_form.open_dialog()
    dialog_form.ask_question()
    response = dialog_form.get_response()

    assert len(response) > 0
    print("Ответ:\n", response)


