import json
import subprocess
import pyperclip
import time
import os
import sys

import win32api

# while True:
#     try:
#         port = int(input("Введи порт: "))
#         if port > 65535 or port < 0:
#             raise ValueError
#         else:
#             break
#     except ValueError:
#         print("Это не порт!")
#
# name = str(input("Введи уникальное имя: "))
port = 25565
try:
    overview = subprocess.run('zrok.exe overview', capture_output=True, text=True)
    if overview.returncode == 0:
        data = json.loads(overview.stdout)
        tokens = []
        for env in data.get('environments', []):
            for share in env.get('shares', []):
                token = share.get('shareToken')
                if token:
                    tokens.append(token)
    for token in tokens:
        release = subprocess.run(f"zrok.exe release {token}", shell=True, encoding='utf-8', capture_output=True, check=False)
        if f"reserved share '{token}' released" in release.stderr:
            print(f"Токен удален: {token}")
        else:
            print(f"ТОКЕН ({token}) НЕ ПОЛУЧЛОСЬ УДАЛИТЬ (ВОЗМОЖНО ОБНОВА)")
            print("Кинь ошибко Сантику:")
            print(release.stderr)
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_files = [f for f in os.listdir(script_dir) if f.endswith('.txt')]
    if len(txt_files) == 0:
        print("Ошибка: тхт не найден")
        input("Нажми enter для выхода...")
        input("ТЫ УВЕРЕН?")
    elif len(txt_files) > 1:
        print("Ошибка: найдено > 1 тхт в папке со скриптом")
        for f in txt_files:
            print(f" - {f}")
        input("Нажми enter для выхода...")
        input("ТЫ УВЕРЕН?")
    filename = txt_files[0]
    filepath = os.path.join(script_dir, filename)
    name = filename.replace(".txt", "")
    with open(filepath, 'r', encoding='utf-8') as file:
        emails = []
        for line in file:
            line = line.strip()
            if not line:
                continue
            email = line.split()[0].split('-')[0].strip()
            emails.append(email)
    reserve = subprocess.run(f"zrok.exe reserve private 127.0.0.1:{port} --backend-mode tcpTunnel --unique-name {name}", shell=True, encoding='utf-8', capture_output=True, check=True)
    if f"your reserved share token is \'{name}\'" in reserve.stderr:
        print("Токен Зарезервирован! (Profit$$$)")
        for email in emails:
            if not "@" in email:
                print(f"ЭТО НЕ ЕМЕЙЛ. АЛЕРТ АЛЕРТ АЛЕРТ ({email}). ПРОПУСК")
                continue
            modify = subprocess.run(f"zrok modify share {name} --add-access-grant {email}", shell=True, encoding='utf-8', check=False, capture_output=True)
            if not "[ERROR]:" in modify.stderr:
                print(f"{email} - добавлен в white list")
            elif "updateShareBadRequest" in modify.stderr:
                print("ОШИБКА!??!?!?!?")
                print(f"{email} - почта не зарегестрирована в zrok(scam)")
            else:
                print("ОШИБКА!??!?!?!?")
                print("Я пропускаю. Но ты кинь сантику текст:")
                print(modify.stderr)
        subprocess.Popen(f"start /min cmd /c zrok.exe share reserved {name}", shell=True, encoding='utf-8')
    else:
        print("О нет! что то не так с резервацией токена! (ИЛИ ОБНОВА(ЗАЕБАЛ(ПИДОР)))(Или просто имя уже существует)")
        print("Сантику отправь это:")
        print(reserve)
    reserve = subprocess.run(f"zrok.exe reserve private 127.0.0.1:{port} --backend-mode udpTunnel --unique-name {name}udp", shell=True,encoding='utf-8', capture_output=True, check=True)
    if f"your reserved share token is \'{name}udp\'" in reserve.stderr:
        print("Токен Голосового чата Зарезервирован! (Profit$$$)")
        for email in emails:
            if not "@" in email:
                print(f"ЭТО НЕ ЕМЕЙЛ. АЛЕРТ АЛЕРТ АЛЕРТ ({email}). ПРОПУСК")
                continue
            modify = subprocess.run(f"zrok modify share {name}udp --add-access-grant {email}", shell=True, encoding='utf-8', check=False, capture_output=True)
            if not "[ERROR]:" in modify.stderr:
                print(f"{email} - добавлен в white list")
            elif "updateShareBadRequest" in modify.stderr:
                print("ОШИБКА!??!?!?!?")
                print(f"{email} - почта не зарегестрирована в zrok(scam)")
            else:
                print("ОШИБКА!??!?!?!?")
                print("Я пропускаю. Но ты кинь сантику текст:")
                print(modify.stderr)
        subprocess.Popen(f"start /min cmd /c zrok.exe share reserved {name}udp", shell=True, encoding='utf-8')
        time.sleep(3)
        pyperclip.copy(f"zrok access private {name} --bind 127.0.0.1:{port}\nzrok access private {name}udp --bind 127.0.0.1:{port}")
        print(f"Готово! Команда для входа скопирована (если есть проблемы можешь сам скопировать):\nzrok access private {name} --bind 127.0.0.1:{port}\nzrok access private {name}udp --bind 127.0.0.1:{port}")
        input("Нажми enter для выхода...")
        input("ТЫ УВЕРЕН?")
    else:
        print("О нет! что то не так с резервацией токена! (ИЛИ ОБНОВА(ЗАЕБАЛ(ПИДОР)))(Или просто имя уже существует)")
        print("Сантику отправь это:")
        print(reserve)
except Exception as e:
    print("О нет тут жесткая ошибка: " + str(e))
    input("Нажми enter для выхода...")
    input("СОСАЛ? (ДА)")