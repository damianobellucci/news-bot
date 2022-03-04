import time
from send import send_messages
starttime = time.time()


while True:
    send_messages()
    time.sleep(4)