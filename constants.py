SMALL = 5
MEDIUM = 15
LARGE = 80
BEGIN = "BEGIN"
END = "END"
LENGTH = 50
commands = {
	'help': 'Gives you information about the available commands',
	'history': 'Shows all messages',
	'reset_history': 'Delete all history messages',
	'my_id': 'return your id',
	'random_sentence': 'return random sentence',
	'large_random_sentence': 'return random sentence of ' + str(LARGE) + ' words',
	'medium_random_sentence': 'return random sentence of ' + str(MEDIUM) + ' words',
	'small_random_sentence': 'return random sentence of ' + str(SMALL) + ' words',
	'send_history': 'send file with history of messages',
	'send_dictionary': 'send file with dictionary',
	'tts': 'convert text to speech',
	'say_random_large': 'generates large voice message',
	'say_random': 'generates small voice message'
}

help_text = """
Привет!
-> Напиши 'бот кнопки' или 'бот пришли клавиатуру' или 'бот клавиатура', чтобы я прислал тебе клавиатуру. 
-> Я умею выбирать из нескольких вариантов. Напиши мне 'бот {что-то} или {что-то} или ...' и тогда я выберу один из вариантов. Пример: бот банан или яблоко или клубника
-> Могу предсказать вероятность чего-то. Напиши мне 'насколько {что-то}' и тогда я скажу вероятность этого. Пример: насколько возможно что дождь пойдёт сегодня
"""

sberkot_stickers = [19584, 55296, 55297, 20867, 50824,
					56586, 51347, 51603, 21656, 21402,
					53541, 51113, 20012, 52913, 20406,
					20279, 20663, 54327, 51258, 53694,
					21313, 50499, 53444, 20549, 54853,
					50121, 54474, 51022, 53966, 19411,
					19412, 19413, 19414, 19415, 19797,
					20181, 51548, 21216, 50402, 53858,
					21099, 20972, 50290, 50933, 21753,
					20732, 21501, 55295]
