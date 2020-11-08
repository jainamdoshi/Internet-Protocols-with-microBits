from microbit import *
import radio

def check_hamming_code(lst, parity, data):
    occurence_of_1 = 0

    #list if the parity bit is correct
    lst1 = lst[:]

    #list if the parity bit is not correct
    lst2 = lst[:]

    #Looping through every segment of the data
    for data_index in range((2 ** parity), len(data), 2 ** (parity + 1)):

        #Looping through every bit in the segment.
        for bits_to_check in range(data_index, data_index+(2 ** parity)):
            if bits_to_check >= len(data):
                break
            if data[bits_to_check] == '1':
                occurence_of_1 += 1
            lst1[bits_to_check] = None
            if lst2[bits_to_check] is not None:
                lst2[bits_to_check] += 1
    
    if occurence_of_1 % 2 == 0:
        return lst1
    else:
        return lst2

def check_secded_code(lst, data):
    occurence_of_1 = 0
    for bits_to_check in range(len(data)):
        if data[bits_to_check] == '1':
            occurence_of_1 += 1
    
    if occurence_of_1 % 2 == 0:
        lst[0] = None

    return lst

def start(data):
    #main list
    lst = [0 for y in range(len(data))]

    index = 0
    parity = 0
    
    #Looping as many times as the the number of parity bits starting from P1
    while True:
        lst = check_hamming_code(lst, parity, data)
        
        parity += 1
        index = 2 ** parity
        if index >= len(data):
            break
    
    lst = check_secded_code(lst, data)
    
    highest = -1
    pos = None
    highest_count = 0
    for parity in range(len(lst)):
        if lst[parity] is not None and lst[parity] > highest:
            high = lst[parity]
            pos = parity
            highest_count = 0
        elif lst[parity] == highest:
            highest_count = None
    
    #2 bit or more bit error
    if highest_count is None:
        display.show(Image.CONFUSED)
        sleep(1000)
        display.clear()
        return
    #Error free
    elif pos is None:
        display.show(Image.YES)
        sleep(1000)
        display.clear()
        return
    #2 bit or more bit error
    elif lst[0] is None:
        display.show(Image.CONFUSED)
        sleep(1000)
        display.clear()
        return
    #1 bit correcable error
    else:
        message = list(data)
        message[pos] = str(((int(message[pos])) + 1) % 2)
        message = "".join(message)
        display.show(Image.SURPRISED)
        sleep(1000)
        display.clear()
        return

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
        message = radio.receive()
        #message = "01010101"
        if message:
            start(message)
            message = None