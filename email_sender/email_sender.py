import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.config import EMAIL
from random import choice           


def reset_password(address_to: str):
    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = EMAIL.ADDRESS  # Адресат
    msg['To'] = address_to  # Получатель
    msg['Subject'] = 'Восстановление пароля'  # Тема сообщения

    code_list = list("1234567890")
    code = ''.join([choice(code_list) for _ in range(6)])
    body = f"Код для восстановления пароля - {code}"
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    server = smtplib.SMTP(EMAIL.SERVER, EMAIL.PORT)  # Создаем объект SMTP
    # server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(EMAIL.ADDRESS, EMAIL.PASSWORD)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим
    return code
