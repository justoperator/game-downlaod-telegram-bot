#BOT CODE, CHANGE TOKEN TO YOUR BOT TOKEN(line: 12) WHAT YOU GOT FROM @BotFather , AND PASTE YOUR TELEGRAM ID IN admins(line: 19) LIST
#Send '/help' command to bot for see all commands

import telebot
from telebot import types
import sqlite3
import json
import random
import os
import string

TOKEN = 'PASTE HERE YOUR API KEY'
bot = telebot.TeleBot(TOKEN)

#Function what generate random names for game photos
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

admins = [PASTE HERE YOUR TELEGRAM ID]

#TEXTS IN ENGLISH AND RUSSIAN LANGUAGES
texts = {
    'en': {
        'welcome': '👋 Welcome! Please confirm (here you can write some your text)',
        'confirm': '✅ I confirm',
        'confirmed': '🎉 You have confirmed!',
        'menu_prompt': '📋 Choose an option:',
        'random_game': '🎲 Random game',
        'game_by_tag': '🏷️ Game by tag',
        'instruction': '📜 Instruction',
        'contact': '📞 Contact',
        'language': '🌐 Language',
        'system': '🖥️ System',
        'android': '🤖 Android',
        'windows': '🪟 Windows',
        'instruction_caption': '''📜 Instructions for installing games:\n
**Step 1:** Click on the “⬇️ Download game” button for the game you want to install.\n
**Step 2:** After clicking on the “⬇️ Download game” button you will see a link to the file sharing service, click on it.\n
**Step 3:** After you get to the file sharing service, click on the “Click here to unlock” button, if you get a message asking you to allow messages, click “Yes”.\n
**Step 4:** Click on the "Generate link" button, if you get a message about allowing messages, click "Yes".\n
**Step 5:** Click on the "Download" button and wait for your game to install.\n
Everything is ready✅ Enjoy game. (USE YOUR PHOTOS FOR INSTRUCTION)''', #HERE YOU CAN WRITE YOUR INSTRUCTION FOR DOWNLOAD YOUR GAMES, I'M USE VEXFILE FOR SHARING MY GAMES
        'contact_info': '📞Contact me via: @(your telegram username, or other information for contact) (For technical/advertising inquiries only)',
        'choose_language': '🌐 Choose language:',
        'language_set': '✅ Language set to English.',
        'system_set': '✅ System set to {system}.',
        'choose_system': '🖥️ Choose your system:',
        'add_game': '🎮 Enter the name of the game:',
        'enter_description': '✏️ Enter the description of the game:',
        'enter_description_ru': '✏️ Enter the description of the game in Russian:',
        'enter_download_link': '🔗 Enter the download link of the game:',
        'enter_tags': '🏷️ Enter the tags of the game separated by comma:',
        'enter_tag': '🏷️ Enter tag. (For example: novel, simulator, rpg, horror, platformer)', #WRITE HERE TEGS WHY HAVE YOUR GAMES
        'android_or_windows': '🤖 Is the game for Android or Windows?',
        'send_image': '📷 Send the image of the game:',
        'game_added': '✅ Game successfully added to the database!',
        'no_game_founde': '🚫 No games found in database.',
        'no_games_found': '🚫 No games found with that tag.',
        'error_image': '⚠️ Error uploading image, try again.',
        'refresh': '🔄 Your menu has been refreshed.',
        'back': '🔙 Back',
        'no_system_set': '🖥️ You have not set your system yet. Please choose your system using the button below:',
        'choose_system_button': '🖥️ System'
    },
    'ru': {
        'welcome': '👋Добро пожаловать! Пожалуйста, подтвердите, что вас предупредили о наличии NSFW-контента в боте.',
        'confirm': '✅ Я подтверждаю',
        'confirmed': '🎉 Вы подтвердили!',
        'menu_prompt': '📋 Выберите опцию:',
        'random_game': '🎲 Случайная игра',
        'game_by_tag': '🏷️ Игра по тегу',
        'instruction': '📜 Инструкция',
        'contact': '📞 Связь',
        'language': '🌐 Язык',
        'system': '🖥️ Система',
        'android': '🤖 Android',
        'windows': '🪟 Windows',
        'instruction_caption': '''📜 Инструкция по установке игр:\n 
**Шаг 1:** Нажимаем на кнопку "⬇️ Скачать игру" по игрой которую вы желаете установить.\n
**Шаг 2:** После нажатия на кнопку "⬇️ Скачать игру" у вас появится ссылка на файло-обменник, нажмите на неё.\n
**Шаг 3:** После того как вы попали на файло-обменник нажмите на кнопку "Click here to unlock", если у вас появится сообщение о том чтобы разрешить сообщения нажмите "Да".\n
**Шаг 4:** Нажмите на кнопку "Generate link", если у вас появится сообщение о том чтобы разрешить сообщения нажмите "Да".\n
**Шаг 5:** Нажмите на кнопку "Download" и ожидайте пока ваша игра установится.\n
Всё готово✅ Наслаждайтесь игрой. (USE YOUR PHOTOS FOR INSTRUCTION)''', #HERE YOU CAN WRITE YOUR INSTRUCTION FOR DOWNLOAD YOUR GAMES, I'M USE VEXFILE FOR SHARING MY GAMES
        'contact_info': '📞 Свяжитесь со мной через: @(your telegram username, or other information for contact) (Только для технических/рекламных вопросов)',
        'choose_language': '🌐 Выберите язык:',
        'language_set': '✅ Язык установлен на Русский.',
        'system_set': '✅ Система установлена на {system}.',
        'choose_system': '🖥️ Выберите вашу систему:',
        'add_game': '🎮 Введите название игры:',
        'enter_description': '✏️ Введите описание игры:',
        'enter_description_ru': '✏️ Введите описание игры на русском:',
        'enter_download_link': '🔗 Введите ссылку на скачивание игры:',
        'enter_tags': '🏷️ Введите теги игры через запятую:',
        'enter_tag': '🏷️ Введите тег. (К примеру: novel, simulator, rpg, horror, platformer)', #WRITE HERE TEGS WHY HAVE YOUR GAMES
        'android_or_windows': '🤖 Игра для Android или Windows?',
        'send_image': '📷 Отправьте картинку игры:',
        'game_added': '✅ Игра успешно добавлена в базу данных!',
        'no_games_founde': '🚫 В базе данных сейчас нету игр.',
        'no_games_found': '🚫 Игры с таким тегом не найдены.',
        'error_image': '⚠️ Ошибка при загрузке изображения, попробуйте снова.',
        'refresh': '🔄 Ваше меню было обновлено.',
        'back': '🔙 Назад',
        'no_system_set': '🖥️ Вы еще не выбрали свою систему. Пожалуйста, выберите свою систему с помощью кнопки ниже:',
        'choose_system_button': '🖥️ Система'
    }
}

