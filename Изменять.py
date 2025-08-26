import requests # Пока оставим для send_notification, но для запросов будем использовать aiohttp
import time
import hashlib
from bs4 import BeautifulSoup
import os
from datetime import datetime
from plyer import notification

# ДОБАВЛЕНО ДЛЯ АСИНХРОННОСТИ
import asyncio
import aiohttp
# import aiofiles # Для асинхронной работы с файлами, если потребуется (пока оставим синхронно для простоты)

# --- НАСТРОЙКИ СКРИПТА ---

# Список сайтов для отслеживания. Каждый элемент списка - это словарь с настройками для одного сайта.
TRACKED_SITES = [
							#Понедельник
# Реинкарнация тёмного магистра
{
        "name": "Магистр Demonic",
        "url": "https://demonicscans.org/manga/The-Heavenly-Demon-Can%2527t-Live-a-Normal-Life",
        "selector": ".chplinks",         
        "hash_file": "demon_demonic_hash.txt",
        "app_name": "Магистр Demonic Tracker"
    },
# Мир после падения
{
        "name": "падение Demonic",
        "url": "https://demonicscans.org/manga/The-World-After-the-Fall",
        "selector": ".chplinks",         
        "hash_file": "world_demonic_hash.txt",
        "app_name": "Падение Demonic Tracker"
    },
# План перерождённого наёмника
{
        "name": "план наёмника Demonic",
        "url": "https://demonicscans.org/manga/The-Regressed-Mercenary%2527s-Machinations",
        "selector": ".chplinks",         
        "hash_file": "plan_demonic_hash.txt",
        "app_name": "План Demonic Tracker"
    },
# Легенда о святом мече (-)

# Бог войны, регрессировавший на 2 уровень (-)

# Боевой король
{
        "name": "Боевой король Demonic",
        "url": "https://demonicscans.org/manga/The-Indomitable-Martial-King",
        "selector": "..chplinks",         
        "hash_file": "Боевой король_demonic_hash.txt",
        "app_name": "Боевой король Demonic Tracker"
    },
# Наномашины: Хаос бога
 {
        "name": "Наномашины Хаос бога Asura",
        "url": "https://asuracomic.net/series/myst-might-mayhem-a7225c05",
        "selector": ".overflow-y-auto", 
        "hash_file": "Наномашины_хаос_бога_asura_hash.txt",
        "app_name": "Наномашины Хаос бога Asura Tracker"
    },
{
        "name": "Наномашины Хаос бога Demonic",
        "url": "https://demonicscans.org/manga/Myst%252C-Might%252C-Mayhem",
        "selector": ".chplinks",         
        "hash_file": "Наномашины_хаос_бога_demonic_hash.txt",
        "app_name": "Наномашины Хаос бога Demonic Tracker"
    },
# Сорока (афк)

							#Вторник
# Ильджин 
{
        "name": "Ильджин Demonic",
        "url": "https://demonicscans.org/manga/The-Bully-In%25252DCharge",
        "selector": ".chplinks",         
        "hash_file": "Ильджин_demonic_hash.txt",
        "app_name": "Ильджин Demonic Tracker"
    },
# Пэк ХХ (hive)

# Элисед (hive)

# 100 регрессия
{
        "name": "100 регрессия Demonic",
        "url": "https://demonicscans.org/manga/The-Max%25252DLevel-Player%2527s-100th-Regression",
        "selector": ".chplinks",         
        "hash_file": "100_регрессия_demonic_hash.txt",
        "app_name": "100 регрессия Demonic Tracker"
    },

 {
        "name": "100 регрессия Asura",
        "url": "https://asuracomic.net/series/the-max-level-players-100th-regression-5e359092",
        "selector": ".overflow-y-auto", 
        "hash_file": "100_регрессия_asura_hash.txt",
        "app_name": "100 регрессия Asura Tracker"
    },
# Ублюдок (vortex)

# Звёздный мастер меча
 {
        "name": "Звёздный мастер меча Asura",
        "url": "https://asuracomic.net/series/star-embracing-swordmaster-b3c90ef2",
        "selector": ".overflow-y-auto", 
        "hash_file": "Звёздный_мастер_меча_asura_hash.txt",
        "app_name": "Звёздный мастер меча Asura Tracker"
    },
{
        "name": "Звёздный мастер меча Demonic",
        "url": "https://demonicscans.org/manga/Star%25252DEmbracing-Swordmaster",
        "selector": ".chplinks",         
        "hash_file": "Звёздный_мастер_меча_demonic_hash.txt",
        "app_name": "Звёздный мастер меча Demonic Tracker"
    },
# Безграничный маг
 {
        "name": "безграничный маг Asura",
        "url": "https://asuracomic.net/series/infinite-mage-61cfdfe9",
        "selector": ".overflow-y-auto", 
        "hash_file": "безграничный_маг_asura_hash.txt",
        "app_name": "безграничный маг Asura Tracker"
    },
{
        "name": "безграничный маг Demonic",
        "url": "https://demonicscans.org/manga/Infinite-Mage",
        "selector": ".chplinks",         
        "hash_file": "безграничный_маг_demonic_hash.txt",
        "app_name": "безграничный маг Demonic Tracker"
    },
# Читатель
 {
        "name": "Читатель Asura",
        "url": "https://asuracomic.net/series/omniscient-readers-viewpoint-2e793a6c",
        "selector": ".overflow-y-auto", 
        "hash_file": "Читатель_asura_hash.txt",
        "app_name": "Читатель Asura Tracker"
    },
{
        "name": "Читатель Demonic",
        "url": "https://demonicscans.org/manga/Omniscient-Reader%2527s-Viewpoint",
        "selector": ".chplinks",         
        "hash_file": "Читатель_demonic_hash.txt",
        "app_name": "Читатель Demonic Tracker"
    },
# Хуашань (афк)

							#Среда
# Возвращение героя катастрофы 
 {
        "name": "катастрофа Asura",
        "url": "https://asuracomic.net/series/return-of-the-disaster-class-hero-69db0865",
        "selector": ".overflow-y-auto", 
        "hash_file": "катастрофа_asura_hash.txt",
        "app_name": "катастрофа Asura Tracker"
    },
{
        "name": "катастрофа Demonic",
        "url": "https://demonicscans.org/manga/The-Return-of-the-Disaster%25252DClass-Hero",
        "selector": ".chplinks",         
        "hash_file": "катастрофа_demonic_hash.txt",
        "app_name": "катастрофа Demonic Tracker"
    },
# Гача (какао)

# Реалити-квест (хз)

# Дурная кровь
 {
        "name": "кровь Asura",
        "url": "https://asuracomic.net/series/bad-born-blood-de7e6379",
        "selector": ".overflow-y-auto", 
        "hash_file": "кровь_asura_hash.txt",
        "app_name": "кровь Asura Tracker"
    },
# Наномашины 
 {
        "name": "Наномашины Asura",
        "url": "https://asuracomic.net/series/nano-machine-aaa740f2",
        "selector": ".overflow-y-auto", 
        "hash_file": "Наномашины_asura_hash.txt",
        "app_name": "Наномашины Asura Tracker"
    },
{
        "name": "Наномашины Demonic",
        "url": "https://demonicscans.org/manga/Nano-Machine",
        "selector": ".chplinks",         
        "hash_file": "Наномашины_demonic_hash.txt",
        "app_name": "Наномашины Demonic Tracker"
    },
# Владыка 
 {
        "name": "Владыка Asura",
        "url": "https://asuracomic.net/series/what-a-bountiful-harvest-demon-lord-8037a845",
        "selector": ".overflow-y-auto", 
        "hash_file": "Владыка_asura_hash.txt",
        "app_name": "Владыка Asura Tracker"
    },
# Рыцарь 
{
        "name": "Рыцарь Asura",
        "url": "https://asuracomic.net/series/terminally-ill-genius-dark-knight-b53322bb",
        "selector": ".overflow-y-auto", 
        "hash_file": "Рыцарь_asura_hash.txt",
        "app_name": "Рыцарь Asura Tracker"
    },
{
        "name": "Рыцарь Demonic",
        "url": "https://demonicscans.org/manga/Terminally%25252DIll-Genius-Dark-Knight",
        "selector": ".chplinks",         
        "hash_file": "Рыцарь_demonic_hash.txt",
        "app_name": "Рыцарь Demonic Tracker"
    },
# Рагнарёк 
{
        "name": "Рагнарёк Asura",
        "url": "https://asuracomic.net/series/solo-leveling-ragnarok-f4b60bcc",
        "selector": ".overflow-y-auto", 
        "hash_file": "Рагнарёк_asura_hash.txt",
        "app_name": "Рагнарёк Asura Tracker"
    },

# Чёртова реинкарнация (афк)

# Жнец луны (афк)

# Палач (афк)

							#Четверг

	# Дизайнер
{
        "name": "Дизайнер Demonic",
        "url": "https://demonicscans.org/manga/The-Greatest-Estate-Developer",
        "selector": ".chplinks",         
        "hash_file": "designer_demonic_hash.txt",
        "app_name": "дизайнер Demonic Tracker"
    },
  # Нуб
	 {
        "name": "Нуб Asura",
        "url": "https://asuracomic.net/series/solo-max-level-newbie-20ab84c1",
        "selector": ".overflow-y-auto", 
        "hash_file": "Noob_asura_hash.txt",
        "app_name": "Нуб Asura Tracker"
    },

    {
        "name": "Нуб Demonic",
        "url": "https://demonicscans.org/manga/Solo-Max%25252DLevel-Newbie",
        "selector": ".chplinks",         
        "hash_file": "noob_demonic_hash.txt",
        "app_name": "Нуб Demonic Tracker"
    },

 # Руководство
	 {
        "name": "Руководство Demonic",
        "url": "https://demonicscans.org/manga/The-Extra%2527s-Academy-Survival-Guide",
        "selector": ".chplinks",         
        "hash_file": "guide_demonic_hash.txt",
        "app_name": "Руководство Demonic Tracker"
  	  },
 
# Охотник SSS
	  {
         "name": "SSS Asura",
        "url": "https://asuracomic.net/series/sss-class-suicide-hunter-302d02f3",
        "selector": ".overflow-y-auto", 
        "hash_file": "SSS_asura_hash.txt",
        "app_name": "SSS Asura Tracker"
    },

# Меч 9 небес
	  {
         "name": "Меч девяти небес Asura",
        "url": "https://asuracomic.net/series/heavenly-inquisition-sword-5fbf8900", # ОБНОВЛЕНО
        "selector": ".overflow-y-auto", 
        "hash_file": "sword9_asura_hash.txt",
        "app_name": "Меч 9 небес Asura Tracker"
    },
 {
        "name": "Меч девяти небес Demonic",
        "url": "https://demonicscans.org/manga/Heavenly-Inquisition-Sword-%2528Nine-Heavens-Swordmaster%2529",
        "selector": ".chplinks",         
        "hash_file": "sword9_demonic_hash.txt",
        "app_name": "Меч 9 небес Demonic Tracker"
  	  },

# Фехтовальщик
	  {
         "name": "Фехтовальщик Asura",
        "url": "https://asuracomic.net/series/the-reincarnated-assassin-is-a-genius-swordsman-a1d61186",
        "selector": ".overflow-y-auto", 
        "hash_file": "Swordsman_asura_hash.txt",
        "app_name": "Фехтовальщик Asura Tracker"
    },
 {
        "name": "Фехтовальщик Demonic",
        "url": "https://demonicscans.org/manga/The-Reincarnated-Assassin-is-a-Genius-Swordsman",
        "selector": ".chplinks",         
        "hash_file": "Swordsman_demonic_hash.txt",
        "app_name": "Фехтовальщик Demonic Tracker"
  	  },

							#Пятница
# Злодей
	 {
        "name": "Злодей Asura",
        "url": "https://asuracomic.net/series/a-villains-will-to-survive-fcfcf109",
        "selector": ".overflow-y-auto", 
        "hash_file": "Villain_asura_hash.txt",
        "app_name": "Злодей Asura Tracker"
    },
{
        "name": "Злодей Demonic",
        "url": "https://demonicscans.org/manga/A-Villain%2527s-Will-to-Survive",
        "selector": ".chplinks",         
        "hash_file": "villian_demonic_hash.txt",
        "app_name": "Злодей Demonic Tracker"
  	  },

 # Игрок прошлого
 {
        "name": "Игрок прошлого Asura",
        "url": "https://asuracomic.net/series/the-player-hides-his-past-dd61d52f",
        "selector": ".overflow-y-auto", 
        "hash_file": "past_asura_hash.txt",
        "app_name": "прошлое Asura Tracker"
    },
	 {
        "name": "Игрок прошлого Demonic",
        "url": "https://demonicscans.org/manga/The-Player-Hides-His-Past",
        "selector": ".chplinks",         
        "hash_file": "past_demonic_hash.txt",
        "app_name": "прошлое Demonic Tracker"
  	  },
 
# Рыцарь дня
	   {
        "name": "Рыцарь дня Demonic",
        "url": "https://demonicscans.org/manga/Eternally-Regressing-Knight",
        "selector": ".chplinks",         
        "hash_file": "Рыцарь_дня_demonic_hash.txt",
        "app_name": "Рыцарь дня Demonic Tracker"
  	  },

# Убийца Питер
 {
        "name": "Убийца Питер Demonic",
        "url": "https://demonicscans.org/manga/Killer-Peter",
        "selector": ".chplinks",         
        "hash_file": "Piter_demonic_hash.txt",
        "app_name": "Питер Demonic Tracker"
  	  },

# С властью короля
 {
        "name": "С властью короля Demonic",
        "url": "https://demonicscans.org/manga/Regressing-with-the-Kings-Power",
        "selector": ".chplinks",         
        "hash_file": "king_demonic_hash.txt",
        "app_name": "С властью короля Demonic Tracker"
  	  },

							#Суббота
# АФК

# Младший сын мечника
 {
        "name": "мечник Asura",
        "url": "https://asuracomic.net/series/swordmasters-youngest-son-0527619f",
        "selector": ".overflow-y-auto", 
        "hash_file": "мечник_asura_hash.txt",
        "app_name": "мечник Asura Tracker"
    },
# Авантюрист
 {
        "name": "Авантюрист Asura",
        "url": "https://asuracomic.net/series/the-last-adventurer-bd6e7618",
        "selector": ".overflow-y-auto", 
        "hash_file": "Авантюрист_asura_hash.txt",
        "app_name": "Авантюрист Asura Tracker"
 },
 {
        "name": "Авантюрист Demonic",
        "url": "https://demonicscans.org/manga/The-Last-Adventurer",
        "selector": ".chplinks",         
        "hash_file": "Авантюрист_demonic_hash.txt",
        "app_name": "Авантюрист Demonic Tracker"
  	  },
# Наёмник
 {
        "name": "Наёмник Demonic",
        "url": "https://demonicscans.org/manga/Mercenary-Enrollment",
        "selector": ".chplinks",         
        "hash_file": "Наёмник_demonic_hash.txt",
        "app_name": "Наёмник Demonic Tracker"
  	  },

# Академия
 {
        "name": "Академия Asura",
        "url": "https://asuracomic.net/series/academys-genius-swordmaster-1b02b083",
        "selector": ".overflow-y-auto", 
        "hash_file": "Академия_asura_hash.txt",
        "app_name": "Академия Asura Tracker"
    },
# Ржавчина 

# Принципы (афк)

# Дракон (афк)

# Новая жизнь убийцы богов (афк)

# Убийца (афк)

							#Воскресенье
# Хозяйка (-)

# Гончая 
{
        "name": "Гончая Asura",
        "url": "https://asuracomic.net/series/revenge-of-the-iron-blooded-sword-hound-06f33b0c",
        "selector": ".overflow-y-auto", 
        "hash_file": "Гончая_asura_hash.txt",
        "app_name": "Гончая Asura Tracker"
    },
# Образование (сливы)

# Ветролом (вортекс)

# Абсолютное Чувство Меча 
 {
        "name": "Чувство Меча Demonic",
        "url": "https://demonicscans.org/manga/Absolute-Sword-Sense",
        "selector": ".chplinks",         
        "hash_file": "Чувство_Меча_demonic_hash.txt",
        "app_name": "Чувство Меча Demonic Tracker"
  	  },

# Игрок
 {
        "name": "Игрок Asura",
        "url": "https://asuracomic.net/series/player-who-returned-10000-years-later-29012feb",
        "selector": ".overflow-y-auto", 
        "hash_file": "Игрок_asura_hash.txt",
        "app_name": "Игрок Asura Tracker"
 },
 {
        "name": "Игрок Demonic",
        "url": "https://demonicscans.org/manga/Player-Who-Returned-10%252C000-Years-Later",
        "selector": ".chplinks",         
        "hash_file": "Игрок_demonic_hash.txt",
        "app_name": "Игрок Demonic Tracker"
  	  },
# Герцог 
 {
        "name": "Герцог Asura",
        "url": "https://asuracomic.net/series/the-regressed-son-of-a-duke-is-an-assassin-5ec7785b",
        "selector": ".overflow-y-auto", 
        "hash_file": "Герцог_asura_hash.txt",
        "app_name": "Герцог Asura Tracker"
 },
 {
        "name": "Герцог Demonic",
        "url": "https://demonicscans.org/manga/The-Regressed-Son-of-a-Duke-is-an-Assassin",
        "selector": ".chplinks",         
        "hash_file": "Герцог_demonic_hash.txt",
        "app_name": "Герцог Demonic Tracker"
  	  },
# Невероятное обучение
{
        "name": "обучение Asura",
        "url": "https://asuracomic.net/series/the-tutorial-is-too-hard-eff98278",
        "selector": ".overflow-y-auto", 
        "hash_file": "обучение_asura_hash.txt",
        "app_name": "обучение Asura Tracker"
 },
 {
        "name": "обучение Demonic",
        "url": "https://demonicscans.org/manga/The-Tutorial-is-Too-Hard",
        "selector": ".chplinks",         
        "hash_file": "обучение_demonic_hash.txt",
        "app_name": "обучение Demonic Tracker"
  	  },
# Миф 
{
        "name": "Миф Asura",
        "url": "https://asuracomic.net/series/i-obtained-a-mythic-item-913dd1af",
        "selector": ".overflow-y-auto", 
        "hash_file": "Миф_asura_hash.txt",
        "app_name": "Миф Asura Tracker"
 },
 {
        "name": "Миф Demonic",
        "url": "https://demonicscans.org/manga/I-Obtained-a-Mythic-Item",
        "selector": ".chplinks",         
        "hash_file": "Миф_demonic_hash.txt",
        "app_name": "Миф Demonic Tracker"
  	  },
# Башня бога (перерыв)

]

