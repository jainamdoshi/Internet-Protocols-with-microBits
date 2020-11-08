from microbit import *
import radio
import random

def calculate_number_of_parity_bits(length):
    total_parity_bits = 0
    while True:
        if (2 ** total_parity_bits) >= (length + total_parity_bits + 1):
            break
        total_parity_bits += 1
    return total_parity_bits

def insert_parity_bits(length, parity_bits, data):
    current_parity = 0
    data_index = 0
    data_with_parity = ['0'] #Place holder for parity 0

    for parity in range(1, length + parity_bits + 1):

        if parity == (2 ** current_parity):
            data_with_parity.append('0') #Place holder for all parity bit
            current_parity += 1
        else:
            data_with_parity.append(data[data_index])
            data_index += 1
        
    return data_with_parity

def set_hamming_code(total_parity_bits, data):

    #Looping as many times as the the number of parity bits starting from P1
    for parity in range(total_parity_bits):
        occurence_of_1 = 0

        #Looping through every segment of the data
        for data_index in range((2 ** parity), len(data), 2 ** (parity + 1)):

            #Looping through every bit in the segment.
            for bits_to_check in range(data_index, data_index + (2 ** parity)):
                if bits_to_check < len(data) and data[bits_to_check] == '1':
                    occurence_of_1 += 1
        
        #Set to 1, it the occurence of 1s are odd
        if occurence_of_1 % 2 != 0:
            data[(2**parity)] = '1'

    return data
    
def set_secded_code(data):
    occurence_of_1 = 0

    #Loop through all the bits
    for bit in data:
        if bit == '1':
            occurence_of_1 += 1

    #Set to 1, it the occurence of 1s are odd
    if occurence_of_1 % 2 != 0:
        data[0] = '1'

    return data

def initilize(DATA):
    
    length = len(DATA)
    
    total_parity_bits = calculate_number_of_parity_bits(length)
    data_with_parity = insert_parity_bits(length, total_parity_bits, DATA)
    data_with_parity = set_hamming_code(total_parity_bits, data_with_parity)
    data_with_parity = set_secded_code(data_with_parity)

    return data_with_parity

def start(message):
    error_count = 0
    while True:

        #Press button A to send the message
        if button_a.was_pressed():
            #display.scroll("".join(message))
            radio.send("".join(message))
            display.show(Image.ARROW_E)
            sleep(1000)
            display.clear()
            return

        #Press button B to add an error to the message (can be pressed multiple times)
        
        index = 0
        if button_b.was_pressed():
            if error_count <= 2:
                error_count += 1
                index = random.randrange(0, len(message))
                if message[index] == '0':
                    message[index] = '1'    
                else:
                    message[index] = '0'

'''
*    Title: Python Main Function implementation
*    Author: Bryan Weber
*    Date: n.d
*    Code version: 
*    Availability: https://realpython.com/python-main-function/
*
'''

if __name__ == "__main__":
    #DATA = "1011"
    
    radio.on()
    radio.config(group=5)
    while True:
        DATA = "010000110110111101101101"
        message = initilize("".join(reversed(DATA)))
        start(message)