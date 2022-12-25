import telebot
import random
import config
from telebot import types
import json

bot = telebot.TeleBot(config.token)

croco_players = {}


def start_user_to_game(message):
	try:
		player = message.text.split()
		croco_players[message.chat.id] = player
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Показать слово", callback_data="Croco"))
		bot.send_message(message.chat.id, f"Игра начинается, учавствует {len(player)} игроков", reply_markup=keyboard)
	except:
		bot.send_message(message.chat.id, "Ошибка! Введите данные правильно")


@bot.message_handler(commands=["start"])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	item1 = types.KeyboardButton("Я никогда не... 🤫")
	item2 = types.KeyboardButton("Правда или действие 🤡")
	item3 = types.KeyboardButton("Крокодил 🐊")
	item4 = types.KeyboardButton("Статистика 📊")
	markup.add(item1, item2, item3, item4)
	bot.send_message(message.chat.id, "Добро пожаловать, вас приветствует Евлампий, выберите игру", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def bot_message(message):
	if message.text == "Я никогда не... 🤫":
		with open("words.txt", "r", encoding="utf-8") as file:
			lines = [line.rstrip() for line in file]
		keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
		key_yes = types.InlineKeyboardButton(text='Следующий факт 🙈', callback_data='Факт')  # кнопка «Да»
		keyboard.add(key_yes)

		bot.send_message(message.chat.id, lines[random.randint(0, len(lines) - 1)], reply_markup=keyboard)

		with open("data.json", "r") as file:
			data = json.load(file)
		if str(message.chat.id) in data:
			data[str(message.chat.id)]['never'] += 1
		else:
			data[str(message.chat.id)] = {"never": 0, "truth": 0, "action": 0, "croco": 0}
			data[str(message.chat.id)]['never'] += 1
		with open("data.json", "w") as file:
			json.dump(data, file)

	if message.text == "Крокодил 🐊":
		bot.send_message(message.chat.id, 'Введите имена игроков через пробел (Иван Анна Алексей)')
		bot.register_next_step_handler_by_chat_id(message.chat.id, start_user_to_game)

	if message.text == "Правда или действие 🤡":
		keyboard = types.InlineKeyboardMarkup()
		key_new = types.InlineKeyboardButton(text='Правда 💬', callback_data='Правда')
		keyboard.add(key_new)
		key_pass = types.InlineKeyboardButton(text='Действие ✋', callback_data="Действие")
		keyboard.add(key_pass)

		bot.send_message(message.chat.id, "Выберите вариант игры", reply_markup=keyboard)

	if message.text == "Статистика 📊":
		with open("data.json", "r") as file:
			data = json.load(file)
		if str(message.chat.id) in data:
			text = f"Статистика:\nЯ никогда не: {data[str(message.chat.id)]['never']}\n" \
				   f"Ответили правду: {data[str(message.chat.id)]['truth']}\n" \
				   f"Выбрали действие: {data[str(message.chat.id)]['action']}\n" \
				   f"Отгадали слов в крокодиле: {data[str(message.chat.id)]['croco']}"

		else:
			data[str(message.chat.id)] = {"never": 0, "truth": 0, "action": 0, "croco": 0}

			text = f"Статистика:\nЯ никогда не: {data[str(message.chat.id)]['never']}\n" \
				   f"Ответили правду: {data[str(message.chat.id)]['truth']}\n" \
				   f"Выбрали действие: {data[str(message.chat.id)]['action']}\n" \
				   f"Отгадали слов в крокодиле: {data[str(message.chat.id)]['croco']}"

		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="Обнулить статистку", callback_data="Reload"))

		bot.send_message(message.chat.id, text, reply_markup=keyboard)
		with open("data.json", "w") as file:
			json.dump(data, file)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "Факт":
		with open("words.txt", "r", encoding="utf-8") as file:
			lines = [line.rstrip() for line in file]
		keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
		key_yes = types.InlineKeyboardButton(text='Следующий факт 🙈', callback_data='Факт')  # кнопка «Да»
		keyboard.add(key_yes)

		bot.send_message(call.message.chat.id, lines[random.randint(0, len(lines) - 1)], reply_markup=keyboard)

		with open("data.json", "r") as file:
			data = json.load(file)
		if str(call.message.chat.id) in data:
			data[str(call.message.chat.id)]['never'] += 1
		else:
			data[str(call.message.chat.id)] = {"never": 0, "truth": 0, "action": 0, "croco": 0}
			data[str(call.message.chat.id)]['never'] += 1
		with open("data.json", "w") as file:
			json.dump(data, file)

	if call.data == "Правда":
		with open("true.txt", "r", encoding="utf-8") as file:
			lines = [line.rstrip() for line in file]
		keyboard = types.InlineKeyboardMarkup()
		key_new = types.InlineKeyboardButton(text='Правда 💬', callback_data='Правда')
		keyboard.add(key_new)
		key_pass = types.InlineKeyboardButton(text='Действие ✋', callback_data="Действие")
		keyboard.add(key_pass)

		bot.send_message(call.message.chat.id, lines[random.randint(0, len(lines) - 1)], reply_markup=keyboard)

		with open("data.json", "r") as file:
			data = json.load(file)
		if str(call.message.chat.id) in data:
			data[str(call.message.chat.id)]['truth'] += 1
		else:
			data[str(call.message.chat.id)] = {"never": 0, "truth": 0, "action": 0, "croco": 0}
			data[str(call.message.chat.id)]['truth'] += 1
		with open("data.json", "w") as file:
			json.dump(data, file)

	if call.data == "Действие":
		with open("action.txt", "r", encoding="utf-8") as file:
			lines = [line.rstrip() for line in file]
		keyboard = types.InlineKeyboardMarkup()
		key_new = types.InlineKeyboardButton(text='Правда 💬', callback_data='Правда')
		keyboard.add(key_new)
		key_pass = types.InlineKeyboardButton(text='Действие ✋', callback_data="Действие")
		keyboard.add(key_pass)

		bot.send_message(call.message.chat.id, lines[random.randint(0, len(lines) - 1)], reply_markup=keyboard)

		with open("data.json", "r") as file:
			data = json.load(file)
		if str(call.message.chat.id) in data:
			data[str(call.message.chat.id)]['action'] += 1
		else:
			data[str(call.message.chat.id)] = {"never": 0, "truth": 0, "action": 0, "croco": 0}
			data[str(call.message.chat.id)]['action'] += 1
		with open("data.json", "w") as file:
			json.dump(data, file)

	if call.data == "Croco":
		try:
			player = croco_players[call.message.chat.id]
			if len(player) > 1:
				bot.send_message(call.message.chat.id, f"Показывает игрок {player[random.randint(0, len(player) - 1)]}")
				with open("croco.txt", "r", encoding="utf-8") as file:
					lines = [line.rstrip() for line in file]
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text="Показать слово", callback_data="Croco"))

				bot.send_message(call.message.chat.id, f"Загаданное слово: {lines[random.randint(0, len(lines) - 1)]}", reply_markup=keyboard)

				with open("data.json", "r") as file:
					data = json.load(file)
				if str(call.message.chat.id) in data:
					data[str(call.message.chat.id)]['croco'] += 1
				else:
					data[str(call.message.chat.id)] = {"never": 0, "truth": 0, "action": 0, "croco": 0}
					data[str(call.message.chat.id)]['croco'] += 1
				with open("data.json", "w") as file:
					json.dump(data, file)

			else:
				bot.send_message(call.message.chat.id, "Нужно минимум 2 игрока")
				return

		except:
			bot.send_message(call.message.chat.id, "Добавьте игроков для игры")
			return

	if call.data == "Reload":
		with open("data.json", "r") as file:
			data = json.load(file)
		data[str(call.message.chat.id)] = {"never": 0, "truth": 0, "action": 0, "croco": 0}
		with open("data.json", "w") as file:
			json.dump(data, file)
		bot.send_message(call.message.chat.id, "Статистика успешно обнулена")
	if call.data == "Menu":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

		item1 = types.KeyboardButton("Я никогда не...")
		item2 = types.KeyboardButton("Правда или действие")
		item3 = types.KeyboardButton("Крокодил 🐊")

		markup.add(item1, item2, item3)
		bot.send_message(call.message.chat.id, "Добро пожаловать, выберите игру", reply_markup=markup)


#
# def create_game_croco(message):
# 	try:
# 		count = int(message.text)
# 		print(message.chat.id)
# 		data = {str(message.chat.id): {1: 0}}
# 		for i in range(1, count):
# 			data[str(message.chat.id)].update({i+1: 0})
# 		print(data)
# 		with open('data.json', 'a+') as f:
# 			try:
# 				json_data = json.load(f)
# 				json_data.write(data)
# 			except:
# 				json_data.write(data)
# 		start_user_to_game(message)
# 	except:
# 		print("Error")


bot.polling(none_stop=True)
