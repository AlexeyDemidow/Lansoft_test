import time

from playwright.sync_api import Playwright, sync_playwright, expect

args = [
    '--disable-blink-features=AutomationControlled',
    '--lang=en-EN'
]


def login_to_twitter_account(page, page1):
    page.goto("https://twitter.com/")
    page.get_by_test_id("loginButton").click()
    time.sleep(1)
    page.locator("label div").nth(3).click()
    page.get_by_label("Phone, email address, or username").fill(email)
    page.get_by_role("button", name="Next").click()
    time.sleep(1)
    page.get_by_test_id("ocfEnterTextTextInput").fill(name)
    page.get_by_test_id("ocfEnterTextNextButton").click()
    time.sleep(1)
    page.get_by_label("Password", exact=True).fill(password_old)
    page.get_by_test_id("LoginForm_Login_Button").click()
    time.sleep(1)

    page1.goto("https://www.mail.com/")
    page1.reload()
    time.sleep(1)
    page1.get_by_role("link", name="Log in").click()
    page1.get_by_placeholder("Email address").fill(email)
    page1.get_by_placeholder("Password").click()
    page1.get_by_placeholder("Password").fill(email_password)
    page1.get_by_role("button", name="Log in").click()
    page1.locator("[data-test=\"actions-menu__visible\"] [data-test=\"actions-menu__item-mail\"]").click()
    page1.frame_locator("[data-test=\"third-party-frame_mail\"]").get_by_text(
        "Your X confirmation code is").first.click()
    code = page1.frame_locator("[data-test=\"third-party-frame_mail\"]").get_by_text(
        "Your X confirmation code is").first.text_content().split(' ')[-1]
    time.sleep(1)

    page.get_by_test_id("ocfEnterTextTextInput").fill(code)
    page.get_by_test_id("ocfEnterTextNextButton").click()
    time.sleep(1)


def reset_password(playwright: Playwright):
    password_new = input('Введите новый пароль.\n')
    print('Ожидайте.')
    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()

    login_to_twitter_account(page, page1)

    page.get_by_test_id("AppTabBar_More_Menu").click()
    time.sleep(1)
    page.get_by_test_id("settings").click()
    time.sleep(1)
    page.get_by_role("tab", name="Change your password Change").click()
    time.sleep(1)
    page.get_by_label("Current password").fill(password_old)
    page.get_by_label("New password").fill(password_new)
    page.get_by_label("Confirm password").fill(password_new)
    time.sleep(1)
    page.get_by_test_id("settingsDetailSave").click()
    time.sleep(1)
    print('Пароль успешно изменен.')
    print()

    context.close()
    browser.close()

    return password_new


def add_twit(playwright: Playwright) -> None:
    twit = input('Введите текст твита:\n')
    print('Ожидайте.')

    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()

    login_to_twitter_account(page, page1)

    page.get_by_test_id("AppTabBar_Home_Link").click()
    time.sleep(1)
    page.get_by_test_id("tweetTextarea_0").fill(twit)
    time.sleep(1)
    page.get_by_test_id("tweetButtonInline").click()
    time.sleep(1)
    print('Твит успешно добавлен.')
    print()

    context.close()
    browser.close()


print('Скрипт для работы с Twitter аккаунтом.')
print('Для выполнения операций введите нужную цифру.')
print('Для начала работы введите Email пользователя, пароль от почты, Имя пользователя и пароль.')
print()

email = input('Введите Email:\n')
email_password = input('Введите пароль от почты пользователя.\n')
name = input('Введите Имя:\n')
password_old = input('Введите пароль:\n')
print()

while True:
    print('Меню:')
    print('1. Изменить пароль.')
    print('2. Добавить твит с вашим текстом.')
    print('q - для выхода.')

    choice = input()

    with sync_playwright() as playwright:
        if choice == '1':
            password_old = reset_password(playwright)
        elif choice == '2':
            add_twit(playwright)
        elif choice == 'q' or choice == 'й':
            print('Выход')
            break
        else:
            print('Выберите значение из меню.')
            print()
