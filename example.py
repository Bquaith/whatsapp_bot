from time import sleep
from whatsapp_bot import WhatsappBot

bot = WhatsappBot()
if bot.open(auth=True):
    print("Authorize")
sleep(30)