# Общий интервал между полными циклами проверки всех сайтов в секундах.
INTERVAL_SECONDS = 180 

# Имя подпапки для логов и хеш-файлов
LOG_FOLDER_NAME = "Логи тайтлов" 

# Имя файла, в который будут записываться общие логи об изменениях.
LOG_FILE_NAME = "общие_логи.log" 

# --- НАСТРОЙКИ TELEGRAM УВЕДОМЛЕНИЙ (ДОБАВЛЮ ПУСТЫЕ ЗНАЧЕНИЯ, ЕСЛИ ИХ НЕТ) ---
# Замените эти значения на ваши полученные на Шагах 1 и 2
TELEGRAM_BOT_TOKEN = "7410799687:AAE6rzrXeobSd0QZFcp1R0dRzky40wBbsY8" # Вставьте ваш токен здесь
TELEGRAM_CHAT_ID = "-1002721265846"   # Вставьте ваш Chat ID здесь
# --- КОНЕЦ НАСТРОЕК TELEGRAM ---

# --- ФУНКЦИИ СКРИПТА ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
LOG_FOLDER_PATH = os.path.join(BASE_DIR, LOG_FOLDER_NAME)
FULL_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, LOG_FILE_NAME)

os.makedirs(LOG_FOLDER_PATH, exist_ok=True)


