import time

from playwright.sync_api import Playwright, sync_playwright
from playwright._impl._errors import TimeoutError as ToE, TargetClosedError as TCE

args = [
    '--disable-blink-features=AutomationControlled',
    '--lang=en-EN'
]


def galxe_login_and_email_confirm(page, page1):
    page.goto("https://galxe.com/")
    page.locator("#topNavbar").get_by_text("Log in").click()
    page.locator("li").filter(has_text="Email").click()
    page.get_by_placeholder("Enter email address").fill(email)
    page.get_by_text("Send a code").click()
    time.sleep(1)

    try:
        page1.goto("https://www.mail.com/")
        page1.get_by_role("link", name="Log in").click()
    except ToE:
        pass
    else:
        page1.reload()
        page1.get_by_role("link", name="Log in").click()

    page1.get_by_placeholder("Email address").fill(email)
    page1.get_by_placeholder("Password").fill(email_password)
    page1.get_by_role("button", name="Log in").click()
    page1.locator("[data-test=\"actions-menu__visible\"] [data-test=\"actions-menu__item-mail\"]").click()
    page1.locator("[data-test=\"actions-menu__visible\"] [data-test=\"actions-menu__item-mail\"]").click()
    page1.frame_locator("[data-test=\"third-party-frame_mail\"]").get_by_text("Galxe", exact=True).first.click()
    code = page1.frame_locator("[data-test=\"third-party-frame_mail\"]").frame_locator(
        "iframe[name=\"mail-display-content\"]").get_by_role("heading").text_content()
    time.sleep(1)
    page1.close()

    page.get_by_placeholder("Enter code").fill(code)
    page.get_by_role("button", name="Login").click()
    time.sleep(1)

    # Указание никнейма
    if page.get_by_placeholder("At least 4 characters").is_visible():
        page.get_by_placeholder("At least 4 characters").fill(name)
        page.get_by_role("button", name="Create").click()
        time.sleep(1)


def twitter_login(page, page3, twitter_name, twitter_password):
    page.get_by_role("button", name="Log in").click()
    time.sleep(1)
    page.locator("label div").nth(3).click()
    time.sleep(1)
    page.get_by_label("Phone, email address, or username").fill(email)
    page.get_by_role("button", name="Next").click()
    time.sleep(1)
    if page.get_by_label("Password", exact=True).is_visible():
        page.get_by_label("Password", exact=True).fill(twitter_password)
    elif page.get_by_test_id("ocfEnterTextTextInput").is_visible():
        page.get_by_test_id("ocfEnterTextTextInput").fill(twitter_name)
        page.get_by_test_id("controlView").get_by_test_id("ocfEnterTextNextButton").click()
        time.sleep(1)
        page.get_by_label("Password", exact=True).fill(twitter_password)
    time.sleep(1)
    page.get_by_test_id("controlView").get_by_test_id("LoginForm_Login_Button").click()


    page3.goto("https://www.mail.com/")
    time.sleep(1)
    page3.get_by_role("link", name="Log in").click()
    time.sleep(1)
    page3.get_by_placeholder("Email address").fill(email)
    page3.get_by_placeholder("Password").fill(email_password)
    page3.get_by_role("button", name="Log in").click()
    time.sleep(1)
    page3.locator("[data-test=\"actions-menu__visible\"] [data-test=\"actions-menu__item-mail\"]").click()
    page3.frame_locator("[data-test=\"third-party-frame_mail\"]").get_by_text(
        "Your X confirmation code is").first.click()
    code = page3.frame_locator("[data-test=\"third-party-frame_mail\"]").get_by_text(
        "Your X confirmation code is").first.text_content().split(' ')[-1]
    time.sleep(1)
    page3.close()

    page.get_by_test_id("ocfEnterTextTextInput").fill(code)
    page.get_by_test_id("controlView").get_by_test_id("ocfEnterTextNextButton").click()
    time.sleep(1)


