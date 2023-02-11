import os
import telebot
from handy import *
from welcoming import w_text

# defining my api key
API_TOKEN = os.environ["BOT_TOKEN"]
Provider_Token = os.environ["PROVIDER_TOKEN"]
Owner_Password = os.environ["PASSWORD"]

# making my bot object
bot = telebot.TeleBot(API_TOKEN)

# defining the keyboard mark-up and the text corresponding to each message
outputs = {
    "/start": {
        "buttons": [
            "Find Product",
            "Add Product",
            "My Cart",
            "My Products",
            "Bought Products",
            "My Balance",
            "Report An Issue",
        ],
        "text": "Main Menu: ",
    },
    "Find Product": {
        "buttons": ["Show All Products", "Search", "Back To Menu"],
        "text": "you can see all the posted products or use the search",
    },
}

search_text = {}


# making keyboard object
def buttons_input(chat_id, message_text):
    """take a message object and return the appropriate text and mark-up"""

    # creating the general mark-up properties
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True
    )
    buttons_list = []

    # handle any message that is defined in the output dictionary
    if message_text in outputs.keys():
        buttons_list = outputs[message_text]["buttons"]
        text = outputs[message_text]["text"]
        i = 0
        while i < len(buttons_list):
            try:
                markups = [
                    telebot.types.KeyboardButton(j) for j in buttons_list[i : i + 2]
                ]
                markup.add(*markups)
            except:
                markup.add(buttons_list[-1])
            i += 2
        if message_text == "/start" and is_admin(chat_id):
            markup.add(telebot.types.KeyboardButton("Pending Posts"))
            markup.add(telebot.types.KeyboardButton("Close Payment"))
            markup.add(telebot.types.KeyboardButton("Send Notification"))

        if message_text == "/start" and is_owner(chat_id):
            markup.add(telebot.types.KeyboardButton("Add Admin"))
            markup.add(telebot.types.KeyboardButton("Remove Admin"))
            markup.add(telebot.types.KeyboardButton("Show Admins"))

        msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        return msg

    # adding the button of cancelling a process
    elif message_text == "Add Product":
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add("Cancel!")
        msg = bot.send_message(
            chat_id=chat_id,
            text="You Can Cancel this Process By Writing 'Cancel!' or Using The Below Cancel Button",
            reply_markup=markup,
        )
        return
    else:
        return


# the start of the steps functions of adding a product
def add_product(message):
    """starting the process by asking for the name of the product"""

    msg = bot.send_message(message.chat.id, "what's the name of your product?")

    # registration for a next step
    bot.register_next_step_handler(msg, process_product_name)


# handling the product name
def process_product_name(message):
    """checking the name of the product"""

    # rejected not-text message
    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID TEXT")
        bot.register_next_step_handler(msg, process_product_name)
        return

    # cancel if the user asked to
    elif message.text == "Cancel!":
        cancelling(message)
        return

    # asking for a new name if it's too long
    if len(message.text) > 30:
        msg = bot.send_message(
            message.chat.id,
            "that's too long for a name, please change it to a brief one:",
        )
        bot.register_next_step_handler(msg, process_product_name)

    else:
        product_name = message.text
        sql(
            "INSERT INTO products(name, owner_id) VALUES (?, ?)",
            (product_name, message.chat.id),
        )
        msg = bot.send_message(
            message.chat.id,
            "Great! now add the price in $USD currency\n\nNOTE:\nWhen someone buy your product we cut 2.5$ from the price as fees and the rest is added to your balance",
        )
        bot.register_next_step_handler(msg, process_product_price)


# handling the product price
def process_product_price(message):
    """handling the price"""

    # rejected not-text message
    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID PRICE")
        bot.register_next_step_handler(msg, process_product_price)
        return

    # cancel if the user asked to
    elif message.text == "Cancel!":
        cancelling(message)
        return

    # check if message is a valid number
    try:
        product_price = round(float(message.text), 2)
    # if not a number, then ask to re-enter
    except:
        msg = bot.send_message(
            message.chat.id,
            "OH a price must be number, please re-enter a valid price number:",
        )
        bot.register_next_step_handler(msg, process_product_price)
        return

    if product_price < 5:
        msg = bot.send_message(
            message.chat.id,
            "SORRY, The price can't be less than 5 dollars\nplease enter a price that's more than 5$",
        )
        bot.register_next_step_handler(msg, process_product_price)
        return
    elif product_price > 10000:
        msg = bot.send_message(
            message.chat.id,
            "SORRY, The price can't be more than 10,000 dollars\nplease enter a price that's less than 10,000$",
        )
        bot.register_next_step_handler(msg, process_product_price)
        return

    # adding price to database
    sql(
        "UPDATE products SET price = ? WHERE owner_id = ? AND photo_id IS NULL",
        (product_price, message.chat.id),
    )
    msg = bot.send_message(
        message.chat.id,
        "please now add a brief description that's between 30 and 120 letters:",
    )
    bot.register_next_step_handler(msg, process_product_desc)


