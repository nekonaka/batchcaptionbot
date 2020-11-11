import telebot
from telebot import apihelper


TOKEN = ''
 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! \n\nI can add, replace or clear media file captions in batch mode. \n\nI support audio, video, photo, document and voice attachments. \n\nUse /setcaption to start and follow the instructions.')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'I can add, replace or clear media file captions in batch mode. \n\nI support audio, video, photo, document and voice attachments. \n\nUse /setcaption to start and follow the instructions.')

caption = ''
fileid = ''

@bot.message_handler(content_types=['text'])
def setcaption(message):
	if message.text == '/setcaption':
		bot.send_message(message.from_user.id, "Send text is you want to add/replace the caption to files. You can use hashtags, channel/group/user tags, URLs and multiple lines of text.\n\nUse /clearcaption to remove caption from files.")
		bot.register_next_step_handler(message, get_caption)
	else:
		bot.send_message(message.from_user.id, 'Use /setcaption to start caption editing');

@bot.message_handler(content_types=['text'])
def get_caption(message): 
	global caption
	if message.text == '/clearcaption':
		caption = ''
		bot.send_message(message.from_user.id, "Ok, now send me the files and their captions will be erased")
		bot.register_next_step_handler(message, get_files_to_clear) 
	else:
		caption = message.text
		bot.send_message(message.from_user.id, 'Caption set. Now send or forward me the file(s). \n\nUse /setcaption again to change editing settings')
		bot.register_next_step_handler(message, get_files)

@bot.message_handler(content_types=['audio','document','video','voice','photo'])
def get_files(message):
	global fileid
	if message.content_type == 'audio':
		fileid = message.audio.file_id
		bot.send_audio(message.chat.id, fileid, caption = caption)
	elif message.content_type == 'video':
		fileid = message.video.file_id
		bot.send_video(message.chat.id, fileid, caption = caption)
	elif message.content_type == 'document':
		fileid = message.document.file_id
		bot.send_document(message.chat.id, fileid, caption = caption)
	elif message.content_type == 'voice':
		fileid = message.voice.file_id
		bot.send_voice(message.chat.id, fileid, caption = caption)
	elif message.content_type == 'photo':
		fileid = message.photo[-1].file_id
		bot.send_photo(message.chat.id, fileid, caption = caption)
	else:
		bot.send_message(message.from_user.id, 'Sorry, this media type is not supported');	

@bot.message_handler(content_types=['audio','document','video','voice','photo'])
def get_files_to_clear(message):
	global fileid
	if message.content_type == 'audio':
		fileid = message.audio.file_id
		bot.send_audio(message.chat.id, fileid)
	elif message.content_type == 'video':
		fileid = message.video.file_id
		bot.send_video(message.chat.id, fileid)
	elif message.content_type == 'document':
		fileid = message.document.file_id
		bot.send_document(message.chat.id, fileid)
	elif message.content_type == 'voice':
		fileid = message.voice.file_id
		bot.send_voice(message.chat.id, fileid)
	elif message.content_type == 'photo':
		fileid = message.photo[-1].file_id
		bot.send_photo(message.chat.id, fileid)
	else:
		bot.send_message(message.from_user.id, 'Sorry, this media type is not supported');











 

bot.polling()
