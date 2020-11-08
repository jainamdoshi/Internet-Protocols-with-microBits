from microbit import *
import radio

#This function will convert the format of the MAC from xxxxxxxx to xx-xx-xx-xx
def get_MAC_address(MAC):   
    cnt = 0
    MAC_address = ""
   
    for i in range(len(MAC)):
        if i % 2 == 0:    
            MAC_address += "-" + MAC[i]
        else:
            MAC_address += MAC[i]
    return MAC_address[1:]

#This fuction will send a broadcasting request for the MAC address and wait for the MAC address from the receiver
def get_MAC(sender_IP_address, receiver_IP_address):
    radio.send(sender_IP_address + ":" + receiver_IP_address + " GET MAC ADDRESS")

    while True:
        MAC = radio.receive()
        if MAC and MAC.startswith(sender_IP_address + ":" + receiver_IP_address):
            index = MAC.find(" ") + 1
            MAC = get_MAC_address(MAC[index:])
            return MAC

def start(ARP_cache):
    sender_IP_address = "1.1.1.1"
    receiver_IP_address = "2.2.2.2"

    while True:

        #Looks in the ARP cache, if the MAC Address is not there, then it will request and add in the table or look it up in the table and will display it.
        if ARP_cache.get(receiver_IP_address) is None:
            MAC = get_MAC(sender_IP_address, receiver_IP_address)  #broadcasts a request and waits till it gets the MAC address.
            ARP_cache[receiver_IP_address] = [MAC, "dynamic"]
        else:
            display.scroll(receiver_IP_address)
            display.scroll(ARP_cache.get(receiver_IP_address)[0])
            return ARP_cache

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
        ARP_cache = {}
        if button_a.was_pressed():
            ARP_table = start(ARP_cache)