# handling the description
def process_product_desc(message):
    """checking the name of the product"""

    # rejected not-text message
    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID TEXT")
        bot.register_next_step_handler(msg, process_product_desc)
        return

    # cancel if the user asked to
    elif message.text == "Cancel!":
        cancelling(message)
        return

    # the description
    desc = message.text
    # reject a long or short description
    if len(desc) < 30:
        msg = bot.send_message(
            message.chat.id, "the description can't be less than 30 letters:"
        )
        bot.register_next_step_handler(msg, process_product_desc)

    elif len(desc) > 120:
        msg = bot.send_message(
            message.chat.id, "the description can't be more than 120 letters:"
        )
        bot.register_next_step_handler(msg, process_product_desc)

    else:
        # adding description to database
        sql(
            "UPDATE products SET description = ? WHERE owner_id = ? AND photo_id IS NULL",
            (desc, message.chat.id),
        )
        msg = bot.send_message(message.chat.id, "what country is this product in:")
        bot.register_next_step_handler(msg, process_product_country)


# handling the country
def process_product_country(message):
    """handling the country"""

    # rejected not-text message
    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID TEXT")
        bot.register_next_step_handler(msg, process_product_country)
        return

    # cancel if the user asked to
    elif message.text == "Cancel!":
        cancelling(message)
        return

    # reject a too long country name
    elif len(message.text) > 25:
        msg = bot.send_message(message.chat.id, "that's too long for country name:")
        bot.register_next_step_handler(msg, process_product_country)

    else:
        country = message.text
        # adding country to the database
        sql(
            "UPDATE products SET country = ? WHERE owner_id = ? AND photo_id IS NULL",
            (country, message.chat.id),
        )
        msg = bot.send_message(message.chat.id, "at which city this product is?")
        bot.register_next_step_handler(msg, process_product_city)


# handling the city
def process_product_city(message):
    """handling the city"""

    # rejected not-text message
    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID TEXT")
        bot.register_next_step_handler(msg, process_product_city)
        return

    # cancel if the user asked to
    elif message.text == "Cancel!":
        cancelling(message)
        return
    # reject a too long city name
    elif len(message.text) > 25:
        msg = bot.send_message(message.chat.id, "that's too long for city name:")
        bot.register_next_step_handler(msg, process_product_city)

    else:
        city = message.text
        # adding country to the database
        sql(
            "UPDATE products SET city = ? WHERE owner_id = ? AND photo_id IS NULL",
            (city, message.chat.id),
        )
        msg = bot.send_message(
            message.chat.id, "Now please send a photo that best describes your product:"
        )
        bot.register_next_step_handler(msg, process_product_photo)


# handling the photo
def process_product_photo(message):
    """handling the photo of the product"""

    if message.content_type == "photo":
        photo_id = message.photo[0].file_id
        # adding photo_id to the database
        sql(
            "UPDATE products SET photo_id = ? WHERE owner_id = ? AND photo_id IS NULL",
            (photo_id, message.chat.id),
        )
        bot.send_message(
            message.chat.id,
            "thanks for using our bot, we sent the request to the admins and when they approve it, it'll be showed for the public.\n\nPlease deliver the product to the nearest WW-Market stock\n\nNote that your post won't be approved in the following cases:\n1- if you didn't deliver the product within a week\n2- if the informations you included aren't descriptive and in this case you can either create a new post or visit our stock and take back your products",
        )
        buttons_input(message.chat.id, "/start")
        # telling the admins
        tell_admins(
            text=f"{message.chat.first_name} have added a product and is waiting for your approval!"
        )

    # cancel if the user asked to
    elif message.content_type == "text" and message.text == "Cancel!":
        cancelling(message)
        return

    else:
        msg = bot.send_message(message.chat.id, "please send a photo")
        bot.register_next_step_handler(msg, process_product_photo)


# the end of adding a product steps


