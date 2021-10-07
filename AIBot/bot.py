import telebot
import config
from telebot import types
import dialogflow, json
import os
from google.api_core.exceptions import InvalidArgument

bot = telebot.TeleBot(config.TOKEN)

def bot_answer(message):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'YOUR_CREDENTIALS'

    DIALOGFLOW_PROJECT_ID = 'alishtelegram-nkmm'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = 'abc'

    text_to_be_analyzed = message

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    return response.query_result.fulfillment_text

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Hi, {0.first_name}! I am ChatBot based on Artificial Intelligence. Let's talk!".format(message.from_user), parse_mode='html')

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == "private":
        
        bot.send_message(message.chat.id, bot_answer(message.text))
        

    

# RUN
bot.polling(none_stop=True)