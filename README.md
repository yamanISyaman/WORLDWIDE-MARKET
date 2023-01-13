# ***WORLDWIDE MARKET***

### this bot is my CS50X's final project

<hr>

#### Video Demo: [WW-Market-Video](https://youtu.be/TnEDsfbWRM8)

#### Bot Link: [WW-Market Link](https://t.me/world_wide_market_bot)

#### worldwide market is a telegram bot where you can buy a product no matter where it is, and as well you can sell your products no matter where you are.

<hr>

## Installation

1. set-up your bot following these steps:
   - open telegram
   - open this bot: [BotFather](https://t.me/BotFather)
   - from Menu click the /newbot command to create new bot and save the bot token
   - follow this steps [[Getting Payment Token](https://core.telegram.org/bots/payments#getting-a-token)] to get a payments provider token. But Note: this bot uses "Stripe" as its provider and hardly recommend to use it to avoid any errors
2. you need to install the pyTelegramBotAPI library. [see the Installation Guide](https://pytba.readthedocs.io/en/latest/install.html)

3. Run this commands in your terminal
   - `export BOT_TOKEN=Your_Bot_Token`
   - `export PROVIDER_TOKEN=Your_Payments_Provider_Token`
   - `export PASSWORD=This_Password_You_Will_Be_Asked_For_Later_To_Prove_That_You're_The_Owner`
###### when you want to start the bot, run this command:
###### `python main.py`

#### and now your bot should work properly.

# How Does It Work?
#### first you should know that this bot has three levels of users:
- Owners
- Admins
- Users
##### each type has the same features of the types below it and few more

## First Time Running The Bot
### If The Bot Has No Owners:
###### at this point the database will be all empty.
###### No matter what you or any user type, the bot will ask for a password (Which is the password you exported in the 3rd step of installation).
###### if the password is wrong, the bot will ask to try again, so please start the bot and enter the password right after running the bot.
###### if the password is right, you'll get a message tells you that you are added as an owner and the bot would start to work for any other user.

### If The Bot Has An Owner:
###### the bot will sends you a welcoming message and displays a Markup keyboard buttons in the place of the regular letter-keyboard.


# Markup Keyboard Buttons
###### the markup keyboard appears in the place of the regular letter-keyboard.

- # Main Menu Buttons:
## 1. Add Product
> #### Who Has Access To It :
###### (Owners  - Admins - Users)
> #### What This Button Do:
###### it walks you through the process of adding a new product.

## 2. Pending Products
> #### Who Has Access To It :
###### (Owners  - Admins)
> #### What This Button Do:
###### show all the pending products.

## 3. Find A Product
> #### Who Has Access To It :
###### (Owners  - Admins - Users)
> #### What This Button Do:
###### it gives the option to either show all products or use the search to find an approved product.

## 4. My Products
> #### Who Has Access To It : 
###### (Owners  - Admins - Users)
> #### What This Button Do:
###### it shows the user all the approved products they posted.

## 5. My Cart
> #### Who Has Access To It :
###### (Owners  - Admins - Users)
> #### What This Button Do:
###### it shows the user all the products they added to their cart.

## 6. My Balance
> #### Who Has Access To It :
###### (Owners  - Admins - Users)
> #### What This Button Do:
###### it shows your balance which increases when someone buys your products.

## 7. Bought Products
> #### Who Has Access To It :
###### (Owners  - Admins - Users)
> #### What This Button Do:
###### it shows the user all the delivered and undelivered products they bought.

## 8. Report An Issue
> #### Who Has Access To It : 
###### (Owners  - Admins - Users)
> #### What This Button Do:
###### it lets the user sends a message to the (admins/owners).

## 9. Close Payment
> #### Who Has Access To It :
###### (Owners  - Admins)
> #### What This Button Do:
###### it lets the admins close a payment using the payment id when the product is delivered

## 10. Send Notification
> #### Who Has Access To It :
###### (Owners  - Admins)
> #### What This Button Do:
###### it lets the admins send a message to a specific user using the user's id

## 11. Add Admin
> #### Who Has Access To It :
###### (Owners)
> #### What This Button Do:
###### it lets the owner promote a user to an admin

## 12. Remove Admin
> #### Who Has Access To It : 
###### (Owners)
> #### What This Button Do:
###### it lets the owner demote an admin to a user

## 13. Show Admins
> #### Who Has Access To It :
###### (Owners)
> #### What This Button Do:
###### it shows the owner a list of the admins and their ids


- # Other Markup Buttons
## 1. Cancel!
> #### When This Button Appears:
###### at almost all process that have multiple steps like (add product, add admin, report an issue...etc)
> #### What This Button Does:
###### it Cancels the process that's support it and redirect the user to the main menu

## 2. Show All Products
> #### When This Button Appears:
###### when the "find a product" button is clicked
> #### What This Button Does:
###### it shows all the approved products

## 3. Search
> #### When This Button Appears:
###### when the "find a product" button is clicked
> #### What This Button Does:
###### it lets the user type a search word and then show all the products posts that contain this search word

## 4. Back To Menu
> #### When This Button Appears:
###### when the "find a product" button is clicked
> #### What This Button Does:
###### it redirects the user to the main menu

# Inline Keyboard Buttons
###### this keyboard appears at the end of the message

## 1. Previous
> #### What Messages Does This Button Appears On:
###### on the results of (show all products - search - my cart - bought products - my products - pending posts) if the number of the posts more than one.
> #### What This Button Does:
###### it swipes to the previous post.

## 2. Next
> #### What Messages Does This Button Appears On:
###### on the results of (show all products - search - my cart - bought products - my products - pending posts) if the number of the posts more than one.
> #### What This Button Does:
###### it swipes to the next post.

## 3. Add To Cart
> #### What Messages Does This Button Appears On:
###### on the results of (show all products - search)
> #### What This Button Does:
###### it adds that product to the user's cart.

## 4. Buy
> #### What Messages Does This Button Appears On:
###### on the results of (show all products - search - my cart)
> #### What This Button Does:
###### it sends the user the invoice of that product to buy it.

## 5. Delete
> #### What Messages Does This Button Appears On:
###### it appears in two cases:
###### 1. on the results of (bought products) when the payment is closed.
###### 2. on the results of (show all products) when the user type is (owner/adimn).
> #### What This Button Does:
###### in the case (1): it removes that closed payment from the history of the user.
###### in the case (2): it delete that product from the database entirely.

## 6. Approve
> #### What Messages Does This Button Appears On:
###### on the results of (Pending Posts)
> #### What This Button Does:
###### the can click it to approve on a pending post so all users can view it

## 6. Disapprove
> #### What Messages Does This Button Appears On:
###### on the results of (Pending Posts)
> #### What This Button Does:
###### the can click it to disapprove on a pending post so it will be deleted from the database entirely

# Files
###### this bot consists of five files:
## 1. main.py
###### this file has all the message handlers that takes the coming message and depending on its type, contents..etc, the appropriate filter will be called.
###### and this is the file that you need to run to let the bot start.

## 2. responses.py
###### this file has all the filters functions that are responsible for showing the appropriate response to the users.

## 3. handy.py
###### this file has some useful functions to prevent us from copy pasting in the previous two files and also can be used for building other telegram bots.

## 4. welcoming.py
###### this file only has one variable which is the welcoming message that appears for a new user.

## 5. data.db
###### a sqlite3 database where all the users ids and products are saved
### Database Contents

<table>
  <tr>
    <th>Table</th>
    <th>Column 1</th>
    <th>Column 2</th>
    <th>Column 3</th>
    <th>Column 4</th>
    <th>Column 5</th>
    <th>Column 6</th>
    <th>Column 7</th>
    <th>Column 8</th>
    <th>Column 9</th>
  </tr>
  <tr>
    <td>users</td>
    <td>id</td>
    <td>name</td>
    <td>is_admin</td>
    <td>balance</td>
    <td>last_sw</td>
  </tr>
  <tr>
    <td>products</td>
    <td>id</td>
    <td>owner_id</td>
    <td>name</td>
    <td>price</td>
    <td>description</td>
    <td>country</td>
    <td>city</td>
    <td>photo_id</td>
    <td>is_approved</td>
  </tr>
  <tr>
    <td>cart</td>
    <td>user_id</td>
    <td>product_id</td>
  </tr>
  <tr>
    <td>history</td>
    <td>id</td>
    <td>user_id</td>
    <td>product_id</td>
    <td>charge_id</td>
    <td>done</td>
  </tr>
</table>

# Security
- #### the database is secure against any injection attacks
- #### the bot has been cautiously built to handle any user messages at anytime without getting broken
<hr>