# handling the show-pending-products-to-admins process
def pending_posts(message, next_product=0, my_message=0):
    """showing the unapproved posts for the admins so they can approve them"""

    pending_products = sql(
        "SELECT id, name, price, description, country, city, photo_id FROM products WHERE is_approved = 0"
    )
    list_len = len(pending_products)
    # if there's no pending posts left, let the admin know
    if list_len == 0:
        bot.send_message(message.chat.id, "NO PENDING POSTS LEFT")
        bot.delete_message(message.chat.id, message.id)
        return
    # if we got past beyond the last product then back to the first one
    elif next_product == list_len:
        index = 0
    else:
        index = next_product

    product = pending_products[index]
    post = make_post(product)
    product_id = pending_products[index][0]
    owner_id = sql("SELECT owner_id FROM products WHERE id = ?", (product_id,))
    text = post[0] + f"\n\nuser id {owner_id[0][0]}\n\n{list_len-1} Pending Posts Left"
    entities = post[1]
    photo_id = post[2]
    id = post[3]
    nex = index + 1
    if list_len == 1:
        inline_buttons = make_inlines(("Approve", f"A{id}"), ("DisApprove", f"D{id}"))
    else:
        inline_buttons = make_inlines(
            ("Approve", f"A{id}"), ("DisApprove", f"D{id}"), ("Next", f"N{nex}")
        )

    if my_message == 0:
        bot.delete_message(message.chat.id, message.id)
        bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_id,
            caption=text,
            reply_markup=inline_buttons,
            caption_entities=entities,
        )
    else:
        media = telebot.types.InputMediaPhoto(photo_id, caption=text)
        bot.edit_message_media(
            media, message.chat.id, message.id, reply_markup=inline_buttons
        )


# handling inlinecallqueries
def answercall(call):
    """take the appropriate actions for different queries"""
    data = call.data
    identifier = data[0]
    product_id = int(data[1:])
    chat_id = call.message.chat.id
    text = call.message.caption
    message_id = call.message.id
    # handling the 'approve' callback query
    if identifier == "A":
        owner_id = sql("SELECT owner_id FROM products WHERE id = ?", (product_id,))
        bot.send_message(
            owner_id[0][0],
            f"Your post with the text:\n{text[:-40]}\nWAS APPROVED BY THE ADMINS",
        )
        sql("UPDATE products SET is_approved = 1 WHERE id = ?", (product_id,))
        pending_posts(call.message, my_message=0)
    # handling the 'disapprove' callback query
    elif identifier == "D":
        owner_id = sql("SELECT owner_id FROM products WHERE id = ?", (product_id,))
        bot.send_message(
            owner_id[0][0],
            f"Your post with the text:\n\n{text[:-40]}\n\nWAS REJECTED BY THE ADMINS",
        )

        sql("DELETE FROM products WHERE id = ?", (product_id,))
        pending_posts(call.message)
    # handling the 'next' callback query for unapproved products
    elif identifier == "N":
        pending_posts(call.message, product_id, my_message=1)

    # handling the 'next' callback query for show all posts
    elif identifier == "F":
        show_all_products(call.message, product_id, 1)

    # handling 'next' callback query for search
    elif identifier == "T":
        post_search(call.message, 1, product_id, 1)

    # handling next callback query for show user products
    elif identifier == "L":
        show_user_products(call.message, product_id, 1)

    # handling next post for cart
    elif identifier == "X":
        show_cart(call.message, product_id, 1)

    # handling next post for cart
    elif identifier == "O":
        show_history(call.message, product_id, 1)

    # handling the 'previous' callback query for show all posts
    elif identifier == "P":
        show_all_products(call.message, product_id, 1)

    # handling 'previous' callback query for search
    elif identifier == "S":
        post_search(call.message, 1, product_id, 1)

    # handling previous callback query for cart
    elif identifier == "Z":
        show_cart(call.message, product_id, 1)

    # handling previous callback query for cart
    elif identifier == "K":
        show_user_products(call.message, product_id, 1)

    # handling previous callback query for cart
    elif identifier == "I":
        show_history(call.message, product_id, 1)

    # handling 'Buy' callback query
    elif identifier == "B":
        owner_id = sql("SELECT owner_id FROM products WHERE id = ?", (product_id,))
        # if the user trying to buy their own product
        if chat_id == owner_id[0][0]:
            bot.send_message(chat_id, "OPS, YOU CAN'T BUY YOUR OWN PRODUCTS")
        else:
            make_payment(chat_id, product_id)

    # handling the Add-to-cart callback query
    elif identifier == "C":
        add_to_cart(chat_id, product_id, call)

    # handling the 'Remove' callback query in cart
    elif identifier == "R":
        sql(
            "DELETE FROM cart WHERE product_id = ? AND user_id = ?",
            (product_id, chat_id),
        )
        show_cart(call.message, removing=1)

    # handling the 'Remove' callback query in cart
    elif identifier == "H":
        sql("DELETE FROM history WHERE id = ?", (product_id,))
        show_history(call.message, removing=1)

        # handling the 'Remove' callback query in all_products
    elif identifier == "Y":
        sql("DELETE FROM products WHERE id = ?", (product_id,))

        sql("DELETE FROM history WHERE product_id = ?", (product_id,))
        show_all_products(call.message, removing=1)


