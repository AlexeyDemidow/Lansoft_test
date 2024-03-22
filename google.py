import time
import re

from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

args = [
    '--disable-blink-features=AutomationControlled',
    '--lang=en-EN'
]


def login_to_google_account(page):
    page.goto("https://myaccount.google.com/")
    page.get_by_role("link", name="Go to your Google Account").click()
    page.get_by_label("Email or phone").fill(email)
    time.sleep(0.5)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Enter your password").fill(password)
    time.sleep(0.5)
    page.get_by_role("button", name="Next").click()
    time.sleep(0.5)
    page.get_by_role("list").locator("li").filter(has_text="Personal info").click()
    time.sleep(0.5)


def edit_name(playwright: Playwright) -> None:
    first_name = input('Введите новое имя.\n')
    last_name = input('Введите новую фамилию.\n')
    print('Ожидайте.')

    browser = playwright.chromium.launch(headless=False, args=args, slow_mo=100)
    context = browser.new_context()
    page = context.new_page()

    login_to_google_account(page)

    page.get_by_role('link', name='Name').click()
    time.sleep(1)
    page.get_by_role("button", name="Edit Name").click()
    time.sleep(1)
    page.get_by_label("First name").fill(f"{first_name}")
    page.get_by_label("Last name").fill(f"{last_name}")
    time.sleep(1)
    page.locator("button").filter(has_text="Save").click()
    print('Имя и фамилия успешно изменены.')
    print()

    context.close()
    browser.close()


def edit_password(playwright: Playwright):
    new_password = input('Введите новый пароль.\n')
    print('Ожидайте.')

    browser = playwright.chromium.launch(headless=False, args=args, slow_mo=100)
    context = browser.new_context()
    page = context.new_page()

    login_to_google_account(page)

    page.get_by_role('link', name='Password').click()
    time.sleep(0.5)
    page.get_by_label("New password", exact=True).fill(f"{new_password}")
    page.get_by_label("Confirm new password").fill(f"{new_password}")
    time.sleep(0.5)
    page.locator("button").filter(has_text="Change password").click()
    time.sleep(0.5)
    print('Пароль успешно изменен.')
    print()

    context.close()
    browser.close()

    return new_password


def save_data(playwright: Playwright) -> None:
    print('Личные данные пользователя будут сохранены в файл user_data.csv')
    print('Ожидайте.')

    browser = playwright.chromium.launch(headless=False, args=args, slow_mo=100)
    context = browser.new_context()
    page = context.new_page()

    login_to_google_account(page)

    p = page.content()
    soup = BeautifulSoup(p, 'html.parser')
    data = []
    data_dict = {}
    for n in soup.find_all('div', class_='ugt2L aK2X8b t97Ap iDdZmf'):
        data.append(n.text)
    for d in data:
        if 'Name' in d:
            data_dict['name'] = d.removesuffix('chevron_right').removeprefix('Name')
        if 'Birthday' in d:
            data_dict['date_of_birth'] = d.removesuffix('chevron_right').removeprefix('Birthday')
    data = []
    for e in soup.find_all('div', class_='ugt2L aK2X8b iDdZmf'):
        data.append(e.text)
    for d in data:
        if 'Email' in d:
            if len(re.findall(r'.+?.com', d.removesuffix('chevron_right').removeprefix('Email'))) > 1:
                data_dict['email'] = re.findall(r'.+?.com', d.removesuffix('chevron_right').removeprefix('Email'))[0]
                data_dict['reserve_email'] = re.findall(
                    r'.+?.com',
                    d.removesuffix('chevron_right').removeprefix('Email')
                )[1]
            else:
                data_dict['email'] = re.findall(r'.+?.com', d.removesuffix('chevron_right').removeprefix('Email'))[0]
                data_dict['reserve_email'] = None
    data_dict['password'] = password
    df = pd.DataFrame(data=data_dict, index=[0])
    df.to_csv('user_data.csv', sep=';')
    print('Данные сохранены.')
    print()

    context.close()
    browser.close()


print('Скрипт для работы с Google аккаунтом.')
print('Для выполнения операций введите нужную цифру.')
print('Для начала работы введите Email пользователя и пароль.')
print()
email = input('Введите Email:\n')
password = input('Введите пароль:\n')
print()
while True:
    print('Меню:')
    print('1. Изменить имя и фамилию пользователя.')
    print('2. Изменить пароль.')
    print('3. Сохранение данных в таблицу: Имя и фамилия, Email, резервный Email, пароль.')
    print('q - для выхода.')

    choice = input()

    with sync_playwright() as playwright:
        if choice == '1':
            edit_name(playwright)
        elif choice == '2':
            password = edit_password(playwright)
        elif choice == '3':
            save_data(playwright)
        elif choice == 'q' or choice == 'й':
            print('Выход')
            break
        else:
            print('Выберите значение из меню.')
            print()
