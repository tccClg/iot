import datetime
import telepot
import time
from telepot.loop import MessageLoop
import RPi.GPIO as IO
from time import sleep
IO.setmode(IO.BCM)
relay = 21
relay2= 20
IO.setup(relay,IO.OUT)
IO.setup(relay2,IO.OUT)
now=datetime.datetime.now()
def handle(msg):
    chat_id = msg['chat']['id']
    command=msg['text']
    print('Received')
    print(command)
    if command == '/hi':
        telegram_bot.sendMessage (chat_id, str("Hi!"))
    elif command == '/time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command == '/relayon':
        telegram_bot.sendMessage (chat_id, str("Relay1 On"))
        IO.output(relay,True)
    elif command == '/relayoff':
        telegram_bot.sendMessage (chat_id, str("Relay1 Off"))
        IO.output(relay,False)
telegram_bot = telepot.Bot('Token ID')
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')
while 1:
    time.sleep(10)