# the start of find-product steps
# handling find product
def find_product(message):
    """make the appropriate response when the user hits the Find_product button"""
    msg = buttons_input(message.chat.id, message.text)
    bot.register_next_step_handler(msg, process_prduct_showing)


def process_prduct_showing(message):
    if message.text == "Show All Products":
        show_all_products(message)
        buttons_input(message.chat.id, "/start")

    elif message.text == "Search":
        buttons_input(message.chat.id, "Add Product")
        msg = bot.send_message(message.chat.id, "Enter your search word:")
        bot.register_next_step_handler(msg, tempo_search_func)

    elif message.text == "Back To Menu":
        buttons_input(message.chat.id, "/start")

    else:
        msg = bot.send_message(
            message.chat.id,
            "Ops, seems like an invalid input\nPlease choose one of the below buttons",
        )
        bot.register_next_step_handler(msg, process_prduct_showing)


# showing all approved posts for the user
def show_all_products(message, next_product=0, my_message=0, removing=0):
    """showing the approved posts to the user"""

    approved_products = sql(
        "SELECT id, name, price, description, country, city, photo_id FROM products WHERE is_approved = 1"
    )
    list_len = len(approved_products)
    # if there's no posts , let the user know
    if list_len == 0:
        bot.delete_message(message.chat.id, message.id)
        msg = bot.send_message(message.chat.id, "There are No Posts yet")
        return msg
    # if we got past beyond the last product then back to the first one
    if next_product == list_len:
        index = 0
    elif next_product < 0:
        index = list_len - 1
    else:
        index = next_product

    product = approved_products[index]
    post = make_post(product)
    text = post[0] + f"\n\nthe post {index + 1} of {list_len} posts"
    entities = post[1]
    photo_id = post[2]
    id = post[3]
    nex = index + 1
    pre = index - 1
    inlines1 = [("Add To Cart", f"C{id}"), ("Buy", f"B{id}")]
    inlines2 = [
        ("Add To Cart", f"C{id}"),
        ("Buy", f"B{id}"),
        ("Previous", f"P{pre}"),
        ("Next", f"F{nex}"),
    ]
    if is_admin(message.chat.id):
        inlines1.append(("Delete", f"Y{id}"))
        inlines2.append(("Delete", f"Y{id}"))

    if list_len == 1:
        inline_buttons = make_inlines(*inlines1)
    else:
        inline_buttons = make_inlines(*inlines2)

    if my_message == 0 or removing == 1:
        bot.delete_message(message.chat.id, message.id)
        msg = bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_id,
            caption=f"{text}",
            reply_markup=inline_buttons,
            caption_entities=entities,
        )
        return msg
    else:
        media = telebot.types.InputMediaPhoto(photo_id, caption=text)
        bot.edit_message_media(
            media, message.chat.id, message.id, reply_markup=inline_buttons
        )


def tempo_search_func(message):
    post_search(message)


# handling searching for post
def post_search(message, search_w=0, next_product=0, my_message=0):
    """show the user all the posts that contains his search word"""
    if message.text == "Cancel!":
        cancelling(message)
        return
    if search_w == 0:
        search_word = message.text
        sql("UPDATE users SET last_sw = ? WHERE id = ?", (search_word, message.chat.id))

    else:
        last_sw = sql("SELECT last_sw FROM users WHERE id = ?", (message.chat.id,))
        search_word = last_sw[0][0]

    approved_products = sql(
        "SELECT id, name, price, description, country, city, photo_id FROM products WHERE is_approved = 1 AND id IN (SELECT id FROM products WHERE description LIKE ? OR name LIKE ? OR city LIKE ? OR country LIKE ?)",
        (
            f"%{search_word}%",
            f"%{search_word}%",
            f"%{search_word}%",
            f"%{search_word}%",
        ),
    )
    list_len = len(approved_products)
    # if there's no posts, let the user know
    if list_len == 0:
        bot.send_message(message.chat.id, "No Results")
        buttons_input(message.chat.id, "/start")

        return
    # if we got past beyond the last product then back to the first one
    elif next_product == list_len:
        index = 0
    elif next_product < 0:
        index = list_len - 1
    else:
        index = next_product

    product = approved_products[index]
    post = make_post(product)
    text = post[0] + f"\n\nThe product {index + 1} of {list_len} products"
    entities = post[1]
    photo_id = post[2]
    id = post[3]
    nex = index + 1
    pre = index - 1
    if list_len == 1:
        inline_buttons = make_inlines(("Add To Cart", f"C{id}"), ("Buy", f"B{id}"))
    else:
        inline_buttons = make_inlines(
            ("Add To Cart", f"C{id}"),
            ("Buy", f"B{id}"),
            ("Previous", f"S{pre}"),
            ("Next", f"T{nex}"),
        )
    if my_message == 0:
        bot.delete_message(message.chat.id, message.id)
        msg = bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_id,
            caption=text,
            reply_markup=inline_buttons,
            caption_entities=entities,
        )
        buttons_input(message.chat.id, "/start")
    else:
        media = telebot.types.InputMediaPhoto(photo_id, caption=text)
        bot.edit_message_media(
            media, message.chat.id, message.id, reply_markup=inline_buttons
        )


