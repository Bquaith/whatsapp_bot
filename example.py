from time import sleep
from whatsapp_bot import WhatsappBot

bot = WhatsappBot()
if bot.open(auth=True):
    print("Authorize")

bot.open_user_by_number("79999999999")
bot.send_text("Hi")
bot.send_file("file", "/whatsapp_bot/.file/mem.jpg", "Hi")
sleep(30)
bot.close()