def get_user_language(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE user = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'en'

#Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_id = message.from_user.id
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT user FROM users WHERE user = ?', (user_id,))
        user_exists = c.fetchone()
        
        if user_exists:
            lang = get_user_language(user_id)
            send_menu(message, lang)
        else:
            c.execute('INSERT INTO users (user, areact, language) VALUES (?, ?, ?)', (user_id, 'Active', 'en'))
            conn.commit()
            lang = 'en'
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text=texts[lang]['confirm'], callback_data='confirm')
            markup.add(btn)
            with open('img1.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=texts[lang]['welcome'], reply_markup=markup)
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

#Confirm button handler
@bot.callback_query_handler(func=lambda call: call.data == 'confirm')
def confirm_handler(call):
    user_id = call.from_user.id
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE users SET areact = "Active" WHERE user = ?', (user_id,))
    conn.commit()
    conn.close()
    lang = get_user_language(user_id)
    bot.send_message(call.message.chat.id, texts[lang]['confirmed'])
    send_menu(call.message, lang)

#Main bot menu
def send_menu(message, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(texts[lang]['random_game'])
    btn2 = types.KeyboardButton(texts[lang]['game_by_tag'])
    btn3 = types.KeyboardButton(texts[lang]['instruction'])
    btn4 = types.KeyboardButton(texts[lang]['contact'])
    btn5 = types.KeyboardButton(texts[lang]['language'])
    btn6 = types.KeyboardButton(texts[lang]['system'])
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    bot.send_message(message.chat.id, texts[lang]['menu_prompt'], reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [texts['en']['system'], texts['ru']['system']])
def choose_system(message):
    try:
        chat_id = message.chat.id
        user_language = get_user_language(chat_id)

        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        itembtn1 = types.KeyboardButton(texts[user_language]['android'])
        itembtn2 = types.KeyboardButton(texts[user_language]['windows'])
        back_btn = types.KeyboardButton(texts[user_language]['back'])
        markup.add(itembtn1, itembtn2)
        markup.add(back_btn)

        bot.send_message(chat_id, texts[user_language]['choose_system'], reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

@bot.message_handler(func=lambda message: message.text in [texts['en']['android'], texts['ru']['android']])
def set_system_android(message):
    chat_id = message.chat.id
    user_language = get_user_language(chat_id)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET system = 'Android' WHERE user = ?", (chat_id,))
    conn.commit()
    conn.close()

    bot.send_message(chat_id, texts[user_language]['system_set'].format(system='Android'))
    send_menu(message, user_language)

@bot.message_handler(func=lambda message: message.text in [texts['en']['windows'], texts['ru']['windows']])
def set_system_windows(message):
    chat_id = message.chat.id
    user_language = get_user_language(chat_id)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET system = 'Windows' WHERE user = ?", (chat_id,))
    conn.commit()
    conn.close()

    bot.send_message(chat_id, texts[user_language]['system_set'].format(system='Windows'))
    send_menu(message, user_language)

@bot.message_handler(func=lambda message: message.text in [texts['en']['back'], texts['ru']['back']])
def go_back_to_menu(message):
    chat_id = message.chat.id
    user_language = get_user_language(chat_id)
    send_menu(message, user_language)

#Command what add new game to your bot
@bot.message_handler(commands=['addgame'])
def add_game(message):
    if message.from_user.id in admins:
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, texts[lang]['add_game'])
        bot.register_next_step_handler(message, process_appname_step)
    else:
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, 'You do not have permission to perform this command.')

game_data = {}

def process_appname_step(message):
    game_data['appname'] = message.text
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, texts[lang]['enter_description'])
    bot.register_next_step_handler(message, process_description_step)