# sending the invoice to the user
def make_payment(chat_id, product_id):
    # product infos
    data = sql(
        "SELECT name, description, price From products WHERE id = ?", (product_id,)
    )
    name = data[0][0]
    price = data[0][2]
    description = data[0][1]
    # make price
    prices = [
        telebot.types.LabeledPrice(label=name, amount=int(price * 100)),
        telebot.types.LabeledPrice(label="fees", amount=int(250)),
    ]
    # sending the invoice
    bot.send_invoice(
        chat_id,
        name,
        description,
        f"{product_id}",
        Provider_Token,
        "USD",
        prices,
        is_flexible=True,
    )


# the appropriate action for successful payment
def payment_action(message):
    # defining variables
    chat_id = message.chat.id
    payment = message.successful_payment
    option = payment.shipping_option_id
    product_id = int(payment.invoice_payload)
    charg_id = payment.provider_payment_charge_id
    amount = payment.total_amount
    if option == "delivery":
        amount = amount - 500
    # updating the user history
    sql(
        "INSERT INTO history (user_id, product_id, charge_id) VALUES(?, ?, ?)",
        (chat_id, product_id, charg_id),
    )
    sql(
        "UPDATE users SET balance = balance + ? WHERE id = (select owner_id FROM products WHERE id = ?)",
        (((amount - 500) / 100), product_id),
    )
    product_data = sql(
        "SELECT owner_id, name FROM products WHERE id = ?", (product_id,)
    )
    # notify user
    if option == "delivery":
        bot.send_message(
            chat_id,
            "Your product will be delivered within a week\n\nThanks for using our market",
        )
    elif option == "pickup":
        bot.send_message(
            chat_id,
            "Thanks for using our market\n\nThe product will be in our center that resides in your city within 5 days",
        )
    bot.send_message(
        chat_id,
        "YOU SHOULD GIVE THE FOLLOWING CODE TO OUR EMPLOYEES TO RECEIVE YOUR PRODUCT\nSO PLEASE KEEP THE CODE IN A SAFE PLACE\n\n",
    )
    entities = [
        telebot.types.MessageEntity("spoiler", 0, len(charg_id)),
        telebot.types.MessageEntity("code", 0, len(charg_id)),
    ]
    bot.send_message(chat_id, charg_id, entities=entities)
    # tell the product owner
    bot.send_message(
        product_data[0][0],
        f"HEY, SOMEONE HAS JUST BOUGHT {product_data[0][1]} FROM YOU, AND THE AMOUNT IS ADDED TO YOUR BALANCE",
    )
    tell_admins(
        f"THE USER {product_data[0][0]} HAS JUST BOUGHT {product_data[0][1]} FROM {chat_id} "
    )


# show all the products that in the user's cart
def show_cart(message, next_product=0, my_message=0, removing=0):
    """showing the approved posts to the user"""

    cart_products = sql(
        "SELECT id, name, price, description, country, city, photo_id FROM products WHERE id in (SELECT product_id FROM cart WHERE user_id = ?)",
        (message.chat.id,),
    )
    list_len = len(cart_products)
    # if the cart is empty
    if list_len == 0:
        bot.delete_message(message.chat.id, message.id)
        msg = bot.send_message(message.chat.id, "YOUR CART IS EMPTY")
        return
    # if we got past beyond the last product then back to the first one
    elif next_product == list_len:
        index = 0
    elif next_product < 0:
        index = list_len - 1
    else:
        index = next_product

    product = cart_products[index]
    post = make_post(product)
    text = post[0] + f"\n\nthe product {index + 1} of {list_len}"
    entities = post[1]
    photo_id = post[2]
    id = post[3]
    nex = index + 1
    pre = index - 1

    if list_len == 1:
        inline_buttons = make_inlines(("Buy", f"B{id}"), ("Remove", f"R{id}"))
    else:
        inline_buttons = make_inlines(
            ("Buy", f"B{id}"),
            ("Remove", f"R{id}"),
            ("Previous", f"Z{pre}"),
            ("Next", f"X{nex}"),
        )

    if my_message == 0 or removing == 1:
        bot.delete_message(message.chat.id, message.id)
        msg = bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_id,
            caption=f"{text}",
            reply_markup=inline_buttons,
            caption_entities=entities,
        )
    else:
        media = telebot.types.InputMediaPhoto(photo_id, caption=text)
        bot.edit_message_media(
            media, message.chat.id, message.id, reply_markup=inline_buttons
        )


