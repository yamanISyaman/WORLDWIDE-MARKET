import sqlite3
import telebot
import responses

def sql(query, vars = None):
    ''' executing the sql query with handling making a connection and closing it '''
    # connecting to the database
    connection = sqlite3.connect('data.db')
    # cursor
    cur = connection.cursor()
    # executing
    if vars != None:
        cur.execute(query, vars)
    else:
        cur.execute(query)
    connection.commit()
    data = cur.fetchall()
    connection.close()
    return data


def get_fullname(message):
    '''takes a message and return user's full name'''
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    if last_name == None:
        fullname = first_name
    else:
        fullname = first_name + ' '+ last_name 
    return fullname


def check_for_newuser(message):
    ''' user is new then add them to the list'''
    users_list = sql("SELECT id FROM users")
    users = []
    for i in users_list:
        users.append(i[0])
    if message.chat.id in users :
        return False
    else:
        sql("INSERT INTO users(id, name) VALUES (?, ?)", (message.chat.id, get_fullname(message)))
        return True


def cancelling(message):
    ''' handling the cleaning and directing when the use cancel the adding-product process'''
    
    markup = telebot.types.ReplyKeyboardRemove()
    responses.bot.send_message(chat_id=message.chat.id, text="--Process Is Cancelled--" , reply_markup=markup)
    responses.buttons_input(message.chat.id, "/start")
        # deleting the cancelled data
    sql("DELETE FROM products WHERE owner_id = ? AND photo_id IS NULL",(message.chat.id,))
    return


def is_admin(id):
    '''check if the user is admin or not'''
    admins = sql("SELECT id FROM users WHERE is_admin > 0")
    user = (id,)
    if user in admins:
        return True
    else:
        return False

def is_owner(id):
    '''check if the user is the owner or not'''
    admins = sql("SELECT id FROM users WHERE is_admin = 2")
    user = (id,)
    if user in admins:
        return True
    else:
        return False


def is_user(id):
    all_users_ids = sql("SELECT id FROM users")
    if (id,) in all_users_ids:
        return True
    else:
        return False

def no_owner():
    owners =sql("SELECT id FROM users WHERE is_admin = 2")
    if len(owners) == 0:
        return True
    else:
        return False

def make_inlines(*args):
    '''this function takes a tuples that contains button_text and callback data and returns '''
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for i in args:
        buttons.append(telebot.types.InlineKeyboardButton(i[0], callback_data=i[1]))
    counter = 0
    length = len(buttons)
    while counter + 2 <= length:
        markup.row(*buttons[counter:counter+ 2])
        counter += 2
    if length % 2 != 0:
        markup.add(buttons[-1])
    return markup


def make_post(data : tuple):
    '''every tuple should have (id, name, price, description, country, city, photo_id'''
    id = data[0]
    name = data[1]
    price = str(data[2])
    description = data[3]
    country = data[4]
    city = data[5]
    photo_id = data[6]

    text = f"{name}\n\n{price} $USD\n\n{description}\n\n{country} || {city}"
    entities = [telebot.types.MessageEntity("bold",0, len(name) + len(price) + 6), telebot.types.MessageEntity("italic" ,text.find(country), len(country) + len(city))]

    return (text, entities, photo_id, id)
        

def tell_admins(text=None, entities=None):
    ''' sends text to admins and returns a list of admins IDs '''
    admins_sql = sql("SELECT id FROM users WHERE is_admin > 0")
    admins = []
    for admin in admins_sql:
        admins.append(admin[0])
        if text != None:
            if entities == None:
                responses.bot.send_message(chat_id=admin[0], text=text)
            else:
                responses.bot.send_message(chat_id=admin[0], text=text, entities=entities)
    return admins