def process_description_step(message):
    game_data['descripsion'] = message.text
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, texts[lang]['enter_description_ru'])
    bot.register_next_step_handler(message, process_description_ru_step)

def process_description_ru_step(message):
    game_data['descripsion_ru'] = message.text
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, texts[lang]['enter_download_link'])
    bot.register_next_step_handler(message, process_download_link_step)

def process_download_link_step(message):
    game_data['download_link'] = message.text
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, texts[lang]['enter_tags'])
    bot.register_next_step_handler(message, process_tags_step)

def process_tags_step(message):
    game_data['tags'] = message.text
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, texts[lang]['android_or_windows'])
    bot.register_next_step_handler(message, process_andrpc_step)

def process_andrpc_step(message):
    game_data['andrpc'] = message.text
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, texts[lang]['send_image'])
    bot.register_next_step_handler(message, process_image_step)

def process_image_step(message):
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        random_filename = generate_random_string() + '.jpg'
        photo_path = os.path.join('gamephotos', random_filename)
        
        with open(photo_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        game_data['images'] = random_filename
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO apps (images, appname, descripsion, descripsion_ru, download_link, tags, andrpc) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (game_data['images'], game_data['appname'], game_data['descripsion'], game_data['descripsion_ru'], game_data['download_link'], game_data['tags'], game_data['andrpc']))
        conn.commit()
        conn.close()
        
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, texts[lang]['game_added'])
    else:
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, texts[lang]['error_image'])