# adding a product to cart
def add_to_cart(chat_id, product_id, call):
    """adding product to user's cart"""
    user_cart = sql(
        "SELECT user_id, product_id FROM cart WHERE user_id = ?", (chat_id,)
    )
    if (chat_id, product_id) in user_cart:
        bot.send_message(chat_id, "PRODUCT IS ALREADY IN YOUR CART")
    else:
        sql(
            "INSERT INTO cart (user_id, product_id) VALUES (?, ?)",
            (chat_id, product_id),
        )
        bot.send_message(chat_id, "PRODUCT IS ADDED TO YOUR CART")


# handling showing user's posts
def show_user_products(message, next_product=0, my_message=0):
    """showing the user all his posts"""

    user_products = sql(
        "SELECT id, name, price, description, country, city, photo_id FROM products WHERE is_approved = 1 AND owner_id = ?",
        (message.chat.id,),
    )
    list_len = len(user_products)
    # if there's no posts, let the user know
    if list_len == 0:
        msg = bot.send_message(message.chat.id, "YOU DIDN'T OFFER ANY PRODUCTS YET")
        return
    # if we got past beyond the last product then back to the first one
    elif next_product == list_len:
        index = 0
    elif next_product < 0:
        index = list_len - 1
    else:
        index = next_product

    product = user_products[index]
    post = make_post(product)
    text = post[0] + f"\n\nthe post {index + 1} of {list_len} posts"
    entities = post[1]
    photo_id = post[2]
    id = post[3]
    nex = index + 1
    pre = index - 1

    if list_len > 1:
        inline_buttons = make_inlines(("Previous", f"K{pre}"), ("Next", f"L{nex}"))

    else:
        inline_buttons = None

    if my_message == 0:
        bot.delete_message(message.chat.id, message.id)
        msg = bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_id,
            caption=f"{text}",
            reply_markup=inline_buttons,
            caption_entities=entities,
        )
        return msg
    else:
        media = telebot.types.InputMediaPhoto(photo_id, caption=text)

        bot.edit_message_media(
            media, message.chat.id, message.id, reply_markup=inline_buttons
        )


# showing buying history
def show_history(message, next_product=0, my_message=0, removing=0):
    """showing the user history"""

    history_data = sql(
        "SELECT product_id , id, done FROM history WHERE user_id = ?",
        (message.chat.id,),
    )

    list_len = len(history_data)

    # if we got past beyond the last product then back to the first one
    if next_product == list_len:
        index = 0
    elif next_product < 0:
        index = list_len - 1
    else:
        index = next_product

    if list_len == 0:
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, "YOUR HISTORY IS EMPTY")
        return

    # if the history is empty
    else:
        bought_products = sql(
            "SELECT id, name, price, description, country, city, photo_id FROM products WHERE id = ?",
            (history_data[index][0],),
        )

    product = bought_products[0]
    post = make_post(product)
    is_done = history_data[index][2]
    if is_done == 0:
        delivered = "UNDELIVERED"
    else:
        delivered = "DELIVERED"
    text = post[0] + f"\n\n{delivered}" + f"\n\nthe product {index + 1} of {list_len}"
    entities = post[1]
    photo_id = post[2]
    id = history_data[index][1]
    nex = index + 1
    pre = index - 1

    if list_len == 1:
        if is_done == 1:
            inline_buttons = make_inlines(("Delete", f"H{id}"))
        else:
            inline_buttons = None
    else:
        if is_done == 1:
            inline_buttons = make_inlines(
                ("Previous", f"I{pre}"), ("Next", f"O{nex}"), ("Delete", f"H{id}")
            )
        else:
            inline_buttons = make_inlines(("Previous", f"I{pre}"), ("Next", f"O{nex}"))

    if my_message == 0 or removing == 1:
        bot.delete_message(message.chat.id, message.id)
        msg = bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_id,
            caption=f"{text}",
            reply_markup=inline_buttons,
            caption_entities=entities,
        )
    else:
        media = telebot.types.InputMediaPhoto(photo_id, caption=text)
        bot.edit_message_media(
            media, message.chat.id, message.id, reply_markup=inline_buttons
        )


# show the user balance
def show_balance(message):
    balance = sql("SELECT balance FROM users WHERE id = ?", (message.chat.id,))
    if balance[0][0] == 0:
        bot.send_message(
            message.chat.id,
            "YOUR BALANCE IS ZERO\n\nYOU SHOULD TRY TO SELL SOMETHING IN OUR MARKET :)",
        )
    else:
        bot.send_message(
            message.chat.id,
            f"YOUR BALANCE IS {balance[0][0]}\n\nPlease visit our nearest center to withdraw your balance",
        )


