# importing libraries
import telebot
from responses import *
from handy import *
from welcoming import w_text

    


# handling any input
@bot.message_handler(content_types=['photo', 'text'])
def action(message):
    '''making an appropriate response for every message'''

    if no_owner():
        no_owner_action(message)
    # greeting new users
    elif check_for_newuser(message):
        user_name = get_fullname(message)
        buttons_input(message.chat.id, "/start")
        bot.send_message(chat_id=message.chat.id, text=f"Hi, {user_name}\n THANKS FOR STARTING THE BOT\n\n{w_text}")
        tell_admins(f"{user_name} has just started the bot!")
    # display buttons when it must to
    elif message.text == "/start":
        buttons_input(message.chat.id, message.text)

    # do the process of adding a product when the user asks to
    elif message.text == 'Add Product':
        buttons_input(message.chat.id, message.text)
        add_product(message)

    # showing posts when adimn asks to
    elif message.text == "Pending Posts" and is_admin(message.chat.id): 
        pending_posts(message)

    elif message.text == "Find Product":
        find_product(message)

    elif message.text == "My Cart":
        show_cart(message)

    elif message.text == "My Products":
        show_user_products(message)

    elif message.text == "Bought Products":
        show_history(message)

    elif message.text == "My Balance":
        show_balance(message)

    elif message.text == "Report An Issue":
        report_issue(message)

    elif message.text == "Close Payment" and is_admin(message.chat.id):
        close_payment(message)

    elif message.text == "Send Notification" and is_admin(message.chat.id):
        send_nf(message)

    elif message.text == "Add Admin" and is_owner(message.chat.id):
        add_admin(message)
    
    elif message.text == "Remove Admin" and is_owner(message.chat.id):
        remove_admin(message)

    elif message.text == "Show Admins" and is_owner(message.chat.id):
        show_admins(message)
        
# handling callback queries
@bot.callback_query_handler(func=lambda call:True)
def call_action(call):
    answercall(call)


# handling the shipping query
@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):

    # making shipping options
    shipping_options = [telebot.types.ShippingOption(id='pickup', title='Local Pickup').add_price(telebot.types.LabeledPrice('Pickup', 0)), telebot.types.ShippingOption(id='delivery', title='Delivery').add_price(telebot.types.LabeledPrice('delivery', 500))]

    #print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)

# handling pre check out query
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    #print(pre_checkout_query)
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="SEEMS LIKE YOU'RE TRYING TO BUY FROM AN EXPIRED INVOICE\n\nPLEASE START A NEW INVOICE AND USE IT INSTEAD")


# handling successful payment
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    
    payment_action(message)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

# run the bot
bot.infinity_polling()