def log_message(message, include_timestamp=True):
    """
    Записывает сообщение в консоль и в файл лога.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}" if include_timestamp else message
    
    print(log_entry)
    
    with open(FULL_LOG_FILE_PATH, 'a', encoding='utf-8') as f: 
        f.write(log_entry + "\n")

def send_notification(title, message, app_name_param='Web Tracker', timeout=10, url_to_open=None):
    """
    Отправляет уведомление на рабочий стол и в Telegram.
    """
    # Отправка уведомления на рабочий стол
    try:
        notification.notify(
            title=title,
            message=message,
            app_name=app_name_param,
            timeout=timeout,
            url=url_to_open
        )
    except Exception as e:
        log_message(f"Ошибка при отправке настольного уведомления: {e}")

    # Отправка уведомления в Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID: 
        telegram_message_text = f"*{title}*\n\n{message}" 
        telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": telegram_message_text,
            "parse_mode": "Markdown", 
            "disable_web_page_preview": True 
        }
        if url_to_open:
            payload["reply_markup"] = {
                "inline_keyboard": [
                    [{"text": "Жмякай сюда", "url": url_to_open}]
                ]
            }

        try:
            # Используем requests для Telegram, так как это отдельный HTTP-вызов,
            # и он не находится в критическом пути получения контента сайтов.
            telegram_response = requests.post(telegram_api_url, json=payload) 
            telegram_response.raise_for_status() 
            log_message(f"Уведомление отправлено в Telegram для: {title}", include_timestamp=False)
        except requests.exceptions.RequestException as e:
            log_message(f"Ошибка при отправке уведомления в Telegram: {e}", include_timestamp=False)
        except Exception as e:
            log_message(f"Произошла непредвиденная ошибка при отправке в Telegram: {e}", include_timestamp=False)
    else:
        log_message("Настройки Telegram для уведомлений не указаны. Пропускаем отправку в Telegram.", include_timestamp=False)

# ИЗМЕНЕНО: Асинхронная функция для получения контента
async def get_page_content_async(session: aiohttp.ClientSession, url: str, selector: str = None):
    """
    Асинхронно загружает содержимое веб-страницы.
    Если указан селектор, возвращает текст только из выбранного элемента.
    """
    try:
        headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
            response.raise_for_status()
            text = await response.text()

            if selector:
                soup = BeautifulSoup(text, 'html.parser')
                target_element = soup.select_one(selector)
                if target_element:
                    return target_element.get_text(strip=True)
                else:
                    log_message(f"Предупреждение: Элемент с селектором '{selector}' не найден на странице '{url}'. Возможно, структура страницы изменилась.")
                    return None 
            else:
                return text 

    except aiohttp.ClientError as e:
        log_message(f"Ошибка aiohttp при загрузке страницы '{url}': {e}")
        return None
    except Exception as e:
        log_message(f"Произошла непредвиденная ошибка при асинхронном запросе к '{url}': {e}")
        return None

def calculate_hash(content):
    """Вычисляет MD5 хеш содержимого."""
    if content is None:
        return None
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def read_last_hash(hash_file_full_path):
    """Читает хеш предыдущей версии из файла."""
    if os.path.exists(hash_file_full_path):
        try:
            with open(hash_file_full_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            log_message(f"Ошибка при чтении файла хеша '{hash_file_full_path}': {e}. Файл будет создан заново.")
            return None
    return None

def write_last_hash(hash_file_full_path, current_hash):
    """Записывает текущий хеш в файл."""
    try:
        with open(hash_file_full_path, 'w', encoding='utf-8') as f:
            f.write(current_hash)
    except Exception as e:
        log_message(f"Ошибка при записи файла хеша '{hash_file_full_path}': {e}")

# НОВАЯ АСИНХРОННАЯ ФУНКЦИЯ ДЛЯ ПРОВЕРКИ ОДНОГО САЙТА
async def check_single_site(session: aiohttp.ClientSession, site_info: dict):
    site_name = site_info["name"]
    url = site_info["url"]
    selector = site_info["selector"]
    hash_file_name = site_info["hash_file"]
    full_hash_file_path = os.path.join(LOG_FOLDER_PATH, hash_file_name)
    app_name_for_notification = site_info.get("app_name", "Web Tracker") 

    log_message(f"\n--- Проверяем сайт: '{site_name}' ({url}) ---")

    last_hash = read_last_hash(full_hash_file_path)
    if last_hash is None:
        log_message(f"Хеш для '{site_name}' не найден, это первая проверка или файл хеша отсутствует.", include_timestamp=False)
    
    current_content = await get_page_content_async(session, url, selector) 
    
    if current_content is not None:
        current_hash = calculate_hash(current_content)

        if last_hash is None:
            log_message(f"Первая проверка '{site_name}'. Сохраняем текущее состояние.", include_timestamp=False)
            write_last_hash(full_hash_file_path, current_hash)
        elif current_hash != last_hash:
            log_message(f"--- !!! ОБНОВИЛОСЬ: '{site_name}' !!! ---", include_timestamp=False)
            log_message(f"Старый хеш: {last_hash}", include_timestamp=False)
            log_message(f"Новый хеш: {current_hash}", include_timestamp=False)
            
            notification_title = f"Новая глава тайтла: {site_name}"
            notification_message = f"обнаружена на анлейте '{site_name}' ({url})\n"
            notification_message += current_content[:10] + "..." if len(current_content) > 10 else current_content
            
            send_notification(
                notification_title, 
                notification_message, 
                app_name_param=app_name_for_notification, 
                timeout=20, 
                url_to_open=url 
            ) 

            log_message("Новое содержимое (первые 10 символов):", include_timestamp=False)
            log_message(current_content[:10] + "..." if len(current_content) > 10 else current_content, include_timestamp=False)
            
            write_last_hash(full_hash_file_path, current_hash)
        else:
            log_message(f"Ничего не изменилось на '{site_name}'.", include_timestamp=False)
    else:
        log_message(f"Не удалось получить содержимое для '{site_name}'.", include_timestamp=False)

# ИЗМЕНЕНО: Главная функция теперь асинхронная и запускает задачи параллельно
async def main_async(): 
    log_message("--- Запуск Web Tracker для нескольких сайтов ---")
    log_message(f"Общий интервал проверки всех сайтов: {INTERVAL_SECONDS / 60} минут ({INTERVAL_SECONDS} секунд)")
    log_message(f"Логи будут записываться в папку: '{LOG_FOLDER_PATH}'")
    log_message(f"Отслеживается {len(TRACKED_SITES)} сайтов.")

    # Логируем, используются ли настройки Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        log_message("Настроены Telegram-уведомления.", include_timestamp=False)
    else:
        log_message("Telegram-уведомления НЕ настроены (пропущены токен или ID чата).", include_timestamp=False)


    while True:
        log_message("\n--- НАЧИНАЕТСЯ НОВЫЙ ЦИКЛ ПРОВЕРОК ВСЕХ САЙТОВ ---")
        
        start_cycle_time = time.time() # Время начала цикла

        # Создаем одну сессию aiohttp для всех запросов в этом цикле
        async with aiohttp.ClientSession() as session:
            tasks = []
            for site_info in TRACKED_SITES:
                tasks.append(check_single_site(session, site_info))
            
            await asyncio.gather(*tasks)
            
        end_cycle_time = time.time() # Время завершения цикла
        cycle_duration = end_cycle_time - start_cycle_time

        log_message(f"\n--- ЦИКЛ ПРОВЕРОК ЗАВЕРШЕН. Продолжительность цикла: {cycle_duration:.2f} секунд. Следующая полная проверка всех сайтов через {INTERVAL_SECONDS} секунд. ---")
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    # Запускаем асинхронную главную функцию
    asyncio.run(main_async())