# handling the issue report key
def report_issue(message):
    """forward the issue of the user to the admins"""
    msg = bot.send_message(
        message.chat.id,
        "ARE YOU FACING ANY ISSUES WHILE USING OUR MARKET?"
        "\nPlease send a descriptive and informative message about the problem you had so we can solve it appropriately",
    )
    # use the add-product Cancel! button to cancel here too
    buttons_input(message.chat.id, "Add Product")

    # registration for a next step
    bot.register_next_step_handler(msg, process_issue)


def process_issue(message):
    """handling the issue message"""

    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID TEXT")
        bot.register_next_step_handler(msg, process_issue)

    elif message.text == "Cancel!":
        cancelling(message)
        return

    else:
        bot.send_message(
            message.chat.id,
            "THANKS FOR CONTACTING WITH US\n\nPlease note that our admins will never contact you first so pay attention from scammers.\n\nif our admins needed to contact with you, you will get a notification through this bot with the username of the admin that you should contact with.",
        )
        entities = [telebot.types.MessageEntity("code", 9, len(str(message.chat.id)))]
        tell_admins(
            f"the user {message.chat.id} sent a report that says\n\n{message.text}",
            entities,
        )
        buttons_input(message.chat.id, "/start")


# handling the close-payment button
def close_payment(message):
    """close payment when user receive the product"""
    msg = bot.send_message(message.chat.id, "SEND THE CHARGE CODE")
    buttons_input(message.chat.id, "Add Product")
    bot.register_next_step_handler(msg, close_payment_process)


def close_payment_process(message):
    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID CODE")
        bot.register_next_step_handler(msg, close_payment_process)
        return

    elif message.text == "Cancel!":
        cancelling(message)
        return

    chat_id = message.chat.id
    code = (message.text,)
    all_payments = sql("SELECT charge_id FROM history")
    unclosed_payments = sql("SELECT charge_id FROM history WHERE done = 0")
    closed_payments = sql("SELECT charge_id FROM history WHERE done = 1")
    if code not in all_payments:
        bot.send_message(chat_id, "THIS CODE IS NOT IN OUR DATABASE")
    elif code in closed_payments:
        bot.send_message(chat_id, "THIS CODE IS ALREADY CLOSED")
    elif code in unclosed_payments:
        sql("UPDATE history SET done = 1 WHERE charge_id IS ?", code)
        bot.send_message(chat_id, "THE PAYMENT HAS BEEN CLOSED SUCCESSFULLY")
    buttons_input(chat_id, "/start")


# handling the send notification button
def send_nf(message):
    """send notification to user"""
    buttons_input(message.chat.id, "Add Product")
    msg = bot.send_message(message.chat.id, "SEND THE USER ID")
    bot.register_next_step_handler(msg, send_nf_process)


def send_nf_process(message):
    chat_id = message.chat.id

    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID USER ID")
        bot.register_next_step_handler(msg, send_nf_process)
        return

    elif message.text == "Cancel!":
        cancelling(message)
        return

    try:
        int(message.text)
    except:
        msg = bot.send_message(
            chat_id, "USER ID MUST BE A NUMBER, PLEASE ENTER A VALID ID"
        )
        bot.register_next_step_handler(msg, send_nf_process)
        return

    user_id = (int(message.text),)
    all_users_ids = sql("SELECT id FROM users")

    if user_id not in all_users_ids:
        bot.send_message(chat_id, "THIS USER IS NOT ONE OF OUR USERS")
        buttons_input(chat_id, "/start")

    else:
        msg = bot.send_message(chat_id, "WRITE A MESSAGE TO BE SENT TO THIS USER")
        bot.register_next_step_handler(msg, send_nf_message_process, user_id)


def send_nf_message_process(message, user_id):
    if message.text == "Cancel!":
        cancelling(message)
        return
    bot.send_message(user_id[0], "YOU HAVE A MESSAGE FROM THE ADMINS:")
    bot.copy_message(user_id[0], message.chat.id, message.id)
    buttons_input(message.chat.id, "/start")


# handling the bot when there's no owners
def no_owner_action(message):
    """handling everything when there's no owners"""
    msg = bot.send_message(
        message.chat.id,
        "THIS BOT IS NOT WORKING, BECAUSE THE OWNERS HAVEN'T VALIDATE THEMSELVES YET\n\n"
        "IF YOU'RE THE OWNER THEN PLEASE ADD THE RIGHT PASSWORD TO START THE BOT",
    )
    bot.register_next_step_handler(msg, process_owner_password)