def verify_twitter_by_twit(playwright: Playwright) -> None:
    twitter_name = input('Введите имя пользователя Twitter.\n')
    twitter_password = input('Введите пароль от аккаунта Twitter.\n')
    print('Ожидайте.')
    print()

    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()
    page3 = context.new_page()

    galxe_login_and_email_confirm(page, page1)

    time.sleep(1)
    page.locator(".flex-align-center > .campaign-avatar").first.click()
    page.locator("#topNavbar").get_by_text("Settings").click()
    page.get_by_text("Social Accounts").click()
    page.get_by_text("Connect Twitter Account").click()
    with page.expect_popup() as page2_info:
        page.get_by_role("button", name="Tweet").click()
    page2 = page2_info.value

    twitter_login(page2, page3, twitter_name, twitter_password)

    page2.get_by_test_id("tweetButton").click()
    time.sleep(1)
    if page2.get_by_role("button", name="Got it").is_visible():
        time.sleep(1)
        page2.get_by_role("button", name="Got it").click()

    page2.get_by_test_id("DashButton_ProfileIcon_Link").click()
    time.sleep(1)
    page2.get_by_role("link", name="Profile").click()
    time.sleep(1)
    page2.get_by_text("Verifying my Twitter account for my #GalxeID").click()
    link = page2.url

    page.locator(".v-input__slot").click()
    time.sleep(1)
    page.get_by_placeholder("Paste link here").fill(link)
    page.get_by_role("button", name="Verify").click()
    page.locator(".v-responsive__content").click()
    time.sleep(1)
    page.locator(".flex-align-center > .campaign-avatar > div > .campaign-avatar-inner > g > rect").first.click()
    page.locator(".profile-settings > .d-inline-flex").click()
    time.sleep(1)
    page.get_by_text("Social Accounts").click()
    time.sleep(1)
    print('Twitter успешно верифицирован!')
    print()
    # ---------------------
    context.close()
    browser.close()


def verify_discord(playwright: Playwright) -> None:
    discord_email = input('Введите Email для Discord.\n')
    discord_password = input('Введите пароль от Discord.\n')
    print('Ожидайте.')
    print()
    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()

    galxe_login_and_email_confirm(page, page1)

    page.locator(".flex-align-center > .campaign-avatar > div > .campaign-avatar-inner > g > rect").first.click()
    page.locator("#topNavbar").get_by_text("Settings").click()
    page.get_by_text("Social Accounts").click()
    try:
        with page.expect_popup() as page2_info:
            page.get_by_text("Connect Discord Account").click()
        page2 = page2_info.value
        page2.get_by_label("Email or phone number*").fill(discord_email)
        page2.get_by_label("Password*").click()
        page2.get_by_label("Password*").fill(discord_password)
        page2.get_by_role("button", name="Log In").click()
        time.sleep(15)
        page2.get_by_role("button", name="Authorize").click()
        print()
    except TCE:
        pass
    print('Discord успешно верифицирован!')
    # ---------------------
    context.close()
    browser.close()


def follow_projects(playwright: Playwright) -> None:
    projects_quantity = int(input('Введите количество проектов на которые нужно подписаться.\n'))
    print('Ожидайте')
    print()

    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()

    galxe_login_and_email_confirm(page, page1)

    page.get_by_role("link", name="Spaces").first.click()
    time.sleep(1)
    try:
        i = 1
        n = projects_quantity
        while i <= n:
            if page.locator(f"div:nth-child({i}) > .space-follow-button > .d-inline-flex").get_by_text('+ Follow').first.is_visible():
                page.locator(f"div:nth-child({i}) > .space-follow-button > .d-inline-flex").click()
                time.sleep(0.5)
                i += 1
            elif not page.locator(f"div:nth-child({i}) > .space-follow-button > .d-inline-flex").get_by_text('+ Follow').first.is_visible():
                i += 1
                n += 1
    except ToE:
        pass
    print(f'Вы подписаны на {projects_quantity} проектов.')
    print()
    time.sleep(1)

    context.close()
    browser.close()


def follow_mind_network_company(playwright: Playwright) -> None:
    print('Подписка на компанию Mind Network.')
    print('Ожидайте')

    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()

    galxe_login_and_email_confirm(page, page1)

    page.goto("https://galxe.com/MindNetwork/campaign/GCBv2t4Y26")
    time.sleep(1)
    if page.get_by_role("button", name="+ Follow").first.is_visible():
        page.get_by_role("button", name="+ Follow").first.click()
        print('Вы успешно подписались на Mind Network')
        print()

    elif page.get_by_role("button", name="Following").first.is_visible():
        print('Вы уже подписаны.')
        print()

    time.sleep(1)
    context.close()
    browser.close()


