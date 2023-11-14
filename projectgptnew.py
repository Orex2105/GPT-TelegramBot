#telegram - 6447564053:AAENEbGde2fbQFw9SnnQn9n1wt2NdltOGlg
#gpt-4 - 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

import telebot
from telebot import types
import openai

import json

bot = telebot.TeleBot('6447564053:AAENEbGde2fbQFw9SnnQn9n1wt2NdltOGlg')
openai.api_key = "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"

channel_id = -1001809895051

def check_channel_membership(user_id):
    member = bot.get_chat_member(channel_id, user_id)
    return member.status != 'left'

admin_id = [5207913851]
access_users = [5207913851] # Для пользования ботом
zap = []

def load_bot_users():
    global access_users
    try:
        with open('bot_users.json', 'r') as file:
            return json.load(file)
    except:
        access_users = [5207913851]

def save_users(access_users):
    with open('bot_users.json', 'w') as file:
        json.dump(access_users, file)

load_bot_users()

@bot.message_handler(commands=['start']) 
def start(message):
    markup_inline = types.InlineKeyboardMarkup()
    mark = types.InlineKeyboardButton(text="Подписаться✅", url='https://t.me/gptopenchanel')
    markup_inline.add(mark)
    name = str(message.from_user.first_name)
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    if not check_channel_membership(user_id):
        bot.send_message(message.chat.id, 'Пожалуйста, подпишитесь на канал, чтобы продолжить использование бота.', reply_markup=markup_inline)
        return
        
    bot.send_message(-1001915494488, f'Пользователь @{user_name}({user_id}) зарегистрировался')
    bot.send_message(message.chat.id, f'Привет, {name}! Напиши свой запрос.')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKWSBlC0br2Bz6OPmsmHnYSK6U5PrewgACbwAD29t-AAGZW1Coe5OAdDAE')


@bot.message_handler(commands=['mes'])
def send_mes(message):
    user_id = message.chat.id
    if user_id in admin_id:
        try:
            user_id_to_message = int(message.text.split()[1].strip())
            message_text = message.text.split()[2:]
            bot.reply_to(message, 'Сообщение отправлено.')
            message_text = ' '.join(message_text)
            bot.send_message(user_id_to_message, message_text)
        except:
            bot.reply_to(message, 'Не удалось отправить сообщение. Пиишите по форме: /mes *ID человека* *текст сообщения*')
    else:
        bot.send_message(message.chat.id, "Вы не являетесь администратором.")


@bot.message_handler(commands=['ahelp'])
def a_help(message):
    user_id = message.from_user.id
    if user_id in admin_id:
        bot.reply_to(message, 'Список команд:\ngive_access - дать доступ к боту')
    else:
        bot.reply_to(message, 'У вас нет доступа к этой команде')



@bot.message_handler(commands=['give_access'])
def give_access(message):
    user_id = message.from_user.id
    if user_id in admin_id:
        try:
            new_access_user_id = int(message.text.split()[1].strip())
            access_users.append(new_access_user_id)
            bot.reply_to(message, f'Теперь пользователь {new_access_user_id} имеет доступ к боту.')
            bot.send_message(new_access_user_id, 'Теперь вы имеете доступ к боту.')
            save_users(access_users)
        except IndexError:
            bot.reply_to(message, 'Пожалуйста, укажите ID пользователя в команде.')
        except ValueError:
            bot.reply_to(message, 'ID пользователя должен быть числом.')
        except Exception as e:
            bot.send_message(message.chat.id, f'Что-то пошло не так: {e}')
    else:
        bot.reply_to(message, 'Вы не имеете доступ к этой команде.')


@bot.message_handler(func=lambda message: True)
def zapros(message):
    try:
        markup_inline_1 = types.InlineKeyboardMarkup()
        mark_1 = types.InlineKeyboardButton(text="Подписаться✅", url='https://t.me/gptopenchanel')
        markup_inline_1.add(mark_1)
        user_id = message.from_user.id
        user_name = str(message.from_user.username)
        markup_inline = types.InlineKeyboardMarkup()
        mark = types.InlineKeyboardButton(text="Ответь иначе", callback_data = 'yes')
        markup_inline.add(mark)
        if not check_channel_membership(user_id):
            bot.send_message(message.chat.id, 'Пожалуйста, подпишитесь на канал, чтобы продолжить использование бота.', reply_markup=markup_inline_1)
            return
        
        if user_id in access_users:
            bot.send_chat_action(message.chat.id, 'typing')
            input_text = message.text
            zap.append(input_text)
            
            if user_id != 5207913851:
                user_name = str(message.from_user.username)
                bot.send_message(-1001915494488, f'Пользователь @{user_name}({user_id}) спросил: {input_text}')

            reply_message = bot.send_message(message.chat.id, 'Запрос на обработке...')

            completion = openai.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {'role': 'system', 'content': 'Ты должен давать короткие, лакончиные ответы, если иного пользователь не просил!'},
                    {"role": "user", "content": input_text}
                ]
            )
            if user_id != 5207913851:
                bot.send_message(-1001915494488, f'ChatGPT ответил пользователю @{user_name}({user_id}): "{completion.choices[0].message.content}"')

            bot.delete_message(message.chat.id, reply_message.message_id)
            markup_inline = types.InlineKeyboardMarkup()
            mark = types.InlineKeyboardButton(text="Ответь иначе", callback_data='yes')
            markup_inline.add(mark)
            bot.reply_to(message, completion.choices[0].message.content, reply_markup=markup_inline)
        else:
            bot.send_message(message.chat.id, 'Вы не можете пользоваться ботом.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так: {e}')


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
model="gpt-4-1106-preview",
messages=[
    {
        'role': 'system', 'content': 'Ты должен давать короткие, лакончиные ответы, если иного пользователь не просил!',
        "role": "user", "content": new_zap,
    },
],
)
            bot.delete_message(call.message.chat.id, reply_message.message_id)
            bot.reply_to(call.message, completion.choices[0].message.content, reply_markup=markup_inline)
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Что-то пошло не так. {e}')
        
bot.polling()