# process the owner password:
def process_owner_password(message):
    """check if the password is right"""

    chat_id = message.chat.id
    # if the password is right
    if no_owner():
        if message.text == Owner_Password:
            name = get_fullname(message)
            sql(
                "INSERT INTO users (id, name, is_admin) VALUES(?, ?, ?) ",
                (chat_id, name, 2),
            )
            bot.send_message(chat_id, "YOU'RE NOW OFFICIALLY THE OWNER")
            buttons_input(chat_id, "/start")

        else:
            msg = bot.send_message(
                chat_id,
                "SEEMS LIKE YOU'RE NOT THE OWNER, PLEASE RESTART THE BOT WHEN THE OWNERS VALIDATE THEMSELVES, OR RE-ENTER THE PASSWORD:",
            )
            bot.register_next_step_handler(msg, process_owner_password)

    else:
        bot.send_message(
            chat_id,
            "THE OWNERS ARE ALREADY VALIDATED, HAVE A NICE TIME USING OUR MARKET :)",
        )
        if check_for_newuser(message):
            user_name = get_fullname(message)
            buttons_input(message.chat.id, "/start")
            bot.send_message(
                chat_id=message.chat.id,
                text=f"Hi, {user_name}\n THANKS FOR STARTING THE BOT\n\n{w_text}",
            )
            tell_admins(f"{user_name} has just started the bot!")
            buttons_input(chat_id, "/start")


# hanlding the add admin button
def add_admin(message):
    """add a new admin"""
    buttons_input(message.chat.id, "Add Product")
    msg = bot.send_message(message.chat.id, "SEND THE USER ID")
    bot.register_next_step_handler(msg, add_admin_process)


def add_admin_process(message):
    chat_id = message.chat.id

    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID USER ID")
        bot.register_next_step_handler(msg, add_admin_process)
        return

    elif message.text == "Cancel!":
        cancelling(message)
        return

    try:
        int(message.text)
    except:
        msg = bot.send_message(
            chat_id, "USER ID MUST BE A NUMBER, PLEASE ENTER A VALID ID"
        )
        bot.register_next_step_handler(msg, add_admin_process)
        return

    user_id = (int(message.text),)

    if not is_user(user_id[0]):
        bot.send_message(chat_id, "THIS USER IS NOT ONE OF OUR USERS")
        buttons_input(chat_id, "/start")

    elif is_admin(user_id[0]):
        bot.send_message(chat_id, "THIS USER IS ALREADY AN ADMIN")
        buttons_input(chat_id, "/start")

    else:
        sql("UPDATE users SET is_admin = 1 WHERE id = ?", user_id)
        bot.send_message(chat_id, "THIS USER IS NOW AN ADMIN")
        bot.send_message(user_id[0], "CONGRATS!, YOU'RE NOW ONE OF OUR ADMINS..")
        buttons_input(user_id[0], "/start")
        buttons_input(chat_id, "/start")


# handling remove admin button
def remove_admin(message):
    """remove an admin"""
    buttons_input(message.chat.id, "Add Product")
    msg = bot.send_message(message.chat.id, "SEND THE USER ID")
    bot.register_next_step_handler(msg, remove_admin_process)


def remove_admin_process(message):
    chat_id = message.chat.id

    if message.content_type != "text":
        msg = bot.send_message(message.chat.id, "PLEASE RE-SEND A VALID USER ID")
        bot.register_next_step_handler(msg, remove_admin_process)
        return

    elif message.text == "Cancel!":
        cancelling(message)
        return

    try:
        int(message.text)
    except:
        msg = bot.send_message(
            chat_id, "USER ID MUST BE A NUMBER, PLEASE ENTER A VALID ID"
        )
        bot.register_next_step_handler(msg, remove_admin_process)
        return

    user_id = int(message.text)

    if not is_user(user_id):
        bot.send_message(chat_id, "THIS IS NOT ONE OF OUR USERS AT ALL")
        buttons_input(chat_id, "/start")

    elif not is_admin(user_id):
        bot.send_message(chat_id, "THIS USER IS NOT AN ADMIN")
        buttons_input(chat_id, "/start")

    else:
        sql("UPDATE users SET is_admin = 0 WHERE id = ?", (user_id,))
        bot.send_message(chat_id, "THIS USER IS NO MORE AN ADMIN")
        bot.send_message(user_id, "SORRY, BUT YOU'RE NOT AN ADMIN WITH US ANYMORE :(")
        buttons_input(user_id, "/start")
        buttons_input(chat_id, "/start")


# handling the show_admins button
def show_admins(message):
    all_admins = sql("SELECT id , name FROM users WHERE is_admin = 1")
    if len(all_admins) == 0:
        bot.send_message(message.chat.id, "THERE ARE NO ADMINS")
        return
    for admin in all_admins:
        admin_id = admin[0]
        name = admin[1]
        entities = [telebot.types.MessageEntity("code", len(name) + 2, 11)]
        bot.send_message(message.chat.id, f"{name} : {admin_id}", entities=entities)


# the ending line.................
