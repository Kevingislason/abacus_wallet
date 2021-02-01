import sys
from hardware_wallet.app import App
# todo: wrap in try catch to prevent error info from "leaking" over stdout
App()


# try:
#     import uos
#     import sys
#     import os
#     import pyb
#     import display
#     from hardware_wallet.persistence import Persistence

#     uos.dupterm(None, 1)

#     display.init()

#     l3 = pyb.LED(3)
#     l4 = pyb.LED(4)
#     l3.toggle()

#     uart = pyb.UART(2, 115200)
#     l4.toggle()

#     line = 'success'
#     while not uart.read():
#         pass
#     Persistence.save_debug(line, "message.txt")

#     uart.write("message from uart \n")
#     display.init()

# except Exception as e:
#     Persistence.save_debug(str(e), "exception.txt")
