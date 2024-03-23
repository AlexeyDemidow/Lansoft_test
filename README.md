# Тестовое задание. Написание скриптов

### Задание

Написать UI тесты на Python или  JavaScript, которые могут выполнять следующие сценарии

- **Почта Google**
    - Google Почта должна быть ранее создана!
    - Изменить пароль.
    - Изменить  Имя и Фамилию.
    - Сохранение данных в таблицу – Емейл, пароль, Имя фамилия, дата рождения, резервный емейл.
    - Исполняемый файл ```google.py```
  <br><br>
- **Twitter**
    - Twitter должен быть создан ранее!
    - Изменение пароля
    - Подтверждение через почту/указание резервной почты
    - Сделать рандомный пост в Twitter (со звездочкой написать через chatGTP)
    - Исполняемый файл ```twitter.py```
<br><br>
- [galxe.com](http://galxe.com/)
    - Вход https://galxe.com/
    - Подтверждение твиттера через твит
    - Подтверждение дискорда
    - Подтверждение имейла
    - Указание Никнейма
    - Подписка на проекты
    - Подписка на [Mind Network](https://galxe.com/MindNetwork/campaign/GCBv2t4Y26)
    - Выполнены задания для [Mind Network](https://galxe.com/MindNetwork/campaign/GCBv2t4Y26):
      1. *Подписка в твиттере*
      2. *Вход в указанный канал дискорда*
    - Исполняемый файл ```galxe.py```

---

## Установка и запуск

- ```git clone https://github.com/AlexeyDemidow/Lansoft_test.git``` клонируем репозиторий
- ```pip install -r requirements.txt``` устанавливаем зависимости
- ```playwright install``` устанавливаем браузеры
- ```python google.py``` запуск скрипта google
- ```python twitter.py``` запуск скрипта twitter
- ```python galxe.py``` запуск скрипта galxe