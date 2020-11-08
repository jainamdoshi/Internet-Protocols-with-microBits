from microbit import *
import radio

'''
*    Title: How to read the device serial number
*    Author: Karl Marklund
*    Date: 5 November 2019
*    Code version: 
*    Availability: https://support.microbit.org/support/solutions/articles/19000070728-how-to-read-the-device-serial-number
*
'''
#This function return the unique serial ID of the microbit
def get_serial_number(type=hex):
    NRF_FICR_BASE = 0x10000000
    DEVICEID_INDEX = 25

    @micropython.asm_thumb
    def reg_read(r0):
        ldr(r0, [r0, 0])
    return type(reg_read(NRF_FICR_BASE + (DEVICEID_INDEX*4)))
   

def start():

    IP_address = "2.2.2.2"

    #Listens for the broadcast and sends the MAC address back to the sender
    while True:
        message = radio.receive()
        if message:
            
            receiver_address = message[message.find(":") + 1: message.find(" ")]
            if receiver_address == IP_address:
                sender_address = message[:message.find(":")]
                frame = sender_address + ":" + IP_address + " " + str(get_serial_number())[3:]
                radio.send(frame)

'''
*    Title: Python Main Function implementation
*    Author: Bryan Weber
*    Date: n.d
*    Code version: 
*    Availability: https://realpython.com/python-main-function/
*
'''
if __name__ == "__main__":
    radio.on()
    radio.config(group=5)
    while True:
        if button_a.was_pressed():
            start()
