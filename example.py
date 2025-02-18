from time import sleep
from whatsapp_bot import WhatsappBot

bot = WhatsappBot()
if bot.open(auth=True):
    print("Authorize")
    #bot.open_known_recipient("+79999999999")

bot.open_user_by_number("79999999999")
bot.send_text("Привет я")
sleep(30)
bot.close()