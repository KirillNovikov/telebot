import telebot
import config
from telebot import apihelper
from telebot import types
from db import get_answers_from_db
from util import check_correction_of_exam, answer_to_list
import logging


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


bot = telebot.TeleBot(token=config.API_TOKEN, skip_pending=True)
apihelper.proxy = config.PROXY


auth_group_id = -492097584
#auth_group_id = -363820358 #test


start_testing_st = 'Начать тестирование'
another_try = 'Начать заново'
choose_another_var = 'Выбрать другой вариант'


start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
var_not_found_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_var = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
rm = types.ReplyKeyboardRemove()


start_markup.add(start_testing_st) 
var_not_found_markup.add(another_try)
change_var.add(choose_another_var)


def check_member(message):
	try:
		ch_m = bot.get_chat_member(auth_group_id, message.chat.id)
		if ch_m.status not in ('creator', 'member'):
			bot.send_message(message.chat.id, "Извините, но вы не состоите в чате.", reply_markup=rm)
			return True
		return False
	except Exception:
		bot.send_message(message.chat.id, "Ooops! Возникла ошибка.", reply_markup=rm)
		return True


def proceed_to_start(message):
	try:
		if message.text.split()[0] == '/start':
			start_bot(message)
			return True
		return False
	except Exception:
		return False


@bot.message_handler(commands=['start'])
def start_bot(message):
	if check_member(message):
		return
	args = message.text.split()
	if len(args) > 1:
		variant = args[1]
		msg = bot.send_message(message.chat.id, "Здравствуйте, сейчас начнется тестирование по варианту %s, который вы выбрали на канале.\nСледуйте инструкциям :-)" % variant, reply_markup=start_markup)
		bot.register_next_step_handler(msg, rt_start_testing, variant=variant)

	else:
		msg = bot.send_message(message.chat.id, "Здравствуйте, этот бот был создан для того, чтобы облегчить вашу подготовку к экзаменам.\nСледуйте инструкциям :-)", reply_markup=start_markup)
		bot.register_next_step_handler(msg, rt_start_testing)
	

format_of_ans = "Пожалуйста, введите ответы.\nФормат ответов:\n1 монополия\n2 124\n3 41234\n8 12\nПорядок ответов неважен."


@bot.message_handler(func = lambda msg: msg.text in (another_try, start_testing_st, choose_another_var, ))
def rt_start_testing(message, variant=None):
	if check_member(message):
		return
	if proceed_to_start(message):
		return
	if variant:
		msg = bot.send_message(message.chat.id, format_of_ans, reply_markup=rm)
		bot.register_next_step_handler(msg,rt_insert_ans, variant=variant)
	else:
		msg = bot.send_message(message.chat.id, "Введите свой вариант для того, чтобы начать!", reply_markup=rm)
		bot.register_next_step_handler(msg,rt_choose_variant)
	

def rt_choose_variant(message):
	if proceed_to_start(message):
		return
	if not message.text:
		rt_start_testing(message)
		return
	variant = message.text
	msg = bot.send_message(message.chat.id, format_of_ans, reply_markup=rm)
	bot.register_next_step_handler(msg, rt_insert_ans, variant=variant)
	

def rt_insert_ans(message,variant):
	if proceed_to_start(message):
		return
	bot.send_message(message.chat.id, "Сверяем с базой данных...")
	user_ans = message.text
	got_answers = False

	try:
		answers = get_answers_from_db(variant)
	except Exception:
		bot.send_message(message.chat.id, "К сожалению, такого варианта нет в базе.", reply_markup=var_not_found_markup)
		return
	
	try:
		list_of_user_answers = answer_to_list(user_ans)
	except Exception:
		bot.send_message(message.chat.id, "Неверный формат ответа, попробуйте снова.",reply_markup=change_var)
		return

	try:
		list_of_answers = answer_to_list(answers)
		result = check_correction_of_exam(list_of_answers,list_of_user_answers)
	except Exception:
		bot.send_message(message.chat.id, "Возникла ошибка, попробуйте снова.",reply_markup=change_var)
		return
	
	bot.send_message(message.chat.id, "Результат - %d/%d\n%s" % result,reply_markup=var_not_found_markup)
	
		
@bot.message_handler(content_types=['text'])
def handle_text(message):
	bot.send_message(message.chat.id, "Введите /start для начала тестирования.", reply_markup=rm)

if __name__ == "__main__":
	bot.polling(none_stop=True)