def get_user_system(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT system FROM users WHERE user = ?', (user_id,))
    system = c.fetchone()
    conn.close()
    return system[0] if system else None

#Button 
@bot.message_handler(func=lambda message: message.text in ['🎲 Random game', '🎲 Случайная игра'])
def random_game(message):
    try:
        user_system = get_user_system(message.from_user.id)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        if user_system:
            c.execute('SELECT * FROM apps WHERE andrpc = ? ORDER BY RANDOM() LIMIT 1', (user_system,))
        else:
            c.execute('SELECT * FROM apps ORDER BY RANDOM() LIMIT 1')
        
        game = c.fetchone()
        conn.close()
        
        if game:
            lang = get_user_language(message.from_user.id)
            description = game[2] if lang == 'en' else game[3]
            tags = ' '.join([f"#{tag.strip()}" for tag in game[5].split(',')])
            system = game[6] if lang == 'en' else 'OC: ' + game[6]
            
            caption = (f"**{game[1]}**\n\n"
                    f"🖥️ **{system}**\n\n"
                    f"\"{description}\"\n\n"
                    f"{tags}")
            
            markup = types.InlineKeyboardMarkup()
            download_button_text = '⬇️ Download game' if lang == 'en' else '⬇️ Скачать игру'
            markup.add(types.InlineKeyboardButton(text=download_button_text, url=game[4]))
            
            photo_path = os.path.join('gamephotos', game[0])
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup, parse_mode='Markdown')
        else:
            lang = get_user_language(message.from_user.id)
            bot.send_message(message.chat.id, texts[lang]['no_games_founde'])
        
        if not user_system:
            lang = get_user_language(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            system_button_text = texts[lang]['choose_system_button']
            markup.add(types.KeyboardButton(system_button_text))
            bot.send_message(message.chat.id, texts[lang]['no_system_set'], reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

#Button what send user game by tag
@bot.message_handler(func=lambda message: message.text in ['🏷️ Game by tag', '🏷️ Игра по тегу'])
def game_by_tag(message):
    try:
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, texts[lang]['enter_tag'])
        bot.register_next_step_handler(message, process_tag_step)
    except Exception as e:
        print(f"Error: {e}")

def process_tag_step(message):
    try:
        tag = message.text.strip('#')
        user_system = get_user_system(message.from_user.id)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        if user_system:
            c.execute('SELECT * FROM apps WHERE tags LIKE ? AND andrpc = ? ORDER BY RANDOM() LIMIT 1', ('%' + tag + '%', user_system))
        else:
            c.execute('SELECT * FROM apps WHERE tags LIKE ? ORDER BY RANDOM() LIMIT 1', ('%' + tag + '%',))
        
        games = c.fetchall()
        conn.close()
        
        if games:
            lang = get_user_language(message.from_user.id)
            for game in games:
                description = game[2] if lang == 'en' else game[3]
                tags = ' '.join([f"#{t.strip()}" for t in game[5].split(',')])
                system = game[6] if lang == 'en' else 'OC: ' + game[6]
                
                caption = (f"**{game[1]}**\n\n"
                        f"🖥️ **{system}**\n\n"
                        f"\"{description}\"\n\n"
                        f"{tags}")
                
                markup = types.InlineKeyboardMarkup()
                download_button_text = '⬇️ Download game' if lang == 'en' else '⬇️ Скачать игру'
                markup.add(types.InlineKeyboardButton(text=download_button_text, url=game[4]))
                
                photo_path = os.path.join('gamephotos', game[0])
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup, parse_mode='Markdown')
        else:
            lang = get_user_language(message.from_user.id)
            bot.send_message(message.chat.id, texts[lang]['no_games_found'])
        
        if not user_system:
            lang = get_user_language(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            system_button_text = texts[lang]['choose_system_button']
            markup.add(types.KeyboardButton(system_button_text))
            bot.send_message(message.chat.id, texts[lang]['no_system_set'], reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

#Button what send instruction for download to user
@bot.message_handler(func=lambda message: message.text in ['📜 Instruction', '📜 Инструкция'])
def instruction(message):
    try:
        lang = get_user_language(message.from_user.id)
        media = []
        
        # Open files and add them to media list
        photos = [open(f'instruction{i}.jpg', 'rb') for i in range(1, 6)]
        
        # Add media with captions
        for i, photo in enumerate(photos):
            if i == 0:
                media.append(types.InputMediaPhoto(photo, caption=texts[lang]["instruction_caption"], parse_mode='Markdown'))
            else:
                media.append(types.InputMediaPhoto(photo))
        
        bot.send_media_group(message.chat.id, media)
        
        # Close files after sending
        for photo in photos:
            photo.close()
    except Exception as e:
        print(f"Error: {e}")

#Contact button
@bot.message_handler(func=lambda message: message.text == '📞 Contact' or message.text == '📞 Связь')
def contact(message):
    try:
        lang = get_user_language(message.from_user.id)
        bot.send_message(message.chat.id, texts[lang]['contact_info'])
    except Exception as e:
        print(f"Error: {e}")

#Button what send change language menu
@bot.message_handler(func=lambda message: message.text in ['🌐 Language', '🌐 Язык'])
def language(message):
    try:
        lang = get_user_language(message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('English🇬🇧')
        btn2 = types.KeyboardButton('Русский🇷🇺')
        back = types.KeyboardButton(texts[lang]['back'])
        markup.add(btn1, btn2)
        markup.add(back)
        bot.send_message(message.chat.id, texts[lang]['choose_language'], reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

#Buttons for change language
@bot.message_handler(func=lambda message: message.text in ['English🇬🇧', 'Русский🇷🇺'])
def set_language(message):
    user_id = message.from_user.id
    lang = 'en' if message.text == 'English🇬🇧' else 'ru'
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE users SET language = ? WHERE user = ?', (lang, user_id))
    conn.commit()
    conn.close()
    
    bot.send_message(message.chat.id, texts[lang]['language_set'])
    send_menu(message, lang)

#Back button
@bot.message_handler(func=lambda message: message.text in [texts['en']['back'], texts['ru']['back']])
def go_back(message):
    lang = get_user_language(message.from_user.id)
    send_menu(message, lang)

#This function checks status of users, if user block bot - this user don't active anymore, else - active.
def check_user_status():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT user FROM users')
    users = c.fetchall()
    for user in users:
        try:
            bot.send_chat_action(user[0], 'typing')
            c.execute('UPDATE users SET areact = "Active" WHERE user = ?', (user[0],))
        except:
            c.execute('UPDATE users SET areact = "Disable" WHERE user = ?', (user[0],))
    conn.commit()
    conn.close()

import threading

def schedule_check():
    check_user_status()
    threading.Timer(86400, schedule_check).start()

schedule_check()

# Command for clear users table
@bot.message_handler(commands=['clearusers'])
def clear_users(message):
    try:
        if message.from_user.id in admins:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('DELETE FROM users')
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "User table has been cleared.")
        else:
            bot.send_message(message.chat.id, "You do not have permission to perform this command.")
    except Exception as e:
        print(f"Error: {e}")

# Command for show you count of users in the bot
@bot.message_handler(commands=['list'])
def list_users(message):
    if message.from_user.id in admins:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute('SELECT COUNT(*) FROM users')
        total_users = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM users WHERE areact = "Active"')
        active_users = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM users WHERE language = "en"')
        total_users_en = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM users WHERE language = "ru"')
        total_users_ru = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM users WHERE language = "en" AND areact = "Active"')
        active_users_en = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM users WHERE language = "ru" AND areact = "Active"')
        active_users_ru = c.fetchone()[0]

        conn.close()

        response = (f"Active users: {active_users}\n"
                    f"Total users: {total_users}\n"
                    f"Total users (English): {total_users_en}\n"
                    f"Total users (Russian): {total_users_ru}\n"
                    f"Active users (English): {active_users_en}\n"
                    f"Active users (Russian): {active_users_ru}")

        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "You do not have permission to perform this command.")

# Command for adding new news to the bot and then sending out a newsletter 
@bot.message_handler(commands=['addnews'])
def add_news(message):
    if message.from_user.id in admins:
        bot.send_message(message.chat.id, "Please send the news text:")
        bot.register_next_step_handler(message, save_news)
    else:
        bot.send_message(message.chat.id, "You do not have permission to perform this command.")

def save_news(message):
    news_text = message.text
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump({"news": news_text}, f)
    bot.send_message(message.chat.id, "News has been added.")

# Command for adding new news to the bot and then sending out a newsletter (For users with russian languages)
@bot.message_handler(commands=['addnewsru'])
def add_news_ru(message):
    if message.from_user.id in admins:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте текст новости:")
        bot.register_next_step_handler(message, save_news_ru)
    else:
        bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды.")

def save_news_ru(message):
    news_text = message.text
    with open('news_ru.json', 'w', encoding='utf-8') as f:
        json.dump({"news": news_text}, f)
    bot.send_message(message.chat.id, "Новость добавлена.")

# Command for send news only for you
@bot.message_handler(commands=['seenews'])
def see_news(message):
    if message.from_user.id in admins:
        with open('news.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
        bot.send_message(message.chat.id, news['news'])
    else:
        bot.send_message(message.chat.id, "You do not have permission to perform this command.")

# Command for send news only for you (In russian)
@bot.message_handler(commands=['seenewsru'])
def see_news_ru(message):
    if message.from_user.id in admins:
        with open('news_ru.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
        bot.send_message(message.chat.id, news['news'])
    else:
        bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды.")

# Command for send news to all users who use your bot
@bot.message_handler(commands=['sendnews'])
def send_news(message):
    if message.from_user.id in admins:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT user, language FROM users WHERE areact = "Active"')
        users = c.fetchall()
        conn.close()

        with open('news.json', 'r', encoding='utf-8') as f:
            news_en = json.load(f)['news']
        with open('news_ru.json', 'r', encoding='utf-8') as f:
            news_ru = json.load(f)['news']

        for user_id, lang in users:
            news = news_en if lang == 'en' else news_ru
            try:
                bot.send_message(user_id, news)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

        bot.send_message(message.chat.id, "News has been sent to all active users.")
    else:
        bot.send_message(message.chat.id, "You do not have permission to perform this command.")

# This command show you list of all commands
@bot.message_handler(commands=['help'])
def help_admin(message):
    if message.from_user.id in admins:
        response = ("/list - Show the number of users.\n"
                    "/addgame - Add new game to the bot.\n"
                    "/clearusers - Delete all users from database.\n"
                    "/addnews - Add news to be sent (in English).\n"
                    "/addnewsru - Add news to be sent (in Russian).\n"
                    "/seenews - View the current news in English.\n"
                    "/seenewsru - View the current news in Russian.\n"
                    "/sendnews - Send the news to all active users.\n"
                    "/help - Show this help message.")
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "You do not have permission to perform this command.")

# Command for refresh menu
@bot.message_handler(commands=['refresh'])
def refresh(message):
    user_id = message.from_user.id
    user_language = get_user_language(user_id)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(texts[user_language]['random_game'])
    btn2 = types.KeyboardButton(texts[user_language]['game_by_tag'])
    btn3 = types.KeyboardButton(texts[user_language]['instruction'])
    btn4 = types.KeyboardButton(texts[user_language]['contact'])
    btn5 = types.KeyboardButton(texts[user_language]['language'])
    btn6 = types.KeyboardButton(texts[user_language]['system'])
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    
    bot.send_message(message.chat.id, texts[user_language]['refresh'], reply_markup=markup)

bot.polling(none_stop=True)