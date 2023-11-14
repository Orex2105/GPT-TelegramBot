import telebot
from telebot import types #FOR BUTTONS
import openai
import json

bot = telebot.TeleBot('YOUR TELEGRAM TOKEN')
openai.api_key = "YOUR OPEN AI API KEY"

channel_id = 'YOUR CHANNEL' #DELETE IT IF YOU DON'T HAVE A SUBSCRIPTION CHANNEL

def check_channel_membership(user_id):
    member = bot.get_chat_member(channel_id, user_id)
    return member.status != 'left'

admin_id = ['YOUR ADMIN ID']
access_users = ['YOUR ID'] # TO USE THE BOT. DELETE IT IF YOUR BOT IS FREE
zap = []

def load_bot_users():
    global access_users
    try:
        with open('bot_users.json', 'r') as file:
            return json.load(file)
    except:
        access_users = ['YOUR DEFAULT ID']

def save_users(access_users):
    with open('bot_users.json', 'w') as file:
        json.dump(access_users, file)

load_bot_users()

@bot.message_handler(commands=['start']) 
def start(message):
    markup_inline = types.InlineKeyboardMarkup()
    mark = types.InlineKeyboardButton(text="YOUR TEXT", url='YOUR URL')
    markup_inline.add(mark)
    name = str(message.from_user.first_name)
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    if not check_channel_membership(user_id):
        bot.send_message(message.chat.id, 'YOUR TEXT', reply_markup=markup_inline)
        return
    bot.send_message(message.chat.id, f'YOUR TEXT')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKWSBlC0br2Bz6OPmsmHnYSK6U5PrewgACbwAD29t-AAGZW1Coe5OAdDAE')

@bot.message_handler(commands=['give_access'])
def give_access(message):
    user_id = message.from_user.id
    if user_id in admin_id:
        try:
            new_access_user_id = int(message.text.split()[1].strip())
            access_users.append(new_access_user_id)
            bot.reply_to(message, f'YOUR TEXT')
            bot.send_message(new_access_user_id, 'YOUR TEXT')
            save_users(access_users)
        except IndexError:
            bot.reply_to(message, 'YOUR TEXT')
        except ValueError:
            bot.reply_to(message, 'YOUR TEXT')
        except Exception as e:
            bot.send_message(message.chat.id, f'YOUR TEXT: {e}') #IF YOU WANT, DELETE {e}
    else:
        bot.reply_to(message, 'YOUR TEXT')


@bot.message_handler(func=lambda message: True)
def zapros(message):
    try:
        markup_inline_1 = types.InlineKeyboardMarkup()
        mark_1 = types.InlineKeyboardButton(text="YOUR TEXT", url='YOUR URL')
        markup_inline_1.add(mark_1)
        user_id = message.from_user.id
        user_name = str(message.from_user.username)
        markup_inline = types.InlineKeyboardMarkup()
        mark = types.InlineKeyboardButton(text="YOUR TEXT", callback_data = 'yes')
        markup_inline.add(mark)
        if not check_channel_membership(user_id):
            bot.send_message(message.chat.id, 'YOUR TEXT', reply_markup=markup_inline_1)
            return
        
        if user_id in access_users:
            bot.send_chat_action(message.chat.id, 'typing')
            input_text = message.text
            zap.append(input_text)

            reply_message = bot.send_message(message.chat.id, 'YOUR TEXT')

            completion = openai.chat.completions.create(
                model="gpt-4-1106-preview", #THIS IS A GPT-4 TURBO. CHANGE THE MODEL IF YOU WANT
                messages=[
                    {'role': 'system', 'content': 'YOUR TEXT'},
                    {"role": "user", "content": input_text}
                ]
            )

            bot.delete_message(message.chat.id, reply_message.message_id)
            markup_inline = types.InlineKeyboardMarkup()
            mark = types.InlineKeyboardButton(text="Ответь иначе", callback_data='yes')
            markup_inline.add(mark)
            bot.reply_to(message, completion.choices[0].message.content, reply_markup=markup_inline)
        else:
            bot.send_message(message.chat.id, 'YOUR TEXT')
    except Exception as e:
        bot.send_message(message.chat.id, f'YOUR TEXT: {e}') #IF YOU WANT, DELETE {e}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.message.from_user.id
    try:
        markup_inline = types.InlineKeyboardMarkup()
        mark = types.InlineKeyboardButton(text="Ответь иначе", callback_data = 'yes')
        markup_inline.add(mark)
        
        if call.data=='yes':
            new_zap = zap[-1]
            user_id = call.message.from_user.id
            
            reply_message = bot.send_message(call.message.chat.id, 'Запрос на обработке...')
            bot.send_chat_action(call.message.chat.id, 'typing')
            completion = openai.chat.completions.create(
model="gpt-4-1106-preview", #THIS IS A GPT-4 TURBO. CHANGE THE MODEL IF YOU WANT
messages=[
    {
        'role': 'system', 'content': 'YOUR TEXT',
        "role": "user", "content": new_zap,
    },
],
)
            bot.delete_message(call.message.chat.id, reply_message.message_id)
            bot.reply_to(call.message, completion.choices[0].message.content, reply_markup=markup_inline)
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Что-то пошло не так. {e}')
        
bot.polling()