def follow_mind_network_company_twitter(playwright: Playwright) -> None:
    print('Подписка на компанию Mind Network в твиттер.\n')
    twitter_name = input('Введите имя пользователя Twitter.\n')
    twitter_password = input('Введите пароль от аккаунта Twitter.\n')
    print('Ожидайте.')
    print()

    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()
    page3 = context.new_page()

    galxe_login_and_email_confirm(page, page1)

    page.goto("https://galxe.com/MindNetwork/campaign/GCBv2t4Y26")
    with page.expect_popup() as page2_info:
        page.get_by_role("button", name="TWITTER Follow @").first.click()
    page2 = page2_info.value

    twitter_login(page2, page3, twitter_name, twitter_password)

    page2.get_by_test_id("confirmationSheetConfirm").click()

    print('Вы успешно подписались на Mind Network в твиттер!')
    print()

    time.sleep(1)
    context.close()
    browser.close()


def enter_discord_channel_ind_network(playwright: Playwright) -> None:
    discord_email = input('Введите Email для Discord.\n')
    discord_password = input('Введите пароль от Discord.\n')
    print('Ожидайте.')
    print()

    browser = playwright.chromium.launch(headless=False, args=args)
    context = browser.new_context()
    page = context.new_page()
    page1 = context.new_page()

    galxe_login_and_email_confirm(page, page1)

    page.goto("https://galxe.com/MindNetwork/campaign/GCBv2t4Y26")
    time.sleep(1)
    try:
        with page.expect_popup() as page2_info:
            page.get_by_role("button", name="Have the Minder role in Mind Network Discord Server").first.click()
        page2 = page2_info.value
        time.sleep(1)
        page2.get_by_role('button', name='Already have an account?').click()
        page2.get_by_label("Email or phone number*").fill(discord_email)
        page2.get_by_label("Password*").click()
        page2.get_by_label("Password*").fill(discord_password)
        page2.get_by_role("button", name="Log In").click()
        time.sleep(15)
        page1.get_by_label("I have read and agree to the").check()
        page1.get_by_role("button", name="Submit").click()
        time.sleep(1)
        time.sleep(100)
    except TCE:
        pass
    print('Вы успешно Вошли в дискорд канал Mind Network!')
    print()
    context.close()
    browser.close()


print('Скрипт для работы с Galxe аккаунтом.')
print('Для выполнения операций введите нужную цифру.')
print('Для начала работы введите Email пользователя, пароль от почты и Имя пользователя если заходите первый раз.')
print()

email = input('Введите Email:\n')
email_password = input('Введите пароль от почты пользователя.\n')
name = input('Введите Имя (если входите не впервые можно оставить пустым):\n')
print()

while True:
    print('Меню:')
    print('1. Подтверждение твиттера через твит.')
    print('2. Подтверждение дискорда.')
    print('3. Подписка на проекты.')
    print()
    print('Выполнение заданий для компании Mind Network:')
    print('\t4. Подписка на Mind Network на galxe.com.')
    print('\t5. Подписка в твиттере на Mind Network (Сначала выполните пункт 1: подтвердите твиттер.).')
    print('\t6. Вход в указанный канал дискорда Mind Network (Сначала выполните пункт 2: подтвердите дискорд.).')
    print()
    print('q - для выхода.')

    choice = input()

    with sync_playwright() as playwright:
        if choice == '1':
            verify_twitter_by_twit(playwright)
        elif choice == '2':
            verify_discord(playwright)
        elif choice == '3':
            follow_projects(playwright)
        elif choice == '4':
            follow_mind_network_company(playwright)
        elif choice == '5':
            follow_mind_network_company_twitter(playwright)
        elif choice == '6':
            enter_discord_channel_ind_network(playwright)
        elif choice == 'q' or choice == 'й':
            print('Выход')
            break
        else:
            print('Выберите значение из меню.')
            print()
