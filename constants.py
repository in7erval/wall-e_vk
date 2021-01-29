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